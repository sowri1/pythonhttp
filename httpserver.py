from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import csv
import json
import pyexcel


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(fromcsv())
	
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(body)
		tocsv(body)
		self.wfile.write(response.getvalue())

	def do_DELETE(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(body,id=id)
		tocsv(body)
		self.wfile.write(response.getvalue())

def fromcsv():
	with open('data.csv') as csvfile:
		reader = csv.reader(csvfile)
		data = {}
		for row in reader:
		   k, v = row
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
		writer.writerow({'ID':id,'String':data.decode()})	

def deletefromcsv(data):
	fr = open('data.csv', 'r')
	dr = csv.reader(fr)
	ls = []
	for row in dr:
		if row[1] != data:
			ls.append(row)
	fr.close()
	pyexcel.save_as(array = ls, dest_file_name = 'data.csv')
	

if __name__ == "__main__":
	"""	httpd = HTTPServer(('localhost', 80), SimpleHTTPRequestHandler)
	print("Started HTTP server on loclahost port 80")
	httpd.serve_forever()"""
	deletefromcsv('hello raja')
#	print(fromcsv())