import json

with open("DomarenV2/Domaren/relevant_SOU_batch_fix2.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        try:
            json.loads(line)
            print(f"Line {i} is valid JSON.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON on line {i}: {e}")
