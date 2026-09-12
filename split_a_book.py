import argparse
import math
import subprocess
from pathlib import Path


CHUNK_LENGTH = 30 * 60  # 30 minutes
SPEED = 1.4


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


parser = argparse.ArgumentParser(
    description="Split, speed up, and tag an MP3."
)
parser.add_argument("input_file", help="Path to the input MP3 file")
args = parser.parse_args()

input_file = Path(args.input_file)

if not input_file.exists():
    raise FileNotFoundError(f"File not found: {input_file}")

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

            # Remove inherited metadata
            "-map_metadata", "-1",

            # Metadata VLC can display
            "-metadata", f"title={part_name}",
            "-metadata", f"album={input_file.stem}",
            "-metadata", f"track={part_number + 1}",

            str(output_file),
        ],
        check=True,
    )

print(f"Done. Created {number_of_parts} files in {output_dir}/")
