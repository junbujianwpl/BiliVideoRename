# encoding : utf-8 
# @File    : Utilities.py
# @Author  : AllenWoo
# @Date    : 2018/1/30 9:01
# @license : Copyright(C), all right reserved.
# @Contact : http://github.com/junbujianwpl
# @Desc    : common utilities

import os


def get_file_size(fname):
    return os.path.getsize(fname)


def rename_file(old_name, new_name):
    os.rename(old_name, new_name)


def path_to_dict(path):
    d = {'name': os.path.basename(path), "size": os.path.getsize(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d
