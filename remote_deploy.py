import http.server
import os
import subprocess

pw = 'aaaaaaaa'

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    print(f"GET request received at {self.path}")
    if self.path.startswith('/%s_%s'%(pw,'push_')):
      try:
        os.chdir('/home/Mark/Projects/%s'%self.path.split('_')[2])
        result = subprocess.run(['git', 'boom', 'remote_push'], capture_output=True, text=True, check=True)
        output = result.stdout + result.stderr
        output_bytes = output.encode("utf-8")

        self.send_response(200 if result.returncode == 0 else 500)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(output_bytes)))
        self.end_headers()
        self.wfile.write(output_bytes)

      except Exception as exc:
        output_bytes = f"Server error: {exc}\n".encode()

        self.send_response(500)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(output_bytes)))
        self.end_headers()
        self.wfile.write(output_bytes)


def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8042) 
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()

