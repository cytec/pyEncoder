# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.


import StringIO, zlib, gzip
import os
import stat
import urllib, urllib2
import re, socket
import shutil
import ConfigParser


from xml.dom.minidom import Node

import sickbeard

from sickbeard.exceptions import MultipleShowObjectsException
from sickbeard import logger, classes
from sickbeard.common import USER_AGENT, mediaExtensions, XML_NSMAP

from sickbeard import db
from sickbeard import encodingKludge as ek
from sickbeard.exceptions import ex

from lib.tvdb_api import tvdb_api, tvdb_exceptions

import xml.etree.cElementTree as etree

urllib._urlopener = classes.SickBeardURLopener()

def isMediaFile (file):
    # ignore samples
    if re.search('(^|[\W_])sample\d*[\W_]', file):
        return False

    # ignore MAC OS's retarded "resource fork" files
    if file.startswith('._'):
        return False

    sepFile = file.rpartition(".")
    if sepFile[2].lower() in mediaExtensions:
        return True
    else:
        return False


def sanitizeFileName (name):
    '''
    >>> sanitizeFileName('a/b/c')
    'a-b-c'
    >>> sanitizeFileName('abc')
    'abc'
    >>> sanitizeFileName('a"b')
    'ab'
    >>> sanitizeFileName('.a.b..')
    'a.b'
    '''
    
    # remove bad chars from the filename
    name = re.sub(r'[\\/\*]', '-', name)
    name = re.sub(r'[:"<>|?]', '', name)
    
    # remove leading/trailing periods
    name = re.sub(r'(^\.+|\.+$)', '', name)
    
    return name
    

def makeDir (dir):
    if not ek.ek(os.path.isdir, dir):
        try:
            ek.ek(os.makedirs, dir)
        except OSError:
            return False
    return True


def listMediaFiles(dir):

    if not dir or not ek.ek(os.path.isdir, dir):
        return []

    files = []
    for curFile in ek.ek(os.listdir, dir):
        fullCurFile = ek.ek(os.path.join, dir, curFile)

        # if it's a dir do it recursively
        if ek.ek(os.path.isdir, fullCurFile) and not curFile.startswith('.') and not curFile == 'Extras':
            files += listMediaFiles(fullCurFile)

        elif isMediaFile(curFile):
            files.append(fullCurFile)

    return files

def copyFile(srcFile, destFile):
    ek.ek(shutil.copyfile, srcFile, destFile)
    try:
        ek.ek(shutil.copymode, srcFile, destFile)
    except OSError:
        pass

def moveFile(srcFile, destFile):
    try:
        ek.ek(os.rename, srcFile, destFile)
        fixSetGroupID(destFile)
    except OSError:
        copyFile(srcFile, destFile)
        ek.ek(os.unlink, srcFile)

def rename_file(old_path, new_name):

    old_path_list = ek.ek(os.path.split, old_path)
    old_file_ext = os.path.splitext(old_path_list[1])[1]

    new_path = ek.ek(os.path.join, old_path_list[0], sanitizeFileName(new_name) + old_file_ext)

    logger.log(u"Renaming from " + old_path + " to " + new_path)

    try:
        ek.ek(os.rename, old_path, new_path)
    except (OSError, IOError), e:
        logger.log(u"Failed renaming " + old_path + " to " + new_path + ": " + ex(e), logger.ERROR)
        return False

    return new_path

#use os.walk to process subdirs as well
def scanFolder(foldername):
    
    allfiles = []
    
    for root, dirs, files in os.walk(foldername):
        for file in files:
            file = os.path.join(root, file)
            
            if isMediaFile(file):
                   allfiles.append(file)
                   
    return allfiles

