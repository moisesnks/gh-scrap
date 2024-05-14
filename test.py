import json

# Read participants from JSON file
with open('input/participantes.json', 'r') as f:
    participants = json.load(f)

# Assign unique keys to each participant
for i, participant in enumerate(participants):
    participant['key'] = i

# Write updated participants back to JSON file
with open('output/participantes_with_keys.json', 'w') as f:
    json.dump(participants, f, indent=4, ensure_ascii=False)

print("Unique keys assigned and saved to output/participantes_with_keys.json")
