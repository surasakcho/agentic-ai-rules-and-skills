# Never rely on the platform's default text encoding

**Task type:** data engineering — reading and writing text anywhere.

---

## The rule

Windows Python decodes and encodes text with the **locale codec** (cp1252, or cp874 on a
Thai-locale machine); Linux and macOS use UTF-8. Code written on one and run on the other
breaks. Make encoding explicit **as the code is written**, not after a crash:

- `open(...)` → pass `encoding="utf-8"` unless the mode is binary
- `subprocess.run(..., text=True)` → pass `encoding="utf-8"`, usually with `errors="replace"`
- PowerShell `Set-Content` / `Add-Content` → pass `-Encoding utf8`
- CLI entry points → enable UTF-8 mode via `-X utf8` / `PYTHONUTF8=1`

## Why the crash is the harmless version

Failing to print an em dash is loud and gets fixed immediately. The dangerous version is JSON
or Markdown **written** with the locale codec on Windows and **read back** as UTF-8 elsewhere
— another machine, CI, a Raspberry Pi. That does not raise; it corrupts. And once text is
mixed-encoding, a blanket re-decode makes it worse: it has to be repaired symbol by symbol.

## The incident

A shapefile reader caught `UnicodeDecodeError` and retried by re-reading **the whole file**
as TIS-620. One bad field therefore re-decoded every field in the file.

- **Cost:** 164 corrupted Thai labels, shipped and unnoticed.
- **The first fix made it worse** — 165 bad rows became **13,697** — because its loop guard
  tested `dtype != object` and the pandas version in use returned `StringDtype`.
- The published root-cause analysis was *also* wrong on the first attempt: it blamed a
  detector for being "blind to cp874" when the actual cause was the whole-file fallback.

Three separate errors on one defect. The final fix decodes **per column**, byte-preserving,
choosing the codec that yields fewer replacement characters, with a post-condition that raises
if any value still begins with a known mojibake prefix.

## Do not audit this with grep

A line-oriented search misses the keyword when a call spans lines, and flags `Image.open(p)`
and `p.open("rb")` as false positives. Acting on that output breaks working code. **Parse the
AST**, or read the whole call before editing it.
