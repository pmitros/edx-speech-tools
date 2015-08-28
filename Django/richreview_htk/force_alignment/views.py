from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import os
import time
import pyforcealign
import shutil
import json
from utilities import format_access

P2FA_DIR = "/Users/venkatesh-sivaraman/p2fa/model"

# Create your views here.
def index(request):
	return format_access(HttpResponse("Hello, word! You're at the force alignment index."))

def forcealign(request):
	sample = request.GET.get('s', 'None')
	transcript = request.GET.get('t', 'None')
	if transcript == 'None' or sample == 'None':
		return format_access(HttpResponse("One or more arguments was not provided.", status=400))
	return_text = ""
	#Create a temporary directory to house our data
	tmppath = "./webtmp/"
	transtmppath = tmppath + "transcript.txt"
	speechtmppath = tmppath + "audio.wav"
	if os.path.exists(tmppath):
		shutil.rmtree(tmppath)
	os.mkdir(tmppath)

	try:
		transfile = urllib2.urlopen(transcript)
	except Exception as e:
		return_text = "Error %r loading transcript file" % e
		return format_access(HttpResponse(return_text))
	else:
		transtext = transfile.read().replace('\xe2\x80\x99', "'")
		with open(transtmppath, "w") as f:
			f.write(transtext)
		print sample, transtext
		#return_text = "You selected to transcribe the contents of %s with transcription %s: <br/>" % (sample, transtext)
		transfile.close()

	try:
		audio = urllib2.urlopen(sample)
	except Exception as e:
		return_text = "Error %r loading speech file" % e
		return format_access(HttpResponse(return_text))
	else:
		with open(speechtmppath, "wb") as tmpfile:
			tmpfile.write(audio.read())
		audio.close()

	words = pyforcealign.force_align(P2FA_DIR, speechtmppath, transtmppath)
	#Create a JSON string to return
	return_text = json.JSONEncoder().encode([[w.word, w.start, w.end] for w in words])
	shutil.rmtree(tmppath)
	return format_access(HttpResponse(return_text))