from kiteconnect import KiteConnect
import webbrowser
import os
import csv # <-- ADD THIS LINE

# ... (API Key, Secret, Redirect URI reading logic remains the same) ...
try:
    with open("api_secret_key.txt", 'r') as f:
        # Splits each line at '=' and takes the second part [1], then strips whitespace
        api_key = f.readline().split('=')[1].strip()
        api_secret = f.readline().split('=')[1].strip()

        # Read the third line for the redirect URI
        redirect_line = f.readline().strip()
        # Check if the line contains '=', if so, parse it, otherwise use the whole line
        if '=' in redirect_line:
            redirect_uri = redirect_line.split('=')[1].strip()
        else:
            redirect_uri = redirect_line

except FileNotFoundError:
    print("Error: 'api_secret_key.txt' not found.")
    exit()
except IndexError:
    print("Error: Check the format in 'api_secret_key.txt'. It should be 'KEY = VALUE'.")
    exit()

# --- Initialize KiteConnect client ---
kite = KiteConnect(api_key=api_key)

# --- Generate and open login URL ---
login_url = kite.login_url()
print(f"Please login here: {login_url}")
webbrowser.open_new(login_url)

# --- Get request_token from the redirect URL ---
request_token = input("Enter the request_token from the redirect URL: ")

# --- Generate access_token ---
try:
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]

    # --- Save the access_token for future use (optional) ---
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    print("Access token generated and saved to access_token.txt")

    # --- Set the access_token and get holdings ---
    kite.set_access_token(access_token)
    holdings = kite.holdings()

    print("\n--- Your Holdings ---")
    if holdings:
        for holding in holdings:
            print(f"Symbol: {holding['tradingsymbol']}, Qty: {holding['quantity']}, Avg: {holding['average_price']:.2f}, LTP: {holding['last_price']:.2f}")
    else:
        print("You have no holdings.")

    # =========================================================================
    # --- ADD THIS SECTION TO SAVE HOLDINGS TO CSV ---

    CSV_FILE_NAME = "my_holdings.csv"

    if holdings:
        # Define the column headers for the CSV file
        fieldnames = ['tradingsymbol', 'quantity', 'average_price', 'last_price', 'pnl']

        with open(CSV_FILE_NAME, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write the data rows
            for holding in holdings:
                # Use writerow with only the keys we need
                writer.writerow({
                    'tradingsymbol': holding.get('tradingsymbol'),
                    'quantity': holding.get('quantity'),
                    'average_price': holding.get('average_price'),
                    'last_price': holding.get('last_price'),
                    'pnl': holding.get('pnl') # Profit & Loss field
                })

        print(f"\n✅ Holdings successfully saved to **{CSV_FILE_NAME}**")

    # =========================================================================

except Exception as e:
    print(f"An error occurred: {e}")
