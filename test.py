from lib import enzyme

#p = enzyme.parse("/Users/workstation/Downloads/complete/Elfen.Lied.COMPLETE.German.Dubbed.HDTVRiP/Elfen.Lied.-.EP09.-.Schoene.Erinnerung.mkv")
#p = enzyme.parse("/Volumes/Datengrab/3D Filme/Avatar (2009)/Avatar.Aufbruch.nach.Pandora.3D.2009.German.DL.1080p.BluRay3D.x264-ANCIENT.mkv")
p = enzyme.parse("/Volumes/Datengrab/Filme_check/Date Night (2010)/Date.Night.2010.Extended.Version.German.DL.720p.BluRay.x264-LeetHD.mkv")
languages = {
	"ger": "german",
	"jpn": "japanese",
	"eng": "english"
}

audio = {
	26448: "Vorbis",
	8193: "dts",
	8192: "ac3",
	85: "mp3"

}

for track in p.audio:
	print "AUDIO: id {0}, language: {1}, codec: {2}, default: {3}, channels: {4}".format(track.id, track.language, track.codec, track.default, track.channels)
	print "AUDIO: Long codes... language: {0}, codec: {1}".format(languages[track.language], audio[track.codec])

for track in p.video:
	print "VIDEO: Title {0}, width: {1}, height: {2}, fps: {3}".format(track.title, track.width, track.height, track.fps)