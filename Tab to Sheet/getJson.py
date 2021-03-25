from urllib.request import urlopen
import json

def songsterrSearch():

    #search_logger = tabLogger.setup_logger('search_logger', 'debug_logfile.log')
    
    URL = ""
    #URL = "https://www.songsterr.com/a/wsa/the-strokes-you-only-live-once-bass-tab-s1384t2"
    #URL = "https://www.songsterr.com/a/wsa/the-smiths-this-charming-man-bass-tab-s17973t5"
    #URL = "https://www.songsterr.com/a/wsa/jojos-bizarre-adventure-golden-wind-giornos-theme-bass-tab-s456145t2"

    songsterrURLBestMatch = "http://www.songsterr.com/a/wa/bestMatchForQueryString?inst=bass&s={song title}&a={artist name}"

    searchOption = int( input("1: Search by artist and Song \n2: Search by URL \n") )

    if(searchOption == 1):
        artist = input("Enter Artist Name \n").replace(" ","+")
        song_name = input("Enter Song Name: \n").replace(" ","+")

        #search_logger.info("Artist: " + artist)
        #search_logger.info("Song: " + song_name)
        
        songsterrURLBestMatch = songsterrURLBestMatch.replace( "{artist name}" , artist )
        songsterrURLBestMatch = songsterrURLBestMatch.replace( "{song title}" , song_name )
        URL = songsterrURLBestMatch
    elif(searchOption == 2):
        URL = input("Enter Songterr URL: \n")
    else:
        print("No option found")
    
    return URL

def getSongSterrJson():

    URL = songsterrSearch()
    #debug_logger.info("URL: " + URL)
    response = urlopen(URL)

    string = response.read().decode('cp1252')

    jsonString = ""
    for line in string.splitlines():
        isTabLine = line.find("application/json")
        if isTabLine >= 0 :
            jsonString = line.split(">")[1].split("<")[0] #strip off <script> tags
            break #found json move on to parsing it

    json_tab = json.loads(jsonString)

    return json_tab