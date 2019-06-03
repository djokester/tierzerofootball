from bs4 import BeautifulSoup
import re
from urllib.parse import urlsplit
import requests
from flask_cors import CORS
import flask
from datetime import datetime
import json

app = flask.Flask(__name__)
CORS(app)


@app.route("/predict", methods=["POST"])
def predict():
    sources = ["henrywinter", "simon-stone", "fabrizio-romano", "paul-joyce", "david-ornstein", "kristof-terreur", "simon-peach"]
    jsonfinal = []
    for source in sources:
      r = requests.get("https://muckrack.com/"+source+"/articles")
      soup = BeautifulSoup(r.content)
      count = 0
      for tags in soup.find_all('div', class_ ="news-story"):
        content = {}
        print(count)
        print(tags.find("h4").text)
        body = (tags.find("div", class_ = "news-story-body").text.split("—"))
        author = (body[0].lstrip().rstrip().split("\n")[0])
        source = (body[0].lstrip().rstrip().split("\n")[1])
        body = body[1].lstrip().rstrip()
        time = tags.find("a", class_ = "timeago").text.lstrip().rstrip()
        link = tags.find("a").get("href")
        content["head"] = tags.find("h4").text
        content["body"] = body
        content["author"] = author
        content["source"] = source
        content["time"] = time
        content["link"] = link
        print(time)
        jsonfinal.append(content)
        count+=1
    json.dumps(jsonfinal)
    with open("output.json", "w") as f:
        json.dump(jsonfinal, f)
    return flask.jsonify(jsonfinal)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 3030)
