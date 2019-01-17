from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import csv
import json
import pyexcel


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.headers['Content-Length']:
			content_length = int(self.headers['Content-Length'])
			body = self.rfile.read(content_length)
			response = BytesIO()
			response.write(body)
			id = body.decode()
		else:
			id = None

		self.send_response(200)
		self.end_headers()
		self.wfile.write(fromcsv(id=id))
	
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(body)
		tocsv(body.decode())
		self.wfile.write(b'Created the record')

	def do_PUT(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(body)
		st = body.decode()
		id, data = evaluate(st)
		deletefromcsv(data, id = id)
		tocsv(data, id=id)
		self.wfile.write(b'Upated the record')

	def do_DELETE(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(body)
		deletefromcsv(body.decode())
		self.wfile.write(b'Deleted the record')

def evaluate(data):
	dt = data.split('&')
	id = dt[0].split('=')[1]
	dat = dt[1].split('=')[1].replace('+',' ')
	return (id, dat)

def fromcsv(id = None):
	with open('data.csv') as csvfile:
		reader = csv.reader(csvfile)
		data = {}
		for row in reader:
			k, v = row
			if id and str(id) == str(k):
				data = {id : v}
				break
			else:
				data[k] = v
		dt = json.dumps(data)
		return str(dt).encode()

def tocsv(data,id=None):
	if not id:
		with open('data.csv', 'r') as f:
			id = len(f.readlines())

	with open(r'data.csv', 'a', newline='\n') as csvfile:
		fieldnames = ['ID', 'String']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow({'ID':id,'String':data})	

def deletefromcsv(data, id = None):
	fr = open('data.csv', 'r')
	dr = csv.reader(fr)
	ls = []
	for row in dr:
		if row[1] != data and id != row[0]:
			ls.append(row)
	fr.close()
	pyexcel.save_as(array = ls, dest_file_name = 'data.csv')


if __name__ == "__main__":
	httpd = HTTPServer(('localhost', 80), SimpleHTTPRequestHandler)
	print("Started HTTP server on loclahost port 80")
	httpd.serve_forever()
#	deletefromcsv('bye raja')
#	print(fromcsv(2))
