import os

def move_to_manual(file, becauseof):
    os.chdir(hotfolder)
    datei2="manual_process/" + file
    if not os.path.exists("manual_process"):
        os.makedirs("manual_process")
    os.rename(file, datei2)
    logging.info("Moved " + file + " to manual_process Folder! --- " + becauseof)

def move_when_finished(file):
    os.chdir(hotfolder)
    datei2="Converted/" + file
    #newfilename with tvdb stuff? not rlly for repacking -.-
    if not os.path.exists("Converted"):
        os.makedirs("Converted")
    os.rename(file, datei2)
    logging.info("DONE: " + file + " was moved to Converted Folder!")
    
def move_source(file):
    os.chdir(hotfolder)
    datei2="BACKUP/" + file
    if not os.path.exists("BACKUP"):
        os.makedirs("BACKUP")
    os.rename(file, datei2)
    logging.info("BACKUP: " + file + " was moved to BACKUP Folder!")


def move_to_target(sourcefolder, file, targetfolder):
    os.chdir(sourcefolder)
    datei2 = targetfolder + "/" + file
    os.rename(file, datei2)
    print sourcefolder, file, targetfolder, datei2

def isMediaFile(extension):
    mediaExtensions = ['.avi', '.mkv', '.mpg', '.mpeg', '.wmv',
                   '.ogm', '.mp4', '.iso', '.img', '.divx',
                   '.m2ts', '.m4v', '.ts', '.flv', '.f4v',
                   '.mov', '.rmvb', '.vob', '.dvr-ms', '.wtv',
                   '.ogv']
    if extension in mediaExtensions:
        return extension
    else:
        return None

def doAppleTV(sourcefolder, file, targetfolder, acodec):
    filename, extension = os.path.splitext(file)
    return "ffmpeg -i " + sourcefolder + "/" +file+ " -vcodec h264 -b 2500k -s 1280x720 -aspect 1280:720 -maxrate 4500k -acodec " + acodec + " " + targetfolder +"/"+filename+".appleTV.m4v"


def getAudioValue(acodec):
    qualityStrings = {
        'unknown' : 0,
        'none' : 0,
        'ogg' : 0,
        'mp3' : 1,
        'mp2' : 2,
        'aac' : 3,
        'ac3' : 4,
        'dts' : 5,
    }
    try:
        quality = qualityStrings[acodec]
    except:
        quality = None
    return quality