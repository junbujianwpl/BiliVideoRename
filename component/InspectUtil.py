# encoding : utf-8
# @File    : InspectUtil.py
# @Author  : AllenWoo
# @Date    : 18-1-20 上午11:20
# @license : Copyright(C), all right reserved.
# @Contact : http://github.com/junbujianwpl
# @Desc    :

import inspect
import traceback
import time


def run_all_method_of_object(obj):
    attributes = (getattr(obj, name) for name in dir(obj))
    methods = filter(inspect.ismethod, attributes)
    for m in methods:
        try:
            print_time("%s,%s" % (m.__name__, str(m())))
        except:
            print_time(traceback.format_exc())


def dec_deal_exception(except_deal_func=None, *args_except, **kwargs_except):
    def deco(func):
        def _deco(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                try:
                    if except_deal_func is not None:
                        return except_deal_func(*args_except, **kwargs_except)
                except:
                    print_time(traceback.format_exc())

        return _deco

    return deco


@dec_deal_exception(lambda x: print_time("%s,lambd" % (str(x))), "haha")
def test():
    print_time("test")
    raise Exception()


@dec_deal_exception()
def test_abbrv():
    print_time("abbrv")


def print_time(*args, **kwargs):
    new_args = (time.strftime("%m-%d %H:%M:%S"), *args)
    print(*new_args, **kwargs)


def get_caller_func_name():
    return traceback.extract_stack(None, 2)[0][2]


def get_caller_class_name():
    frame = inspect.stack()[1][0]
    args, _, _, value_dict = inspect.getargvalues(frame)
    # we check the first parameter for the frame function is
    # named 'self'
    if len(args) and args[0] == 'self':
        # in that case, 'self' will be referenced in value_dict
        instance = value_dict.get('self', None)
        if instance:
            # return its class
            return getattr(instance, '__class__', None)
    # return None otherwise
    return None


if __name__ == '__main__':
    print_time("haha", "hehe", 3, 4, 3)
    get_caller_class_name()
    # test()
    # test_abbrv()
