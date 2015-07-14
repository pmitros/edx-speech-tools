from django.shortcuts import render
from django.http import HttpResponse
import py_s2t
import json
import urllib2
from utilities import format_access

def index(request):
	'''Transcribes the audio provided by the 's' parameter. The server must be able to access the file at the URL, so it cannot be a local blob.'''
	
	sample = request.GET.get('s', 'None')
	if sample == 'None':
		return format_access(HttpResponse("One or more arguments was not provided.", status=400))
	return_text = ""
	speechToText = py_s2t.SpeechToTextService()

	try:
		audio = urllib2.urlopen(sample)
	except Exception as e:
		return_text = "Error loading speech file: %r " % e
		return format_access(HttpResponse(return_text, status=400))

	response = speechToText.s2t(audio.read())
	audio.close()

	try:
		return_text = json.JSONEncoder().encode(response.json())
		print return_text
		return format_access(HttpResponse(return_text))
	except:
		return format_access(HttpResponse("Well, recognizing was successful, but I have no idea what the words are."))
