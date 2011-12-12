import os
import logging 
from sqlite3 import *
import time
import pipes
import shutil
from lib.pymediainfo import MediaInfo
from lib.name_parser.parser import NameParser, InvalidNameException
from lib.tvdb_api.tvdb_api import Tvdb
import lib.pyencoder.helper as helper


# depends: ffmpeg, mediainfo CLI, python 2.7
# Author: cytec
# Reencode Specified medias


############### needed infos:
#bitrate audio/video, gesammte end bitrate (ton+video zusammen), audio spuren anzahl, simplejson



# GLOBAL VARS #

#Minimum Video height needed to reencode the files
#anything underneth will be skipped
video_height_need=720

#path to the hofloder which should be scanned for mediafiles
hotfolder="/Volumes/Media/Series/"
#which kind of media files should be processed
media_types = ['.avi','.mkv','.mp4','.wmv', '.mov'] 
#Path to pyEncoder NEEDS ending "/"
pyEncoder="/Users/cytec/pyEncoder/"
#Time to whait bevore next Scan of hotfolder in MINUTES
sleeptime=1
#Possible values: DEBUG, INFO, ERROR
loglevel="DEBUG"

#### VIDEO CONVERT SETTINGS
#Kepp the original file in BACKUP folder values: True, False
keep_source=False
#Size of the new Video File
new_video_size="1280x720"
#Maximum Bitrate of the new Video
vid_max_bitrate=2500000
audio_max_bitrate=320000
#if vid_max_bitrate is over 2500kb/s and an AppleTV compatible one should be created
#Values: True, False
#Video will be named: _appletv.mp4
extra_apple_tv=False


#not yet implemented...
video_bitrate_need=""
audio_bitrate_need=""
audio_codec_need=""



#### Logging functions

logging.basicConfig( 
    filename=pyEncoder + "pyEncoder.log",  
    level = logging.DEBUG, 
    format = "%(asctime)s %(levelname)s: %(message)s", 
    datefmt = "%d.%m.%Y %H:%M:%S") 
    



def test():
    ###connect to sqlite datenbank
    conn = connect(pyEncoder + "pyEncoder.db")
    curs = conn.cursor()
    logging.debug("Connecting to sqlite Database: pyEncoder.db")
    os.chdir(hotfolder) #go to folder
    dir_content=os.listdir(hotfolder) #get content of folder
    logging.debug("Scanning " + hotfolder + " for MediaFiles")
    for datei in dir_content:
        filename, extension = os.path.splitext(datei)
        if os.path.isdir(datei) == True:
            logging.debug(datei + "is a Directory... skipping it")
        elif (extension in media_types):
            logging.debug("Filename for " + datei + " is " + filename)
            logging.debug("Extension for " + datei + " is " + extension)
            moved=False
            ##### GER SERIES NAME AND STUFF...
            
            logging.info("Getting tvdb infos for " + datei)
            tp = NameParser()
            parse_result = tp.parse(datei)
            logging.debug("Parsing Showname..." + str(parse_result))

            
            # print parse_result.series_name
            # print parse_result.extra_info
            #print parse_result.season_number
            # print parse_result.episode_numbers
            #             print parse_result.release_group
            
            sname = parse_result.series_name
            snumber = parse_result.season_number
            if (snumber == None): 
                snumber=01
                logging.error("Not able to find a Season Number in Name... trying Season 01...")
            ep = parse_result.episode_numbers[0]
            
            logging.debug("Starting TVDB.com Scan with Values for " + datei + ": Name: " + sname + ", Season: " + str(snumber) + ", Episode: " + str(ep))
            t = Tvdb(language="de")
            
            #t[name].data.keys()
            #>>> t[name]['id']
            #u'75760'
            #define value for series
            series = t[sname]
            tvdbid = series['id']
            network = series['network']
            genre = series['genre']

            tvdbget = series[snumber][ep]
            
            #>>> t[name][season][ep[0]].keys()
            #['episodenumber', 'rating', 'overview', 'dvd_episodenumber', 'dvd_discid', 'combined_episodenumber', 'epimgflag', 'id', 'seasonid', 'seasonnumber', 'writer', 'lastupdated', 'filename', 'absolute_number', 'ratingcount', 'combined_season', 'imdb_id', 'director', 'dvd_chapter', 'dvd_season', 'gueststars', 'seriesid', 'language', 'productioncode', 'firstaired', 'episodename']

            epname = tvdbget['episodename']
            overview = tvdbget['overview']
            rating = tvdbget['rating']
            epid = tvdbget['id']
            #overview = overview.encode('ascii', 'replace')

            logging.debug("TVDB.com Values: ID: " + tvdbid + ", Network: " + network + ", EpisodeName: " + epname + ", Overview: " + overview + ", Rating: " + rating + ", epID: " + epid)
            #print sname, snumber, ep, epname, overview, rating
            #exit()
            media_info = MediaInfo.parse(datei)
            logging.debug("Parsing MediaInfo for " + datei)
            logging.info("Processing file: " + datei)
            for track in media_info.tracks:
                if track.track_type == 'General':
                    logging.debug("General File Infos: Number of Audio Streams: " + str(track.count_of_audio_streams))
                elif track.track_type == 'Video':
                    logging.info("Checking video height for" + datei)
                    if (track.height < video_height_need):
                        logging.error("Video height is " + str(track.height) + " we need " + str(video_height_need))
                        move_to_manual(datei, "resolution to small")
                        moved=True
                        break
                    else:
                        logging.debug("Video Infos: Filename: " + datei + " Resulution: " + str(track.width) + "x" + str(track.height))
                        logging.info("Video height is ok...")
                        logging.info("Scannin " + datei + " for Audio Channels...")
                elif track.track_type == 'Audio':
                    if (track.language == "de"):
                        # USE track_id - 1 for the correct id... (ffmpeg workaround ...)!!!!
                        stramid=track.track_id-1
                        logging.info("GERMAN audio Found: #0." + str(stramid))
                        #logging.debug("Audio Channel #0." + str(stramid) + " Language: " + track.language + " Bitrate: " + str(track.bit_rate) + " Audi Channels: " + str(track.channel_s) + " Audio Codec: " + track.codec_info)
                        german=str(stramid)
                    elif (track.language == "en"):
                        stramid=track.track_id-1
                        logging.info("ENGLISH audio Found: #0." + str(stramid))
                        #logging.debug("Audio Channel #0." + str(stramid) + " Language: " + track.language + " Bitrate: " + str(track.bit_rate) + " Audi Channels: " + str(track.channel_s) + " Audio Codec: " + track.codec_info)
                        englisch=str(stramid)
                elif track.track_type == 'Text':
                    if (track.language == "en"):
                        logging.debug("Found English subs...")
            #if german AND english audio is found, add to database... else skipp file and move it to the _manual folder...
            if "german" and "englisch" in locals():
                insertstuff = epid, genre, epname, tvdbid, network, rating, overview, ep, snumber, sname, datei, englisch, german
                curs.execute("""insert into video
                values (?,?,?,?,?,?,?,?,?,?,NULL,?,?,?,0)""", insertstuff)
                conn.commit()
                logging.debug("Writing " + datei + " to the convert database VALUES: " + str(insertstuff))
                logging.info("Writing " + datei + " to the convert database")
                #reset/delete variables
                del german, englisch
            else:
               # print "No German OR English Audio found... Skipped file: " + datei
                # englisch="2"
                # german="1"
                # insertstuff = datei, englisch, german
                # curs.execute("""insert into video
                # values (NULL,?,?,?,0)""", insertstuff)
                # conn.commit()
                if (moved == True):
                    del moved
                else:
                    helper.move_to_manual(datei, "no language found")            
    run_ffmpeg()

def run_ffmpeg():
    conn = connect(pyEncoder + 'pyEncoder.db')
    curs = conn.cursor()
    curs.execute('select * from video order by filename')
    os.chdir(hotfolder)
    for row in curs:
        logging.debug("Database Output: " + str(row))
        #print row
        epid = row[0]
        genre = row[1]
        epname = row[2]
        tvdb_id = row[3]
        network = row[4]
        rating = row[5]
        overview = row[6]
        epnum = row[7]
        snumber = row[8]
        sname = row[9]
        localid  = row[10]
        datei = row[11]
        englisch = row[12]
        german = row[13]
        converted = row[14]
        filename, extension = os.path.splitext(datei)
        if (converted == 0):
            logging.info("MAPPING german audio to channel 1, english will be mapped to channel 2")
            logging.debug("CONVERTING: " + datei + " Convertsettings: ffmpeg -i " + pipes.quote(datei) + " -map 0.0 -map 0." + german + " -map 0." + englisch + " -s " + new_video_size + " -b " + str(vid_max_bitrate) + " -ab " + str(audio_max_bitrate) + " " + pipes.quote(filename) + ".mp4 -newaudio")
            logging.info("Starting converting for: " + datei)
            
             # -metadata title="Track #5" \
             #     -metadata author="Unknown Artist" \
             #     -metadata composer="Composer Unknown" \
             #     -metadata album="Tracer Video Game Soundtrack" \
             #     -metadata year="1996" \
             #     -metadata track="5" \
             #     -metadata comment="This is redbook CD audio track #5 from the Windows 95 game \"Tracer\"" \
             #     -metadata genre="Game Soundtrack" \
             #     -metadata copyright="Copyright 1996 Future Endeavors, Inc." \
             #     -metadata description="Nifty techno background tune for a futuristic video game" \
             #     -metadata synopsis="Hey, is this thing on? This is where the 'synopsis' field shows up." \
             #     -metadata show="Tracer" \
             #     -metadata episode_id="102" \
             #     -metadata network="Some network" \
            
            
            os.popen("ffmpeg -i " + pipes.quote(datei) + " -map 0.0 -map 0." + german + " -map 0." + englisch + " -s " + new_video_size + " -b " + str(vid_max_bitrate) + " -ab " + str(audio_max_bitrate) + " " + pipes.quote(filename) + ".mp4 -newaudio") # 2> /dev/null
            
            updatedb = str(row[10])
            curs2 = conn.cursor()
            curs2.execute("UPDATE video SET converted = '1' WHERE id=?", updatedb)
            logging.info("FINISHED converting for: " + datei)
            logging.debug("Upadting Database for " + datei + " with VALUE 1 for converted")
            newfilename=filename + ".mp4"
            #use atomicparsly to set metadatas...
            
            #os.popen(pyEncoder + "lib/AtomicParsley " + newfilename + "--title " + pipes.quote(epname) + " --description "  " --stik 'TV Show' " + " --TVNetwork " + " --TVShowName " + " --TVEpisode " + " --TVSeasonNum " + " --TVEpisodeNum " + " --genre" + " --overWrite")
            
            
            #fake the transcoding for tests...
            #shutil.copy (datei, newfilename)
            helper.move_when_finished(newfilename)
            if (keep_source == True):
                helper.move_source(datei)
            else:
                os.remove(datei)
                logging.info("Source File: " + datei + " DELETED!")
            conn.commit()
    #time.sleep(sleeptime*60)
    #test()
        

test()

