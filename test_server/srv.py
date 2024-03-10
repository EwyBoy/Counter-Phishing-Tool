from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, threading, datetime, os

### This file sets up a test server for use in verifying the logger functionality. It also contains the necessary imports to
# ensure the logger is setup and initialized for the whole program.

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
    # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Get the length of the content
        content_length = int(self.headers['Content-Length'])

        # Read the content data
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Process the received data (replace this with your logic)
        response_data = f"Received data: {post_data}"

        # Write content as utf-8 data
        self.wfile.write(bytes(response_data, 'utf-8'))
        return

def setup_logger():

    log_folder = os.path.join(os.getcwd(), 'logs')

    # Create the logs folder if it doesn't exist
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Configure the logger basic configuration
    instance_start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = os.path.join(log_folder, f'app_{instance_start_time}.log')
    logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create the logger for the main app
    logger = logging.getLogger("main-app")

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

# Set the server address and port
def start_test_server():
    setup_logger()
    host = 'localhost'
    port = 25565

    # Create an instance of the HTTP server with the custom request handler
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)

    print(f"Server started on {host}:{port}")

    # Keep the server running
    httpd.serve_forever()
    

if __name__ == "__main__":
    start_test_server()
