# `tablify`

Lines up markdown tables in monospace columns. Cells that make a table too wide are wrapped
to fit.

Copy a table from your editor, run `tablify`, and paste the aligned version.

## Example

Input:

```
| What | Value | Code |
|---|---|---|
| Guncam focal length | **36445 px/rad** (636.1 px/deg) | `apriltags.GUNCAM_FX` |
| LRF parallax | **73mm right** of the guncam: the beam center is `fx * 0.073 / R` px right of the boresight | `server.py` |
```

`tablify -w 70`:

```
| What           | Value                     | Code                  |
|----------------|---------------------------|-----------------------|
| Guncam focal   | **36445 px/rad** (636.1   | `apriltags.GUNCAM_FX` |
| length         | px/deg)                   |                       |
|                |                           |                       |
| LRF parallax   | **73mm right** of the     | `server.py`           |
|                | guncam: the beam center   |                       |
|                | is `fx * 0.073 / R` px    |                       |
|                | right of the boresight    |                       |
```

If any cell wraps, an empty row separates the entries. Column widths are picked to keep
the number of wrapped lines low. A table that already fits is only aligned, never wrapped.

## Usage

```
tablify                  # format the clipboard in place (xclip), and print it
tablify file.md ...      # print the formatted files
tablify -i file.md ...   # rewrite the files in place
cat file.md | tablify    # format stdin to stdout
```

The clipboard is only read or written when there are no files and nothing is piped in.

## Options

| Option                 | Effect                                                         |
|------------------------|----------------------------------------------------------------|
| `-w N`, `--width N`    | max table width, default 120; `-w 0` aligns without wrapping   |
| `-k`, `--strip-markup` | strip `**` and backticks from cells; by default they are kept  |
| `--no-gap`             | don't put empty rows between wrapped entries                   |
| `-f`, `--fence`        | wrap the output in a ``` block, e.g. for Slack                 |
| `-p`, `--print-only`   | clipboard mode: print the result but leave the clipboard alone |
| `-i`, `--in-place`     | rewrite the given files                                        |
| `--min-col N`          | narrowest a column may shrink to, default 8                    |
| `--max-word N`         | words longer than this may be broken mid-word, default 40      |

## Safe on whole files

Only GitHub-style tables are changed: a header row, then a `|---|` row. Everything else passes
through byte-for-byte:

- prose, lists and headings
- anything inside ``` or ~~~ fences
- `|` lines with no `|---|` row
- indentation, line endings and the trailing newline

Running it again gives the same output. A table that `tablify` already wrapped is joined back
into one row per entry (using the empty rows) and then wrapped again, so `-i` is safe to repeat.

## Caveats

- Wrapped tables aren't valid markdown and won't render as tables. Use `-w 0` for files you
  want to keep rendering.
- A table wrapped with `--no-gap` can't be joined back later, because nothing marks where one
  entry ends and the next begins.
- A word longer than `--max-word` is broken mid-word, and joining the table back puts a space
  at the break.
