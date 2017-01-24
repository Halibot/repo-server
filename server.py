import json
import http.server
import socketserver
from threading import Thread

class RepoHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		args = list(filter(lambda x: len(x) > 0, self.path.split('/')))

		if len(args) >= 1:
			if args[0] == 'fetch':
				path = self.server.repo.tarball_path('/'.join(args[1:]))
				if path != None:
					with open(path, 'rb') as f:
						ball = f.read()
						self.send_response(200)
						self.send_header('Content-Type', 'application/x-compressed')
						self.send_header('Content-Length', int(len(ball)))
						self.end_headers()
						self.wfile.write(ball)
						return
			elif args[0] == 'search':
				if len(args) == 1:
					results = self.server.repo.packages
				else:
					terms = '/'.join(args[1:])
					results = self.server.repo.search(terms)
				data = json.dumps(results).encode()

				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.send_header('Content-Length', int(len(data)))
				self.end_headers()
				self.wfile.write(data)
				return
					
		self.send_error(404)


class RepoServer():

	def __init__(self, repo, port=4842): # 0x4842 = "HB"
		self.port = port
		self.repo = repo
		self.thread = Thread(target=self.run)
		self.thread.start()

	def run(self):
		Handler = RepoHandler
		self.httpd = socketserver.TCPServer(("", self.port), Handler)
		self.httpd.repo = self.repo
		self.httpd.serve_forever()

	def shutdown(self):
		self.httpd.shutdown()
		self.thread.join()

