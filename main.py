from riotapi import RiotAPI
import parsesummoner as ps
import riotconstants as riot

import sys

SHWANGCAT_ID = "35370803"
SHWANGCAT_NAME = "ShwangCat"

DANA_NAME = "Chocolatê"
MERU_NAME = "Kïll Ëm Sôftly"

def debug_suite():
	api = RiotAPI(riot.API["key"])
	ps.setup(api)
	# response_fromid = api.get_stats(SHWANGCAT_ID)


	response = api.get_match_info_by_name("ShwangCat")
	print(ps._tojson_beautify_json(response))		

	# champ_data, wr = ps.get_champion_data(api.get_stats_by_name(SHWANGCAT_NAME)["champions"])
	# champ_data, wr = api.get_champion_stats_by_name(SHWANGCAT_NAME)

	# print("Summoner: "+SHWANGCAT_NAME)
	# print(ps._tojson_beautify_json(champ_data))



def main():
	print("WARNING: BE SURE TO UPDATE CODE TO ACCOUNT FOR DEPRECATED API BEFORE 7/24/2017")

	if len(sys.argv) == 2 and sys.argv[1] == "d":
		debug_suite()

if __name__ == "__main__":
	main()