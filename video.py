import pickle
from moviepy.editor import *

class TimeStamp:
  def __init__(self, start, end):
    self.start = [start]
    self.end = [end]
  def append(self, start, end):
    self.start.append(start)
    self.end.append(end)

def main():
  videos = {}
  path = "./videos"

  for filename in os.listdir(path):
    f = VideoFileClip(filename)
    print(filename)
  words = pickle.load(open("save.p", "rb"))
  text = input("Enter Obama's speech: ")
  text.split(" ")
  for word in text:
    if(text[word]):
      text[word]
      
main()