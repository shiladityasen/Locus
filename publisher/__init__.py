from flask import Flask, render_template, request
from models import Advertisement
import requests
import json
app = Flask(__name__)

lookupaddr = 'http://0.0.0.0:5000'
kafkadrr = 'http://169.234.64.97:5000/publish/'

@app.route('/')
@app.route('/publish/', methods=['GET', 'POST'])
def publish():
    app.logger.debug(request.method)
    if request.method == 'GET':
        latitude = request.args.get('lat')
        longitude = request.args.get('lon')


        # request for list of available topics
        r = requests.get(lookupaddr+'/topiclist')
        topiclist = json.loads(r.content)
        # for topic in topiclist:
        #     app.logger.debug("Topic: " + str(topic))

        return render_template('publish-ad.html', topiclist=topiclist)
    else:
        selectedtopics = request.form.getlist('adcat')
        adcontent = request.form['content']


        latitude = request.args.get('lat')
        longitude = request.args.get('lon')
        print latitude
        print longitude


        # request for region of the advertiser
        r = requests.get(lookupaddr+'/region?lat='+str(latitude)+'&lon='+str(longitude))
        publishregion = json.loads(r.content)
        publishregion = publishregion['name']
        app.logger.debug("Region of publisher: " + str(publishregion))

        # app.logger.debug("Ad content: " + str(adcontent))
        # for topic in selectedtopics:
        #     app.logger.debug("Topic: " + topic)


        selectedtopics = [topic + '_' + str(publishregion) for topic in selectedtopics]
        app.logger.debug(selectedtopics)
        ad = Advertisement(selectedtopics, adcontent)

        app.logger.debug(json.dumps(ad.__dict__))

        r = requests.post(kafkadrr, json=json.dumps(ad.__dict__))
        return r.content
        #return "published"


if __name__ == '__main__':
    app.debug=True
    app.run(host="0.0.0.0", port=5100)
