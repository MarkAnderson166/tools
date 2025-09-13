import os
import threading
import json
import requests
import urllib.parse
import http.server
import socketserver
from tkinter import Tk, Button, Label, Frame, messagebox, ttk
from pathlib import Path

# --- CONFIG ---
PORT = 8000
HOSTS = {
    "Mark-Desktop-Fedora": "192.168.0.140",
    "Guybrush-Laptop": "192.168.0.135",
    "Naomi-Desktop": "192.168.0.9",
    "Mark-Laptop": "192.168.0.39",
}
SELF_NAME = os.uname().nodename.lower() if hasattr(os, "uname") else os.getenv("COMPUTERNAME", "").lower()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SYNC_DIR = SCRIPT_DIR

# --- SERVER HANDLER ---
class SyncHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/filelist.json':
            file_list = []
            for root, dirs, files in os.walk(SYNC_DIR):
                for fname in files:
                    full_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(full_path, SYNC_DIR)
                    rel_path = rel_path.replace("\\", "/")  # ensure consistent separators
                    size = os.path.getsize(full_path)
                    mtime = os.path.getmtime(full_path)
                    file_list.append({'path': rel_path, 'size': size, 'mtime': mtime})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(file_list).encode())
        elif parsed_path.path == '/file':
            qs = urllib.parse.parse_qs(parsed_path.query)
            rel_path = qs.get('path', [None])[0]
            if not rel_path:
                self.send_error(400, "Missing file path")
                return
            rel_path = urllib.parse.unquote(rel_path)
            safe_path = os.path.abspath(os.path.join(SYNC_DIR, rel_path))
            if not safe_path.startswith(SYNC_DIR):
                self.send_error(403, "Access denied")
                return
            if not os.path.exists(safe_path):
                self.send_error(404, "File not found")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", os.path.getsize(safe_path))
            self.end_headers()
            with open(safe_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        if self.path == '/ping':
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        return


def start_server():
    def _run():
        with socketserver.TCPServer(("", PORT), SyncHandler) as httpd:
            httpd.serve_forever()
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


# --- SYNC CLIENT ---
def pull_from_host(ip, progress_bar):
    try:
        filelist_url = f"http://{ip}:{PORT}/filelist.json"
        r = requests.get(filelist_url, timeout=5)
        r.raise_for_status()
        file_list = r.json()
        total_files = len(file_list)
        if total_files == 0:
            raise Exception("No files to pull")

        for idx, entry in enumerate(file_list, 1):
            rel_path = entry['path']
            dest_path = os.path.join(SYNC_DIR, *rel_path.split("/"))  # split to handle subfolders
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            encoded_path = urllib.parse.quote(rel_path)
            file_url = f"http://{ip}:{PORT}/file?path={encoded_path}"
            r = requests.get(file_url, stream=True, timeout=10)
            r.raise_for_status()

            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            progress_bar['value'] = (idx / total_files) * 100
            progress_bar.update_idletasks()

        messagebox.showinfo("Sync Complete", f"Pulled {total_files} files from {ip}")
    except Exception as e:
        messagebox.showerror("Sync Error", f"{ip}: {e}")
    finally:
        progress_bar['value'] = 0


# --- CHECK HOSTS ---
def check_online_hosts():
    status = {}
    for name, ip in HOSTS.items():
        if name.lower() == SELF_NAME:
            continue
        try:
            r = requests.post(f"http://{ip}:{PORT}/ping", timeout=1)
            status[name] = r.status_code == 200
        except:
            status[name] = False
    return status


# --- GUI ---
def create_gui():
    root = Tk()
    root.title("Folder Sync Tool")
    Label(root, text=f"Sharing: {SYNC_DIR}").pack(pady=5)

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=5)

    status_frame = Frame(root)
    status_frame.pack(pady=10)

    host_buttons = {}

    def refresh():
        online_status = check_online_hosts()
        for name, ip in HOSTS.items():
            if name.lower() == SELF_NAME:
                continue
            status = online_status.get(name, False)
            symbol = "✓" if status else "✗"
            text = f"{symbol} Pull from {name} ({ip})"
            if name in host_buttons:
                host_buttons[name].config(text=text, state='normal' if status else 'disabled')
            else:
                btn = Button(status_frame,
                             text=text,
                             command=lambda ip=ip: pull_from_host(ip, progress),
                             state='normal' if status else 'disabled')
                btn.pack(fill='x', pady=2)
                host_buttons[name] = btn

    Button(root, text="Refresh Hosts", command=refresh).pack(pady=5)
    refresh()
    root.mainloop()


if __name__ == "__main__":
    start_server()
    create_gui()
