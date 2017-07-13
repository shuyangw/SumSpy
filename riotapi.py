import riotconstants as riot
import parsesummoner as ps
import requests

class RiotAPI(object):
	def __init__(self, api_key, region=riot.REGIONS['na']):
		self.api_key = api_key
		self.region = region

	def _request(self, api_url, v3, params={}):
		args = {'api_key': self.api_key}
		for key, value in params.items():
			if key not in args:
				args[key] = value

		if v3 == False:
			response = requests.get(
				riot.URL['base'].format(
					proxy=self.region,
					region=self.region,
					url=api_url
					),
				params=args
				)
		else:
			response = requests.get(
				riot.URL['base_v3'].format(
					proxy=riot.REGIONS["na_v3"],
					url=api_url
					),
				params=args
				)
		
		return response.json()

	#Collects the Summoner ID, Profile Icon ID, Revision Date, Summoner Level
	#given the name of a summoner	
	def get_summoner_by_name(self, name):
		api_url = riot.URL['summoner_by_name'].format(
			version=riot.API_VERSIONS['summoner'],
			names=name
			)

		return self._request(api_url, False)

	#Collects the Summoner ID, Profile Icon ID, Revision Date, Summoner Level
	#given the id of a summoner provided by get_summoner_by_name
	def get_summoner_by_id(self, id):
		api_url = riot.URL['summoner_by_id'].format(
			version=riot.API_VERSIONS['summoner'],
			id=id
			)

		return self._request(api_url, False)

	#Returns the ranked stats containing information on individual champions given
	#the id of a summoner 
	def get_stats(self, id):
		api_url = riot.URL['get_stats'].format(
			version=riot.API_VERSIONS['ranked'],
			id=id
			)

		return self._request(api_url, False)

	def get_current_match_info(self, summoner_id):
		api_url = riot.URL['get_curr_game'].format(
			version=riot.API_VERSIONS['spectator'],
			summonerId = summoner_id
			)

		return self._request(api_url, True)

	def get_league_info(self, summonerId):
		api_url = riot.URL['get_ranked_stats'].format(
			version=riot.API_VERSIONS['leagues'],
			summonerId=summonerId
			)
		return self._request(api_url, True)

	#Returns the ranked stats containing information on individual champions given
	#the name of a summoner
	def get_stats_by_name(self, name):
		sum_id = self.extr_id_from_name(name)
		return self.get_stats(sum_id)

	#Returns a list of dictionaries representing the stats of champions played
	#sorted by games played in descending order
	def get_champion_stats_by_name(self, name):
		champ_data, wr = ps.get_champion_data(self.get_stats_by_name(name)["champions"])
		return champ_data, wr

	#Extracts the summoner id of a summoner given the name of a summoner
	def extr_id_from_name(self, name):
		from_name_pack = self.get_summoner_by_name(name)
		name = list(from_name_pack.keys())[0]
		return from_name_pack[name]["id"]

	def get_match_info_by_name(self, name):
		stats = ps.get_current_match_stats(self.get_current_match_info(self.extr_id_from_name(name)))
		return stats
	
	def get_rank_by_name(self, name):
		stats = self.get_league_info(self.extr_id_from_name(name))[0]
		return stats["tier"]+" "+stats["rank"]