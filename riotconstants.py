URL = {
	'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
	'base_v3': 'https://{proxy}.api.riotgames.com/lol/{url}',

	#Gets summoner by name
	'summoner_by_name': 'v{version}/summoner/by-name/{names}',

	#Gets summoner by id
	'summoner_by_id': 'v{version}/summoner/{id}',

	#Gets ranked stats of summoner by id of champions played
	'get_stats': 'v{version}/stats/by-summoner/{id}/ranked',

	#Gets information of current game of a summoner by id
	'get_curr_game': 'spectator/v{version}/active-games/by-summoner/{summonerId}',

	'get_ranked_stats': 'league/v{version}/positions/by-summoner/{summonerId}'
}

API_VERSIONS = {
	'summoner': '1.4',
	'ranked': '1.3',
	'spectator': '3',
	'leagues': '3'
}

REGIONS = {
	'na': 'na',
	'na_v3': 'na1'
}

API = {
	'key': 'RGAPI-b71ee3e1-4bec-4ab6-afa2-5b9a08b86431'
}