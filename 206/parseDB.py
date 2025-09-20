import sqlite3
import json

# Path to the .vscdb file
db_path = "state.vscdb"

# Step 1: Connect to the SQLite database
connection = sqlite3.connect(db_path)

# Step 2: Create a cursor object
cursor = connection.cursor()

# Step 3: Query the data from the itemTable table
try:
    cursor.execute("SELECT value FROM itemTable WHERE key = 'aiService.generations'")
    rows = cursor.fetchall()

    # Step 4: Parse the result and write to JSON
    if rows:
        # Extract the JSON string from the first row
        json_data = rows[0][0]
        
        # Parse the JSON string
        parsed_data = json.loads(json_data)
        
        # Write the parsed data to a JSON file
        with open("prompts.json", "w", encoding="utf-8") as json_file:
            json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)
        
        print("Data has been written to prompts.json")
    else:
        print("No data found for the specified key.")

    # Get workspaceOpenedDate
    cursor.execute("SELECT value FROM itemTable WHERE key = 'cursorAuth/workspaceOpenedDate'")
    rows = cursor.fetchall()
    if rows:
        # Extract the JSON string from the first row
        timestamp = rows[0][0]
        
        # Create an JSON object
        parsed_data = [{"timestamp": timestamp, "text": "Workspace opened", "type": "info"}]

        # Write the parsed data to a JSON file
        with open("timeline.json", "w", encoding="utf-8") as json_file:
            json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)

        print("Data has been written to timeline.json")
    else:
        print("No data found for the specified key.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Step 5: Close the connection
connection.close()