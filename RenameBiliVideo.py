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


@dec_deal_exception(lambda: my_logger.debug(traceback.format_exc()))
def get_title_part_name(fname):
    with open(fname, encoding="utf8") as f:
        exclude_char = ['\\', '/', '*', '?', '<', '>', ':', '|', '"']
        fill_str = " "
        my_dict = json.load(f)
        title = functools.reduce(lambda s, c: str(s).replace(str(c), fill_str), exclude_char,
                                 str(my_dict.get(title_key, None)))
        part = functools.reduce(lambda s, c: str(s).replace(str(c), fill_str), exclude_char,
                                str(my_dict.get("page_data").get(part_key, None)))
        return title, part


@dec_deal_exception(lambda: my_logger.debug(traceback.format_exc()))
def analyze_root(dir):
    """

    :param dir: must be the exact root dir of a batch of videos
    :return:
    """
    sub_dirs = os.listdir(dir)
    print_time(sub_dirs)
    title = ""
    part = ""
    for dirpath, dirs, files in os.walk(dir):
        dir_abs_name = os.path.abspath(dirpath)
        for f in files:
            if f == index_file_name:
                title, part = get_title_part_name(os.path.join(dir_abs_name, f))
            # rename *.blv to dir_basename.mp4
            file_name, ext_name = os.path.splitext(f)
            if ext_name == src_suffix:
                # keep file in old dir code
                # os.rename(os.path.join(dir_abs_name, f),
                #           os.path.join(dir_abs_name,
                #                        "{}_{}{}".format(os.path.basename(dir_abs_name), file_name, dst_suffix)))
                # mv file upward twice
                twice_up_dir = os.path.join(dir_abs_name, os.path.pardir, os.path.pardir)
                tag_name = os.path.basename(dir_abs_name)
                primary_index = os.path.basename(os.path.join(dir_abs_name, os.path.pardir))
                i = 0
                new_name = os.path.join(twice_up_dir,
                                        "{}_{}_{}_{}{}".format(tag_name, primary_index, file_name, i, dst_suffix))
                while os.path.exists(new_name):
                    i += 1
                    new_name = os.path.join(twice_up_dir,
                                            "{}_{}_{}_{}{}".format(tag_name, primary_index, file_name, i, dst_suffix))

                os.rename(os.path.join(dir_abs_name, f), new_name)

        dir_added = []
        if title and part:  # found the index file
            i = 0
            for d in dirs:  # itertools.product cross each element, zip good
                primary_index = os.path.basename(dir_abs_name)
                dst_dir_name = os.path.join(dir_abs_name, "{}{}{}_{}".format(title, connect_sep, primary_index, i))
                if dst_dir_name == d:
                    continue
                while os.path.exists(dst_dir_name):
                    i += 1
                    dst_dir_name = os.path.join(dir_abs_name, "{}{}{}_{}".format(title, connect_sep, primary_index, i))

                os.rename(os.path.join(dir_abs_name, d), dst_dir_name)
                dir_added.append(dst_dir_name)
                i += 1
        dirs += dir_added
    if title:
        new_name = os.path.join(os.path.join(dir, os.path.pardir), title)
        while os.path.exists(new_name):
            new_name += "_"
        os.rename(dir, new_name)


if __name__ == '__main__':
    root_dir = r"I:/Bilibili/Nox_share/Other"
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]

    for dir in os.listdir(root_dir):
        sub_dir = os.path.join(root_dir, dir)
        if os.path.isdir(sub_dir):
            dir_info = path_to_dict(sub_dir)
            my_logger.debug(dir_info)
            analyze_root(sub_dir)
