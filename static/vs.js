var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var highlights = {};

var filler = ['the', 'of', 'and', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us', 'about', 'if', 'my', 'has', 'but', 'our', 'one', 'other', 'do', 'no', 'time', 'they', 'he', 'up', 'may', 'what', 'which', 'their', 'news', 'out', 'use', 'any', 'there', 'see', 'only', 'so', 'his', 'when', 'here', 'who', 'also', 'now', 'am', 'been', 'would', 'how', 'were', 'me', 'these', 'its', 'like', 'than', 'had', 'just', 'them', 'should', 'then', 'well', 'where', 'each', 'does', '(', ')', '', "i'm", "ok", "oh", "--"];

function onPlayerReady(event) {
  event.target.playVideo();
  generateKWElements();
  document.getElementsByTagName("title")[0].innerText = player.getVideoData().title;
}

function onPlayerStateChange(event) {
  
}

function highlightTime(word, timeArr) {
  var timeline = document.getElementById("timeline");
  var times = timeArr.split(",");

  if(word in highlights) {
    for(i = 0; i < highlights[word].length; i++) {
      highlights[word][i].style.visibility = "visible";
    }
  }
  else {
    highlights[word] = [];

    for(i = 0; i < times.length; i++) {
      var highlight = document.createElement("a");
      var vidLength = player.getDuration();
      var start = times[i].substring(0, times[i].indexOf(";") - 1);
      var duration = times[i].substring(times[i].indexOf(";") + 1);
      highlight.style.marginLeft = 100 * start / vidLength + "%";
      highlight.style.width = 100 * duration / vidLength + "%";
      highlight.className = "highlight";
      highlight.dataset.start = start;
      highlight.onclick = function () {
        player.seekTo(this.dataset.start, true);
      }
      timeline.appendChild(highlight);
      highlights[word].push(highlight);
    }
  }
}

function unhighlightTime(word) {
  if(word in highlights) {
    for(i = 0; i < highlights[word].length; i++) {
      highlights[word][i].style.visibility = "hidden";
    }
  }
}

function generateKWElements() {
  var originalData = {};
  var manip = [];
  var container = document.getElementById("container");

  if(data === 0) {
    container.innerHTML = "Sorry, we couldn't extract the subtitles for this video.";
  }

  for(var key in data) {
    for(i = 0; i < data[key].length; i++) {
      if(filler.indexOf(data[key][i].toLowerCase()) > -1) {
        data[key].splice(i, 1);
      }
      else {
        if(originalData[data[key][i]]) {
          originalData[data[key][i]].push(key);
        } else {
          originalData[data[key][i]] = [key];
        }
      }
    }
  }

  for(var key in originalData) {
    var word = originalData[key];
    manip.push({tinfo: originalData[key], word: key });
  }

  manip.sort(function(a, b) {
    return b.tinfo.length - a.tinfo.length;
  });

  for(i = 0; i < manip.length; i++) {
    var node = document.createElement("a");
    // node.data = manip[i].word;
    node.className = "btn btn-default";
    node.innerHTML = manip[i].word + " (" + manip[i].tinfo.length + ")";
    node.dataset.word = manip[i].word;
    node.dataset.time = manip[i].tinfo;
    node.onclick = function () {
      if(this.className.indexOf("active") > -1) {
        unhighlightTime(this.dataset.word);
        this.className = "btn btn-default";
      } else {
        highlightTime(this.dataset.word, this.dataset.time);
        this.className = "btn btn-default active";
      }
    };
    container.appendChild(node);
  }
}

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: video_id,
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}
