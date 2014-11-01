import os, time, math, pickle, pdb
from datetime import timedelta, datetime

class TimeStamp:
  def __init__(self, start, end, vid):
    self.start = [start]
    self.end = [end]
    self.vid = [vid]
  def append(self, start, end, vid):
    self.start.append(start)
    self.end.append(end)
    self.vid.append(vid)

def getTimeDiff(start, end, length):
  timeStart = time.strptime("1978 " + start, "%Y %H:%M:%S.%f")
  timeEnd = time.strptime("1978 " + end, "%Y %H:%M:%S.%f")
  timeStart = time.mktime(timeStart)
  timeEnd = time.mktime(timeEnd)
  timeDiff = timeEnd - timeStart
  return timeDiff / length

def main():
  words = {}
  path = './subtitles'

  for filename in os.listdir(path):
    f = open(path + '/' + filename, 'r')
    for line in f:
      if line.rstrip().isdigit():
        timeStr = str.replace(f.readline().rstrip(), ",", ".")
        timeStr = timeStr.split(" ")
        start = timeStr[0]
        if(len(start) == 9):
          start += "00"
        end = timeStr[2]
        if(len(end) == 9):
          end += "00"
        speech = f.readline().rstrip().split(" ")
        length = len(speech)
        timeDiff = getTimeDiff(start, end, length)
        start = datetime.strptime(start, "%H:%M:%S.%f")
        end = datetime.strptime(end, "%H:%M:%S.%f")
        while speech != ['']:
          for index, word in enumerate(speech):
            if word in words:
              words[word].append(start + timedelta(index * timeDiff), start + timedelta((index+1) * timeDiff), filename)
            else:
              words[word] = TimeStamp(start + timedelta(index * timeDiff), start + timedelta((index+1) * timeDiff), filename)
          speech = f.readline().rstrip().split(" ")
          length = len(speech)
  pickle.dump(words, open("save.p", "wb"))
  print("Video subtitles generated!")

main()