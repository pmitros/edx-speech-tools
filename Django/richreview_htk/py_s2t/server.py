#
# Copyright 2014 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

import os
import requests
import json
import urllib2
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

class SpeechToTextService:
	"""Wrapper on the Speech to Text service"""
	
	def s2t(self, audio, sample_rate=22050):
		"""Returns the post HTTP response by sending a POST to
			/v1/recognize with an audio readable stream and the integer sample rate.
			Assumes audio/l16 format.
			"""
		print "Audio:", len(audio)
		return requests.Session().request('POST', self.url + "/v1/recognize", headers={"content-type": "audio/l16; rate=" + str(sample_rate), "timestamps": True, "action": "start"}, data=audio, auth=(self.username, self.password))

	def __init__(self):
		"""
		Construct an instance. Fetches service parameters from VCAP_SERVICES
		runtime variable for Bluemix, or it defaults to local URLs.
		"""
		vcapServices = os.getenv("VCAP_SERVICES")
		# Local variables
		self.url = "https://stream.watsonplatform.net/speech-to-text/api"
		self.username = "381965b7-c938-41e2-9919-7958fec70b83"
		self.password = "O7y1QO5reyRC"

		if vcapServices is not None:
			print("Parsing VCAP_SERVICES")
			services = json.loads(vcapServices)
			svcName = "speech_to_text"
			if svcName in services:
				print("Speech to Text service found!")
				svc = services[svcName][0]["credentials"]
				self.url = svc["url"]
				self.username = svc["username"]
				self.password = svc["password"]
			else:
				print("ERROR: The Speech to Text service was not found")

	def synthesize(self, text, voice, accept):
		"""
		Returns the get HTTP response by doing a GET to
		/v1/synthesize with text, voice, accept
		"""

		return requests.get(self.url + "/v1/synthesize", auth=(self.username, self.password), params={'text': text, 'voice': voice, 'accept': accept}, stream=True, verify=False)


@app.route('/', methods=['GET'])
def index():
    pass

@app.route('/recognize', methods=['GET'])
def recognize():
	sampleurl = request.args.get('audio', 'None')
	print sampleurl
	if sampleurl == 'None':
		abort(500)
	
	audio = urllib2.urlopen(sampleurl)
	try:
		audiodata = audio.read()
		print "audio:", len(audiodata)
		audio.close()
		req = speechToText.s2t(audiodata)
		return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])
	except Exception as e:
		abort(500)

@app.errorhandler(500)
def internal_Server_error(error):
    return 'Error processing the request', 500

# Global watson service wrapper
speechToText = None

if __name__ == "__main__":
    speechToText = SpeechToTextService()

    # Get host/port from the Bluemix environment, or default to local
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))

    app.run(host=HOST_NAME, port=int(PORT_NUMBER), debug=True)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))
