from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

FILE_PATH = "received_updates.json"

# Ensure the file exists before writing
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as file:
        json.dump([], file)  # Initialize with an empty JSON array

@app.route('/receive_from_mobile', methods=['POST'])
def receive_from_mobile():
    print("\n📩 Incoming request received at Fog Node...")  # Debugging log
    try:
        data = request.get_json()
        
        # Check if request body is empty
        if not data:
            print("❌ Error: Request body is empty or not valid JSON.")
            return jsonify({"error": "Invalid JSON format"}), 400
        
        print("🔹 Received data:", data)  # Log received data
        
        encrypted_weights = data.get("encrypted_weights")
        if not encrypted_weights:
            print("❌ No encrypted data received.")
            return jsonify({"error": "No encrypted data received"}), 400
        
        print("\n✅ Successfully received encrypted model update.")

        # Save to JSON file
        with open(FILE_PATH, "r+", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)  # Load existing data
            except json.JSONDecodeError:
                existing_data = []  # Reset if file is empty or corrupt

            existing_data.append({"encrypted_weights": encrypted_weights})  # Append new data

            file.seek(0)  # Move pointer to the beginning
            json.dump(existing_data, file, indent=4)  # Write updated data
            file.truncate()  # Remove leftover characters if overwriting

        print(f"✅ Data saved in '{FILE_PATH}'")

        return jsonify({"message": "Model update received successfully"}), 200

    except Exception as e:
        print(f"❌ Error in processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
 # Enable debug mode





