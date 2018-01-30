# encoding : utf-8 
# @File    : RenameBiliVideo.py
# @Author  : AllenWoo
# @Date    : 2018/1/29 23:30
# @license : Copyright(C), all right reserved.
# @Contact : http://github.com/junbujianwpl
# @Desc    : rename bili video in the download dir

from component.InspectUtil import *
from component.Logger import *
from component.Utilities import *
import os
import sys
import itertools
import json
import functools

log_path = os.path.join("bili_log.log")
my_logger = create_file_logger(log_path)

index_file_name = "entry.json"
title_key = "title"
part_key = "part"
dst_suffix = ".mp4"
src_suffix = ".blv"

connect_sep = "_"

primary_dir_info = {}


class DirInfo:
    pass


@dec_deal_exception(lambda: my_logger.debug(traceback.format_exc()))
def init():
    pass


@dec_deal_exception(lambda: my_logger.debug(traceback.format_exc()))
def get_title_part_name(fname):
    with open(fname, encoding="utf8") as f:
        exclude_char = ['\\', '/', '*', '?', '<', '>', ':', '|', '"']
        my_dict = json.load(f)
        title = functools.reduce(lambda s, c: str(s).replace(str(c), ""), exclude_char,
                                 str(my_dict.get(title_key, None)))
        part = functools.reduce(lambda s, c: str(s).replace(str(c), ""), exclude_char,
                                str(my_dict.get("page_data").get(part_key, None)))
        return title, part


def analyze_root(dir):
    sub_dirs = os.listdir(dir)
    print_time(sub_dirs)
    title = ""
    part = ""
    for dirpath, dirs, files in os.walk(dir):
        base_name = os.path.abspath(dirpath)
        for f in files:
            if f == index_file_name:
                title, part = get_title_part_name(os.path.join(base_name, f))
            # rename *.blv to dir_basename.mp4
            file_name, ext_name = os.path.splitext(f)
            if ext_name == src_suffix:
                os.rename(os.path.join(base_name, f),
                          os.path.join(base_name, "{}_{}{}".format(dirpath, file_name, dst_suffix)))

        dir_added = []
        if title and part:  # found the index file
            i = 0
            for d in dirs:  # itertools.product cross each element, zip good
                dst_dir_name = os.path.join(base_name, "{}{}{}".format(title, connect_sep, i))
                if dst_dir_name == d:
                    continue
                while os.path.exists(dst_dir_name):
                    i += 1
                    dst_dir_name = os.path.join(base_name, "{}{}{}".format(title, connect_sep, i))

                os.rename(os.path.join(base_name, d), dst_dir_name)
                dir_added.append(dst_dir_name)
                i += 1
                # os.rename(os.path.join(base_name, d), os.path.join(base_name, "a"))
        dirs += dir_added


if __name__ == '__main__':
    root_dir = r"I:/Bilibili/Nox_share/Other/10610680"
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]

    dir_info = path_to_dict(root_dir)
    my_logger.debug(dir_info)
    analyze_root(root_dir)
    init()
