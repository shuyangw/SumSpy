import json as json
import os
import riotconstants as riot

API_OBJECT = None

def setup(api):
	global API_OBJECT
	API_OBJECT = api

#Warning, input json_arr must be the data under 'champions' from the response json package
#Given the json of champion data, this returns a list of dictionaries representing the statistics
#of the champions played in ranked and is then sorted in descending order by number of games played
def get_champion_data(json_arr): #json_arr is of type list
	#Extracts the summoner's stats on a champion by the champion id
	def _extract_stats_by_id(id):
		for val in json_arr:
			if int(val["id"]) == id:
				return val["stats"]
		return None

	#Calculates the overall winrate of a summoner given the champion section of the json
	def _calc_overall_winrate(json_arr):
		#Loops through each champion until we reach the summary json entry indicated by an id of 0
		for val in json_arr:
			if int(val["id"]) == 0:
				#Performs the win rate calculation
				wr_actual = (val["stats"]["totalSessionsWon"]/val["stats"]["totalSessionsPlayed"])
				#Rounds to the nearest hundredth
				return "Overall win rate :"+str("{:.2f}".format(wr_actual))[2:]+"%"
		return None

	curr_wr = _calc_overall_winrate(json_arr)
	packet = {} #Packet to store data of each champion, will be sorted by number of games played
	#Loops through every champion
	for champ_data in json_arr:
		#Current champion ID
		curr_champ_id = champ_data["id"]

		#If we reach the end of the dictionary which represents the end of the champion data
		if curr_champ_id == 0:
			#Sorts the value of the dictionary by the value under the string "Total games played"
			return sorted(packet.items(), key = lambda x: x[1]["Total games played"], reverse = True), curr_wr
		
		#Gets the current champion name
		curr_champ = _get_champion_by_id(curr_champ_id)

		#Gets the stats of the summoner on this specific champion
		curr_champ_stats = _extract_stats_by_id(curr_champ_id)

		#Performs the winrate calculation
		curr_champ_wr = curr_champ_stats["totalSessionsWon"]/curr_champ_stats["totalSessionsPlayed"]
		
		#Performs the kill-death-assist calculation
		kda = (curr_champ_stats["totalChampionKills"]+curr_champ_stats["totalAssists"])/curr_champ_stats["totalDeathsPerSession"]
		
		#Gets the total number of games
		num_total_games = curr_champ_stats["totalSessionsPlayed"]

		#The dictionary that represents the summoner's stats on the current champion
		subpacket = {}
		subpacket["KDA"] = "{:.2f}".format(kda)
		subpacket["Win rate"] = "{:.2f}".format(curr_champ_wr)
		subpacket["Total games played"] = num_total_games

		#Enters the subpacket into the packet that will be sorted and returned
		packet[str(curr_champ)] = subpacket

	#Saftey precaution in case something goes wrong, will still return the packet
	return sorted(packet.items(), key = lambda x: x[1]["Total games played"], reverse = True), curr_wr

#Private class performs a binary searche through the Riot provided JSON which was presorted in ascending order
#by champion id so that we will get the champion name
def _get_champion_by_id(id):
	champion_json = import_champions_json()
	champ_list = list(champion_json.values())
	def _binary_search(id, left, right):
		if right >= 1:
			mid = int((left+right)/2)
			if champ_list[mid][1] == id:
				return champ_list[mid][0]
			elif champ_list[mid][1] > id:
				return _binary_search(id, left, mid-1)
			else:
				return _binary_search(id, mid+1, right)
		return -1
	return _binary_search(id, 0, len(champ_list)-1)

def get_current_match_stats(match_packet):
	players = []
	count = 1
	for player in match_packet["participants"]:
		current_player = player["summonerName"]
		packet = {}
		packet["Name"] = current_player
		packet["Champion"] = _get_champion_by_id(player["championId"])
		packet["Rank"] = get_rank_by_name(current_player)
		if player["teamId"] == 100:
			packet["Team"] = "Blue"
			packet["ID"] = "B"+str(count)
		else:
			packet["Team"] = "Red"
			packet["ID"] = "R"+str(count)
		players.append(packet)
		count += 1
		if count == 6:
			count = 1

	return players
	
#Imports the Riot sorted JSON which represents data on each champion which was presorted by champion ID
def import_champions_json():
	try:
		json_data = json.load(open("riotdata\\sortedchampion.json"))
		return json_data
	except:
		print("Error importing json file")

#Forms a pretty JSON from a dictionary
def _tojson_beautify_json(dict):
	return json.dumps(dict, indent=4)

def get_rank_by_name(name):
	initial_object = API_OBJECT.get_league_info(API_OBJECT.extr_id_from_name(name))
	if len(initial_object) == 0:
		return "Unranked"
	stats = API_OBJECT.get_league_info(API_OBJECT.extr_id_from_name(name))[0]
	return stats["tier"]+" "+stats["rank"]