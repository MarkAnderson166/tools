import http.server
import os
import subprocess

pw = 'ffffff'

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    print(f"GET request received at {self.path}")
    if self.path.startswith('/%s_'%(pw)):
      try:
        bits = self.path.split('_')
        wd = '/home/Mark/Projects/%s'%(bits[2])
        os.chdir(wd)

        if bits[1] == 'status':
          r1 = subprocess.run(['git', 'status'], capture_output=True, text=True, check=True)
          output = r1.stdout + r1.stderr
        
        elif bits[1] == 'push':
          r1 = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True, check=True)
          r2 = subprocess.run(['git', 'commit', '-m',  'remote_push'], capture_output=True, text=True, check=True)
          r3 = subprocess.run(['git', 'pull'], capture_output=True, text=True, check=True)
          r4 = subprocess.run(['git', 'push'], capture_output=True, text=True, check=True)
          output = r1.stdout + r1.stderr + r2.stdout + r2.stderr + r3.stdout + r3.stderr + r4.stdout + r4.stderr

        else:
          output = 'borked'

        output_bytes = output.encode("utf-8")

        self.send_response(200)
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

