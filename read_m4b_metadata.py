import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_LINES_PER_PAGE = 40


def get_metadata(input_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            "-of", "json",
            str(input_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout)


def print_paginated(text, lines_per_page):
    lines = text.splitlines()

    for start in range(0, len(lines), lines_per_page):
        page = lines[start:start + lines_per_page]

        print("\n".join(page))

        if start + lines_per_page < len(lines):
            try:
                input("\n--- Press Enter for more ---\n")
            except KeyboardInterrupt:
                print()
                return


def main():
    parser = argparse.ArgumentParser(
        description="Print FFmpeg metadata as formatted JSON."
    )

    parser.add_argument(
        "input_file",
        help="Path to an MP3 or M4B file",
    )

    parser.add_argument(
        "--lines",
        type=int,
        default=DEFAULT_LINES_PER_PAGE,
        help=(
            "Number of lines to display per page "
            f"(default: {DEFAULT_LINES_PER_PAGE})"
        ),
    )

    args = parser.parse_args()
    input_file = Path(args.input_file)

    if not input_file.exists():
        raise FileNotFoundError(
            f"File not found: {input_file}"
        )

    if args.lines < 1:
        raise ValueError(
            "The number of lines per page must be at least 1."
        )

    try:
        metadata = get_metadata(input_file)
    except subprocess.CalledProcessError as error:
        print(
            "ffprobe could not read the file.",
            file=sys.stderr,
        )

        if error.stderr:
            print(error.stderr, file=sys.stderr)

        sys.exit(1)

    formatted_metadata = json.dumps(
        metadata,
        indent=4,
        ensure_ascii=False,
    )

    print_paginated(
        formatted_metadata,
        args.lines,
    )


if __name__ == "__main__":
    main()
