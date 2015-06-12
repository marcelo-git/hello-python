import os
import uuid
import urlparse
import redis
import json
import random
import newrelic.agent
newrelic.agent.initialize('./newrelic.ini')
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

def hex_code_colors():
    a = hex(random.randrange(0,256))
    b = hex(random.randrange(0,256))
    c = hex(random.randrange(0,256))
    a = a[2:]
    b = b[2:]
    c = c[2:]
    if len(a)<2:
        a = "0" + a
    if len(b)<2:
        b = "0" + b
    if len(c)<2:
        c = "0" + c
    z = a + b + c
    return "#" + z.upper()

@app.route('/')
def hello():
	r.incr("hit_counter")
	COUNTER = r.get("hit_counter")

	fntcolor = hex_code_colors()
	bkgcolor = hex_code_colors()

	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="{}">Hi, I'm GUID:<br/>
	{}
	</center>
	<center><h1><font color="{}">Number of hits:<br/>
	{}
	</center>

	</body>
	</html>
	""".format(bkgcolor,fntcolor,my_uuid,fntcolor,COUNTER)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
