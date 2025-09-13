import subprocess

input_file = 'links.txt'

with open(input_file, 'r') as f:
    links = [line.strip() for line in f if line.strip()]

for link in links:
    print(f"Processing: {link}")
    try:
        subprocess.run([
            'yt-dlp',
            '-x',
            '--audio-format', 'mp3',
            '--audio-quality', '128k',
            '-o', '%(title)s.%(ext)s',
            link
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {link}: {e}")

