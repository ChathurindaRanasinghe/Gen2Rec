import json

import requests

response = requests.post("https://noteb.com/api/webservice.php", data={"apikey": "112233aabbcc",
                                                                       "method": "list_models",
                                                                       "param[model_id]": ""})

parsed_data = response.json()

id_list = [model["id"] for key in parsed_data["result"] for model in parsed_data["result"][key]["model_info"]]

data = []
for i in id_list:
    details = requests.post("https://noteb.com/api/webservice.php", data={"apikey": "112233aabbcc",
                                                                          "method": "get_model_info",
                                                                          "param[model_id]": i})
    parsed_details = details.json()
    if parsed_details.get("result") and len(parsed_details["result"]) > 0:
        data.append(parsed_details["result"]["0"])

json_file_path = "data/collected_data.json"

with open(json_file_path, "w") as json_file:
    json.dump(data, json_file)
