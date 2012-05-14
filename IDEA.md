pyEncoder is the current working name.

It stated as an (re)encoder for media files to convert them to an iTunes/iDevice compatible format.

The current idea is:

* (re)encode mediafiles to mp4
	- scale down to 720p
	- video bitrate max 250kbit (AppleTV support)
	- if video is lower than 720p/250kbit keep settings
	- select german and english audio (german primary)
* recognize series and add iTunes Mediadata to mp4/mv4 files
* webinterface
	- settings
	- Series Infos etc
* same for movies
* file renaming based on mediainfos

at the moment only the reencoding and basic tvdb infos are done.

THIS IS STILL A VERRY ALPHA STATE THING, so use on your own risk


ADDITIONAL IDEAS:

Do the same stuff for movies (check imdb for movie infos) and then reencode those files according to settings for the different watch folders.
Settings should be manageabel over webinterface, watchfolders too

Example:

folder 3DStuff has settings: Audio AC3, bitrate 448k, channels 2, and videocodec h264
every file inside 3DStuff should be reencoded to those settings (use passthorugh if possible) and dont change video sizes...

folder iTunes has settings: Audio mp3, bitrate 128k, channels 2, videocodec h264, videobitrate 250k, resolution 720p, german audio first, add mediadata
all files should be encoded with the settings above and the german audiostream should be mapped to 0.1 additional audio gets mapped 0.2 etc


**pyEncoder uses [ffmpeg](http://http://ffmpeg.org/) for encoding, [tvdb_api](https://github.com/dbr/tvdb_api) for metadata, [mediainfo CLI](http://mediainfo.sourceforge.net/de) for getting infos from video file, and [AtomicParsley](http://atomicparsley.sourceforge.net/) to set the iTunes metadatas**

Developed under: OSX 10.7 with python 2.7.2