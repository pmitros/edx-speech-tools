from django.shortcuts import render
from django.http import HttpResponse
import json
import os
import requests
from utilities import format_access

def index(request):
	"""Send back the Bluemix username and password in JSON format."""
	return format_access(HttpResponse(json.JSONEncoder().encode({"username": "391a148f-6273-4a76-a90c-54a8a67a773c", "password": "huQm9X34vL8b"})))

def token(request):
	"""Send back a username, password, and token string that the client app can use to authenticate a socket for live transcription."""
	url = "https://stream.watsonplatform.net/authorization/api/v1/token?url=" + "https://stream.watsonplatform.net/speech-to-text/api"
	mytoken = requests.Session().request('GET', url, auth=("391a148f-6273-4a76-a90c-54a8a67a773c", "huQm9X34vL8b"))
	return format_access(HttpResponse(json.dumps({"username": "391a148f-6273-4a76-a90c-54a8a67a773c", "password": "huQm9X34vL8b", "token": mytoken.text})))
