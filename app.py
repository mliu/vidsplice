import sqlite3, json, os
from flask import Flask, g, request, render_template
from contextlib import closing
import requests, pdb, re, urllib
from re import findall
import xml.etree.ElementTree as ET

DATABASE = "./tmp/flaskr.db"
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def build_video_func(url):
  words = {}

  # For when you pass in https://www.youtube.com/watch?v=VIDEOID
  # root = findall("=.*&?", url)
  # root = ''.join(root)
  # if "&" in root:
  #   x = root.index("&")
  #   root = root[1:x]
  # else:
  #   root = root[1:]
  request = requests.get("http://video.google.com/timedtext?v=" + url + "&lang=en")
  try:
    request = ET.fromstring(request.content)
    for elem in request:
      # Clean punctuation
      for ch in [',', '.', '!', ';', '?']:
        if ch in elem.text:
          elem.text = elem.text.replace(ch, '')
      for word in elem.text.replace('\n', ' ').split(" "):
        if elem.attrib['start'] + ";" + elem.attrib['dur'] in words:
          words[elem.attrib['start'] + ";" + elem.attrib['dur']].append(word)
        else:
          words[elem.attrib['start'] + ";" + elem.attrib['dur']] = [word]

    return json.dumps(words)
  except:
    return 0

@app.route("/build_video/<video_id>")
def build_video(video_id):
  return render_template('video.html', video_id=video_id, data=build_video_func(video_id))

if __name__ == '__main__':
    app.run()
