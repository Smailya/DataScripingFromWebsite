import json

input_path = r"C:\Users\ismae\OneDrive\Documents\Salat\Dataset\model_behavior_with_prayer.jsonl"
output_path = r"C:\Users\ismae\OneDrive\Documents\Salat\Dataset\user_responses.jsonl"

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        entry = json.loads(line.strip())

        # Remove the 'output' field if it exists
        entry.pop("output", None)

        # Write only input, tags, and prayer
        outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"✅ Done! Saved as: {output_path}")
