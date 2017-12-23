from http.server import *
from urllib.parse import urlparse
import Search
import Preprocessing
import Spell

HOST = ''
PORT = 8080
server = (HOST, PORT)

def make_list(s):
	return '<li>%s</li>\n' % s


class BallHandler(BaseHTTPRequestHandler):
	def success(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_GET(self):
		if self.path == '/':
			self.success()
			with open('base.html') as fp:
				page = fp.read()
				self.wfile.write(page.encode())

		elif self.path.startswith('/?search='):
			self.success()
			query = urlparse(self.path).query[7:]
			with open('base.html') as fp:
				page = fp.read().split('<!--##PEWPEW##-->')
				self.wfile.write(page[0].encode())
				self.wfile.write(b'<ul>\n\n')
				query = query.replace('+',' ')
				# Processing query
				results = Search.search(query)
				if not results:
					sw = Spell.SearchWord()
					words = Preprocessing.Clean(query)
					spelled = []
					for word in words:
						spelled.append(sw.spell(word))
					for document in spelled[0]:
						self.wfile.write(make_list(document).encode())
				else:
					for r in results:
						list = results[r]
						for document in list:
							self.wfile.write(make_list(document).encode())

				# End processing
				self.wfile.write(b'\n</ul>\n')
				self.wfile.write(page[1].encode())


try:
	s = HTTPServer((HOST, PORT), BallHandler)
	s.serve_forever()
except KeyboardInterrupt:
	print('\b\bByebye ;)')
