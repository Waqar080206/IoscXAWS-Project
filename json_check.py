import json

with open("clean_data.json", "r") as f:
    data = json.load(f)

usernames = [entry["username"] for entry in data]
unique = set(usernames)

print(f"Total entries: {len(data)}")
print(f"Unique usernames: {len(unique)}")
print(f"Duplicates: {len(data) - len(unique)}")