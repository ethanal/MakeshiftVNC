import os
import SimpleHTTPServer
import SocketServer
import sys
import tempfile


class ScreenshotRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "index.html")) as f:
                contents = f.read()
                self.send_header("Content-length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
        elif path == "/screen.png":
            screenshot = tempfile.NamedTemporaryFile()
            filename = screenshot.name
            screenshot.close()
            os.system("/usr/sbin/screencapture -x -t png {}".format(filename))
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            with open(filename, "rb") as f:
                contents = f.read()
                self.send_header("Content-length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
            os.remove(filename)
        else:
            self.send_response(404)


port = 8080
if len(sys.argv) == 2 and sys.argv[1].isdigit():
    port = int(sys.argv[1])

handler = ScreenshotRequestHandler
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", port), handler)

print("Serving on port {}".format(port))

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Exiting")
    httpd.shutdown()
    sys.exit(0)
