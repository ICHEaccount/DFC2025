import os
import json
from datetime import datetime

# Path to the JSON file
json_path = "prompts.json"



# Load the JSON data
with open(json_path, "r", encoding="utf-8") as json_file:
    prompts_data = json.load(json_file)
    result = []
    for item in prompts_data:
        timestamp = datetime.fromtimestamp(item["unixMs"] / 1000.0)  # ms → s 변환
        result.append({
            "timestamp": timestamp.isoformat(),   # ISO8601 문자열
            "type": item["type"],
            "text": item["textDescription"]
        })

# Sort by timestamp
result_sorted = sorted(result, key=lambda x: x["timestamp"])

# Load timeline.json 
if os.path.exists("timeline.json"):
    with open("timeline.json", "r", encoding="utf-8") as f:
        try:
            timeline = json.load(f)
        except json.JSONDecodeError:
            timeline = []
else:
    timeline = []

# Append new entries
timeline.extend(result_sorted)

# Save to timeline.json
with open("timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, indent=4, ensure_ascii=False)
