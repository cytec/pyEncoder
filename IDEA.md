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

**pyEncoder uses [ffmpeg](http://http://ffmpeg.org/) for encoding, [tvdb_api](https://github.com/dbr/tvdb_api) for metadata, [mediainfo CLI](http://mediainfo.sourceforge.net/de) for getting infos from video file, and [AtomicParsley](http://atomicparsley.sourceforge.net/) to set the iTunes metadatas**

Developed under: OSX 10.7 with python 2.7.2