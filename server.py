import http.server
import socketserver
import sqlite3
import json

# Define the handler for the HTTP requests


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        endpoint = data.get("endpoint")

        if endpoint == "insert_image":
            response = self.insert_image(data)
        elif endpoint == "insert_student":
            response = self.insert_student(data)
        else:
            response = {
                "status": "error",
                "message": "Invalid endpoint"
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def insert_image(self, data):
        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            student_id = data.get("student_id")
            student_idcard = data.get("student_idcard")
            student_image = data.get("student_image")
            student_selfie = data.get("student_selfie")
            mega_idcard = data.get("mega_idcard")
            mega_image = data.get("mega_image")
            mega_selfie = data.get("mega_selfie")
            code = data.get("code")
            jjson = data.get("json")

            cursor.execute("INSERT INTO images (student_id, student_idcard, student_image, student_selfie, mega_student_idcard, mega_student_image, mega_student_selfie, json, code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (student_id, student_idcard, student_image, student_selfie, mega_idcard, mega_image, mega_selfie, jjson, code))
            conn.commit()

            response = {
                "status": "success",
                "message": "Data inserted into images table successfully"
            }
        except Exception as e:
            response = {
                "status": "error",
                "message": str(e)
            }
        finally:
            cursor.close()
            conn.close()

        return response

    def insert_student(self, data):
        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            student_id = data.get("student_id")
            student_name = data.get("student_name")

            cursor.execute("INSERT INTO student (student_id, student_name) VALUES (?, ?)",
                           (student_id, student_name))
            conn.commit()

            response = {
                "status": "success",
                "message": "Data inserted into student table successfully"
            }
        except Exception as e:
            response = {
                "status": "error",
                "message": str(e)
            }
        finally:
            cursor.close()
            conn.close()

        return response


# Create an HTTP server
PORT = 8000
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
