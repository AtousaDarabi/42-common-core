"""Writes a generated maze to disk using the subject's output file format."""

import sys
from typing import List, Tuple


def write_maze_file(
    hex_rows: List[str],
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path: str,
    output_file: str,
) -> None:
    """!
    @brief Writes the maze to `output_file` in the required format.
    @param hex_rows One hexadecimal-encoded string per maze row.
    @param entry Entry coordinates (x, y).
    @param exit_cell Exit coordinates (x, y).
    @param path The shortest entry-to-exit path, as a string of
           N/E/S/W letters.
    @param output_file Destination file path.
    @details Rows are written first, then a blank line, then entry, exit and
             path each on their own line, exactly as specified by the subject.
             The `with` block below guarantees the file handle is flushed and
             closed the moment writing finishes -- even if an exception is
             raised mid-write -- so no extra close() call is needed. A write
             failure never crashes with a raw traceback; it's reported and
             the process exits cleanly instead, per the subject's
             error-handling requirement.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as handle:
            for row in hex_rows:
                handle.write(row + "\n")
            handle.write("\n")
            handle.write(f"{entry[0]},{entry[1]}\n")
            handle.write(f"{exit_cell[0]},{exit_cell[1]}\n")
            handle.write(f"{path}\n")
    except OSError as exc:
        print(
            f"Error: unable to save to file '{output_file}': {exc}",
            file=sys.stderr,
        )
        sys.exit(1)
