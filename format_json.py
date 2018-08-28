import json

with open("message1.json") as file:
    msg = json.load(file)
    print(msg)