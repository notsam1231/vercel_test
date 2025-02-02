import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Load student marks data
with open('q-vercel-python.json') as f:
    data_list = json.load(f)

# Convert list to dictionary for fast lookup
MARKS_DATA = {entry["name"]: entry["marks"] for entry in data_list}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Parse query parameters correctly
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get('name', [])

        # Fetch marks (ensure all names are checked)
        marks = [MARKS_DATA.get(name, 0) for name in names]

        # Send response in the correct format
        response = json.dumps({"marks": marks})
        self.wfile.write(response.encode())

    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
