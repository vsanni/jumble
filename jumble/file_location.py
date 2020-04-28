"""
Created on Sat Nov 24 12:21:06 2018

@author: vsanni
"""

import os
import datetime
import time
import glob
from uuid import uuid4
import tempfile as tf

from jumble.type_extra import as_list, string_replace


def split(file_location):

    if  isinstance(file_location, (list, tuple)):
        l = []
        for p in file_location:
            path, filename      = os.path.split(p)
            filename, extension = os.path.splitext(filename)
            l.append([path, filename, extension])
        return l

    else:
        path, filename      = os.path.split(file_location)
        filename, extension = os.path.splitext(filename)

        return path, filename, extension



def path(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [os.path.split(p)[0] for p in file_location]

    else:
        return os.path.split(file_location)[0]



def filename(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [os.path.splitext(os.path.split(p)[1])[0] for p in file_location]

    else:
        return os.path.splitext(os.path.split(file_location)[1])[0]



def extension(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [os.path.splitext(p)[1][1:] for p in file_location]

    else:
        return os.path.splitext(file_location)[1][1:]



def temporary(temp_dir=None, prefix='', postfix='', extension=None):

    if temp_dir is None: temp_dir = tf.gettempdir()

    if extension is not None: extension = path.extsep+extension
    else                    : extension = ""

    return path.join(temp_dir, prefix+str(uuid4())+postfix+extension)



def good(file_location, replacement="", space_replacement=""):

    bad_chars="^*|()[]{}<>'`~\":;,?$%&!@=\n\t\r"

    def _good(fl, bad_chars, replacement):
        fl    = fl.replace(" ",space_replacement).replace("&","and")
        fl    = string_replace(fl, BadChars=bad_chars, Replacement=replacement)
        s     = ""
        found = False
        for c in fl:
            if c == "."  and not found:
                s    += c
                found = True
            elif c != ".":
                found = False
                s    += c
        return s


    if  isinstance(file_location, (list, tuple)):
        return [_good(fl, bad_chars, replacement) for fl in file_location]

    else:
        return _good(file_location, bad_chars, replacement)


def good_date(date):

    m, d, y = [int(s) for s in date.split("/")]

    return "%04d-%02d-%02d" %(y, m, d)


def current_time(pre_string="", post_string=""):
    return pre_string+time.strftime("%H:%M:%S")+post_string


def current_datetime(pre_string="", post_string=""):
    return pre_string+time.strftime("%F.%H:%M:%S")+post_string


def current_date(pre_string="", post_string=""):
    return pre_string+time.strftime("%F")+post_string


def remove_extension(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [os.path.join(*split(p)[:2]) for p in file_location]

    else:
        return os.path.join(*split(file_location)[:2])



def remove_path(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [os.path.split(p)[-1] for p in file_location]

    else:
        return  os.path.split(file_location)[-1]



def files_location(base_path=[""]):

    files = []
    for bp in as_list(base_path):
        files += glob.glob(bp)

    files.sort()

    return files



def datestamp(fl):
    import os
    from datetime import datetime

    t  = os.path.getctime(fl)
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")



def filename_date(date):

    s = date.split("/")

    return datetime.datetime(int(s[2]), int(s[0]), int(s[1]), 0, 0).strftime("%Y-%m-%d")
