import os
import json
import parsesummoner

def extract_id(json):
	try:
		return int(json['data']['key'])
	except:
		print("err")
		return 0

def _tojson_beautify_json(dict):
	return json.dumps(dict, indent=4)

if __name__ == "__main__":
	save_path = os.getcwd()+"\\riotdata"
	complete_name = os.path.join(save_path, "sortedchampion.json")
	file = open(complete_name, "w")
	
	try:
		json_file = json.load(open("riotdata\\champion.json"))
	except:
		print("Error importing json file")

	sorted_json = sorted(json_file["data"], key = lambda x: int(json_file["data"][x]["key"]))
	new_json = [json_file["data"][ip] for ip in sorted_json]
	new_data = {}
	for val in new_json:
		new_data[val["key"]] = [val["name"], int(val["key"])]
	jsondump = _tojson_beautify_json(new_data)
	print(jsondump)
	file.write(jsondump)
	file.close()