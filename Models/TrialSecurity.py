from Models.JsonDecode import key_json

# create a separate folder for Json.
keys = key_json("Details.json") #mention JSON file path in the method call
Json_Key = keys['columns']
print(Json_Key)