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
