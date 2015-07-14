'''Use this file to adjust the URLs that are allowed to access speech2text, bluemix_auth, etc.'''

def format_access(res):
	res["Access-Control-Allow-Origin"] = "http://localhost:63342" #"http://richreview-speech2text.mybluemix.net"
	return res