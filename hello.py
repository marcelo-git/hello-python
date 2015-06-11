import os
import uuid
import urlparse
import redis
import json
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = BLUE

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
hit_counter = r.get("hit_counter")
if hit_counter < 1:
	
	r.set("hit_counter", 1)

@app.route('/')

def htmlcolor(randcolor):
	def _chkarg(a):
		if isinstance(a, int):
			if a < 0:
				a = 0
			elif a > 255:
				a = 255
		elif isinstance(a, float):
			if a < 0.0:
				a = 0
			elif a > 1.0:
				a = 255
			else:
				a = int(round(a*255))
		else:
			raise ValueError('Arguments must be integers or floats.')
		return a
	randcolor = _chkarg(randcolor)

def hello():
	r.incr("hit_counter")
	COUNTER = r.get("hit_counter")

	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Hi, I'm GUID:<br/>
	{}
	</center>
	<center><h1><font color="white">Number of hits:<br/>
	{}
	</center>

	</body>
	</html>
	""".format(randcolor,my_uuid,COUNTER)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
