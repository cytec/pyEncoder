import os.path
import operator, platform
import re
import ConfigParser


def genConfig():
	config = ConfigParser.RawConfigParser()
	config.add_section('General')
	config.set('General', 'int', '15')
	config.set('General', 'bool', 'true')
	config.set('General', 'float', '3.1415')
	config.set('General', 'baz', 'fun')
	config.set('General', 'bar', 'Python')
	config.set('General', 'foo', '%(bar)s is %(baz)s!')