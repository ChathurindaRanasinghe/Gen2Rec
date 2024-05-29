import json

import requests


def get_ids() -> list:
    response = requests.post("https://noteb.com/api/webservice.php", data={"apikey": "112233aabbcc",
                                                                           "method": "list_models",
                                                                           "param[model_id]": ""})
    parsed_data = response.json()
    return [model["id"] for key in parsed_data["result"] for model in parsed_data["result"][key]["model_info"]]


def get_data(id_list) -> list:
    data = []
    for i in id_list:
        details = requests.post("https://noteb.com/api/webservice.php", data={"apikey": "112233aabbcc",
                                                                              "method": "get_model_info",
                                                                              "param[model_id]": i})
        parsed_details = details.json()
        if parsed_details.get("result") and len(parsed_details["result"]) > 0:
            print(f"Got data for {i}")
            data.append(parsed_details["result"]["0"])
    return data


def save_to_file(data):
    json_file_path = "data/collected_data.json"

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    id_list = get_ids()
    data = get_data(id_list)
    save_to_file(data)
