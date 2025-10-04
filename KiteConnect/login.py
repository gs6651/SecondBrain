from kiteconnect import KiteConnect
import webbrowser
import os
import csv
import socketserver
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

# --- 1. CONFIGURATION ---

CONFIG_FILE = "api_secret_key.txt"
GLOBAL_REQUEST_TOKEN = None

# --- Read API Key, Secret, and Redirect URI from file ---
try:
    with open(CONFIG_FILE, 'r') as f:
        # Splits each line at '=' and takes the second part [1], then strips whitespace
        api_key = f.readline().split('=')[1].strip()
        api_secret = f.readline().split('=')[1].strip()

        # Read the third line for the redirect URI
        redirect_line = f.readline().strip()
        if '=' in redirect_line:
            redirect_uri = redirect_line.split('=')[1].strip()
        else:
            redirect_uri = redirect_line

except Exception as e:
    print(f"Error reading config: {e}")
    sys.exit(1)

# Extract Host and Port from REDIRECT_URI
try:
    parsed_uri = urllib.parse.urlparse(redirect_uri)
    REDIRECT_HOST = parsed_uri.hostname

    # Check if port is available
    REDIRECT_PORT = parsed_uri.port
    if REDIRECT_PORT is None:
        raise ValueError("Port missing from REDIRECT_URI.")

except ValueError as e:
    print(f"\n❌ CONFIGURATION ERROR: {e}")
    print(f"Please check your '{CONFIG_FILE}' file.")
    print("The REDIRECT_URI must be fully specified, e.g., 'http://127.0.0.1:5000/auth'")
    sys.exit(1)
except Exception as e:
    print("Error: Ensure REDIRECT_URI is in the format http://127.0.0.1:PORT/PATH")
    print(f"Details: {e}")
    sys.exit(1)

# Initialize KiteConnect client
kite = KiteConnect(api_key=api_key)

# -----------------------------------------------------------------------------
# --- 2. AUTOMATED TOKEN CAPTURE CLASS (Built-in modules only) ---
# -----------------------------------------------------------------------------

class AuthHandler(BaseHTTPRequestHandler):
    """Custom handler to capture the request_token from the redirected URL."""

    def do_GET(self):
        global GLOBAL_REQUEST_TOKEN

        # 1. Parse the path to get the query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        # 2. Extract the 'request_token'
        token = query_params.get('request_token', [None])[0]

        if token:
            GLOBAL_REQUEST_TOKEN = token
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # 3. Send a confirmation message to the browser
            self.wfile.write(b'<h1>Authentication Successful!</h1>')
            self.wfile.write(b'<p>Token captured automatically. You can close this window.</p>')

            # 4. Shut down the server thread
            self.server.shutdown()

        else:
            self.send_error(400, 'Error: request_token not found in URL. Check Kite Connect settings.')

# -----------------------------------------------------------------------------
# --- 3. MAIN EXECUTION FLOW ---
# -----------------------------------------------------------------------------

def automated_login_and_fetch():
    """Manages the full automated login and data fetch process."""
    global GLOBAL_REQUEST_TOKEN

    # --- Generate and open login URL ---
    login_url = kite.login_url()
    print("\n--- STAGE 1: AUTOMATED LOGIN FLOW ---")
    print(f"1. Opening browser. Please complete the login and TOTP:\n{login_url}")
    webbrowser.open_new(login_url)

    # --- Start the temporary server to capture the token ---
    try:
        # Use ThreadingTCPServer to be slightly more robust, though TCPServer should suffice
        server_class = socketserver.TCPServer
        httpd = server_class((REDIRECT_HOST, REDIRECT_PORT), AuthHandler)
        print(f"2. Waiting for Zerodha redirect to {REDIRECT_HOST}:{REDIRECT_PORT}...")

        # The script blocks here until the browser hits the AuthHandler and it calls httpd.shutdown()
        httpd.serve_forever()

    except OSError as e:
        print(f"\n❌ ERROR: Could not start the server on {REDIRECT_HOST}:{REDIRECT_PORT}.")
        print("Please check if another application is using that port, or verify your REDIRECT_URI.")
        print("Error details:", e)
        return False
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during server operation: {e}")
        return False

    print("✅ Token captured automatically. Shutting down server...")

    # --- Generate access_token ---
    if GLOBAL_REQUEST_TOKEN:
        try:
            print("\n--- STAGE 2: GENERATING ACCESS TOKEN & FETCHING DATA ---")

            # Exchange the request token for a persistent access token
            data = kite.generate_session(GLOBAL_REQUEST_TOKEN, api_secret=api_secret)
            access_token = data["access_token"]

            # --- Save the access_token for future use (optional) ---
            with open("access_token.txt", "w") as f:
                f.write(access_token)
            print("Access token generated and saved to access_token.txt")

            # --- Set the access_token and get holdings ---
            kite.set_access_token(access_token)
            holdings = kite.holdings()

            # --- Print Holdings ---
            print("\n--- Your Holdings ---")
            if holdings:
                for holding in holdings:
                    print(f"Symbol: {holding['tradingsymbol']}, Qty: {holding['quantity']}, Avg: {holding['average_price']:.2f}, LTP: {holding['last_price']:.2f}")
            else:
                print("You have no holdings.")

            # --- Save to CSV ---
            CSV_FILE_NAME = "my_holdings.csv"
            if holdings:
                fieldnames = ['tradingsymbol', 'quantity', 'average_price', 'last_price', 'pnl']
                with open(CSV_FILE_NAME, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for holding in holdings:
                        writer.writerow({k: holding.get(k) for k in fieldnames})
                print(f"\n✅ Holdings successfully saved to **{CSV_FILE_NAME}**")

        except Exception as e:
            print(f"\n❌ An error occurred during token exchange or data fetching: {e}")

    return True

if __name__ == "__main__":
    automated_login_and_fetch()
