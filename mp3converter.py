from pathlib import Path
import subprocess
import json
import sys

# Change this to your music directory, or pass it as the first command-line argument.
SOURCE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
OUTPUT_DIR = SOURCE_DIR / "converted_mp3"

SUPPORTED_INPUTS = {
    ".mp3",
    ".wma",
    ".wav",
    ".flac",
    ".m4a",
    ".aac",
    ".ogg",
    ".opus",
    ".alac",
}

def get_metadata(input_file):
    """Read basic metadata with ffprobe."""
    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_entries", "format_tags",
        str(input_file),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        tags = data.get("format", {}).get("tags", {}) or {}

        # FFmpeg may return uppercase or lowercase tag names.
        return {
            key.lower(): value
            for key, value in tags.items()
        }
    except Exception:
        return {}

def convert_file(input_file):
    relative_path = input_file.relative_to(SOURCE_DIR)
    output_file = OUTPUT_DIR / relative_path.with_suffix(".mp3")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    tags = get_metadata(input_file)

    title = tags.get("title") or input_file.stem
    album = tags.get("album")
    artist = tags.get("artist")
    album_artist = tags.get("album_artist") or tags.get("albumartist")
    genre = tags.get("genre")
    date = tags.get("date") or tags.get("year")
    track = tags.get("track") or tags.get("tracknumber")
    disc = tags.get("disc") or tags.get("discnumber")
    comment = tags.get("comment")

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",
        "-y",
        "-i", str(input_file),

        # Select the first audio stream only.
        "-map", "0:a:0",

        # Very widely supported MP3 format.
        "-c:a", "libmp3lame",
        "-b:a", "320k",
        "-ar", "44100",
        "-ac", "2",

        # Compatible ID3 tagging.
        "-id3v2_version", "3",
        "-write_id3v1", "1",

        # Prevent accidental replay gain or encoder metadata issues.
        "-map_metadata", "-1",

        str(output_file),
    ]

    # Add cleaned metadata explicitly.
    metadata = {
        "title": title,
    }

    if album:
        metadata["album"] = album
    if artist:
        metadata["artist"] = artist
    if album_artist:
        metadata["album_artist"] = album_artist
    if genre:
        metadata["genre"] = genre
    if date:
        metadata["date"] = date
    if track:
        metadata["track"] = track
    if disc:
        metadata["disc"] = disc
    if comment:
        metadata["comment"] = comment

    for key, value in metadata.items():
        command.extend(["-metadata", f"{key}={value}"])

    print(f"Converting: {input_file}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"FAILED: {input_file}")

def main():
    if not SOURCE_DIR.exists():
        print(f"Directory does not exist: {SOURCE_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    files = [
        path for path in SOURCE_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_INPUTS
        and OUTPUT_DIR not in path.parents
    ]

    if not files:
        print("No supported audio files found.")
        return

    print(f"Found {len(files)} audio files.")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    for file in files:
        convert_file(file)

    print()
    print("Finished.")
    print("Point Jellyfin at the 'converted_mp3' directory, or replace your old library after checking the results.")

if __name__ == "__main__":
    main()
