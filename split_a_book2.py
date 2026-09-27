import json
import math
import subprocess
from pathlib import Path


CHUNK_LENGTH = 30 * 60  # Used only for MP3 files
SPEED = 1.3


def get_duration(input_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(input_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(result.stdout.strip())


def get_chapters(input_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_chapters",
            "-of", "json",
            str(input_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    return data.get("chapters", [])


def process_mp3(input_file):
    """
    MP3 behavior:
    Split into fixed-length parts, then speed up each part.
    """

    output_dir = Path.cwd() / input_file.stem
    output_dir.mkdir(exist_ok=True)

    duration = get_duration(input_file)
    number_of_parts = math.ceil(duration / CHUNK_LENGTH)

    for part_number in range(number_of_parts):
        start_time = part_number * CHUNK_LENGTH
        part_name = f"Part {part_number + 1:03d}"
        output_file = output_dir / f"part_{part_number + 1:03d}.mp3"

        print(f"Creating {output_file}...")

        subprocess.run(
            [
                "ffmpeg",
                "-y",

                "-ss", str(start_time),
                "-t", str(CHUNK_LENGTH),
                "-i", str(input_file),

                "-vn",
                "-filter:a", f"atempo={SPEED}",
                "-c:a", "libmp3lame",
                "-q:a", "2",

                # Remove inherited metadata.
                "-map_metadata", "-1",

                # Add metadata.
                "-metadata", f"title={part_name}",
                "-metadata", f"album={input_file.stem}",
                "-metadata", f"track={part_number + 1}",

                str(output_file),
            ],
            check=True,
        )

    print(
        f"Done. Created {number_of_parts} MP3 files in {output_dir}/"
    )


def process_m4b(input_file):
    """
    M4B behavior:
    Split according to embedded chapter markers, then speed up each chapter.
    """

    chapters = get_chapters(input_file)

    if not chapters:
        print(
            f"Skipping {input_file.name}: "
            "no chapter markers were found."
        )
        return

    output_dir = Path.cwd() / input_file.stem
    output_dir.mkdir(exist_ok=True)

    for chapter_number, chapter in enumerate(chapters, start=1):
        start_time = float(chapter["start_time"])
        end_time = float(chapter["end_time"])
        chapter_duration = end_time - start_time

        tags = chapter.get("tags", {})
        chapter_title = tags.get(
            "title",
            f"Chapter {chapter_number}"
        )

        # Make the chapter title safe for use in a filename.
        safe_title = "".join(
            character
            if character.isalnum() or character in " .-_"
            else "_"
            for character in chapter_title
        ).strip()

        if not safe_title:
            safe_title = f"Chapter {chapter_number:03d}"

        # Example:
        # 01 - Chapter 1.m4b
        output_file = (
            output_dir
            / f"{chapter_number:02d} - {safe_title}.m4b"
        )

        print(f"Creating {output_file}...")

        subprocess.run(
            [
                "ffmpeg",
                "-y",

                # These are input options.
                # The complete original chapter is extracted first.
                "-ss", str(start_time),
                "-t", str(chapter_duration),
                "-i", str(input_file),

                # Select the main audio stream.
                "-map", "0:a:0",

                # Speed up the selected chapter.
                "-filter:a", f"atempo={SPEED}",

                # Encode as AAC inside an M4B container.
                "-c:a", "aac",
                "-b:a", "96k",

                # Each output file is already one chapter.
                "-map_chapters", "-1",

                # Remove inherited metadata.
                "-map_metadata", "-1",

                # Add useful metadata.
                "-metadata", f"title={chapter_title}",
                "-metadata", f"album={input_file.stem}",
                "-metadata", f"track={chapter_number}",
                "-metadata", f"tracktotal={len(chapters)}",

                # Allow playback to begin before the entire file downloads.
                "-movflags", "+faststart",

                str(output_file),
            ],
            check=True,
        )

    print(
        f"Done. Created {len(chapters)} M4B files in {output_dir}/"
    )


def main():
    # Process files in the folder where the script is run.
    input_directory = Path.cwd()

    input_files = sorted(
        file_path
        for file_path in input_directory.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in {".mp3", ".m4b"}
    )

    if not input_files:
        print(
            "No .mp3 or .m4b files were found in "
            f"{input_directory}"
        )
        return

    print(
        f"Found {len(input_files)} audiobook file(s) "
        f"in {input_directory}\n"
    )

    for input_file in input_files:
        print(f"Processing: {input_file.name}")

        try:
            if input_file.suffix.lower() == ".mp3":
                process_mp3(input_file)
            elif input_file.suffix.lower() == ".m4b":
                process_m4b(input_file)

        except subprocess.CalledProcessError as error:
            print(
                f"FFmpeg or ffprobe failed while processing "
                f"{input_file.name}: {error}\n"
            )

        except Exception as error:
            print(
                f"Error while processing {input_file.name}: "
                f"{error}\n"
            )

    print("All files have been processed.")


if __name__ == "__main__":
    main()
