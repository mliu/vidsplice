import pickle, os, random, datetime, pdb
from  moviepy.editor import *

class TimeStamp:
  def __init__(self, start, end):
    self.start = [start]
    self.end = [end]
  def append(self, start, end):
    self.start.append(start)
    self.end.append(end)

def main():
  videos = {}
  clips = []
  path = "./videos"

  for filename in os.listdir(path):
    f = VideoFileClip(path + "/" + filename)
    videos[filename] = f
  words = pickle.load(open("save.p", "rb"))
  text = input("Enter Obama's speech: ").rstrip()
  text = text.split(" ")
  print(text)
  for word in text:
    if word in words:
      el = random.randint(0, len(words[word].vid) -1)
      print(el)
      print(word)
      print(words[word].vid)
      video = videos[words[word].vid[el] + "mp4"]
      clip = video.subclip(words[word].start[el].strftime("%H:%M:%S.%f"), words[word].end[el].strftime("%H:%M:%S.%f"))
      clips.append(clip)
  concatenate_videoclips(clips).write_videofile("ObamaSays.avi", codec='mpeg4')
  print("Obama has spoken!")

main()