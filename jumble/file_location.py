"""
Created on Sat Nov 24 12:21:06 2018

@author: vsanni
"""

import os
import time
from jumble.type_extra import as_list,string_replace


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
        return [ os.path.split(p)[0] for p in file_location]

    else:
        return os.path.split(file_location)[0]



def filename(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [os.path.splitext(os.path.split(p)[1])[0] for p in file_location]

    else:
        return os.path.splitext(os.path.split(file_location)[1])[0]



def extension(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [ os.path.splitext(p)[1] for p in file_location]

    else:
         return os.path.splitext(file_location)[1]



def temporary( temp_dir=None,prefix='',postfix='',extension=None):

    from uuid import uuid4
    import tempfile as tf

    if temp_dir is None: temp_dir = tf.gettempdir()

    if extension is not None: extension = path.extsep+extension
    else                    : extension = ""

    return path.join(temp_dir,prefix+str(uuid4())+postfix+extension)



def good(file_location, replacement=""):

    bad_chars=" ^*|()[]{}<>'`~\":;,?$%&!@=\n\t\r"

    if  isinstance(file_location, (list, tuple)):
        return [ string_replace(p, BadChars=bad_chars, Replacement=replacement) for p in file_location]

    else:
        return string_replace(file_location, BadChars=bad_chars, Replacement=replacement)



def current_time(pre_string="",post_string=""):
    return pre_string+time.strftime("%F.%H-%M-%S")+post_string



def remove_extension(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [ os.path.join(*split(p)[:2]) for p in file_location]

    else:
        return os.path.join(*split(file_location)[:2])



def remove_path(file_location):

    if  isinstance(file_location, (list, tuple)):
        return [ os.path.split(p)[-1] for p in file_location]

    else:
        return  os.path.split(file_location)[-1]



def files_location( base_path=[""], base_filename=[""], extension=[""]):

    import glob

    files = []
    for bp in as_list(base_path):
        for bn in as_list(base_filename):
            for ex in as_list(extension):
                files += glob.glob(os.path.join(bp, bn if ex == "" else bn+'.' + ex))

    files.sort()

    return files
