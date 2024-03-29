#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 寻找Xcode中不使用的图片

import glob
import os
import re
import shutil

#  正则表达式  \d匹配一个数字字符。等价于[0-9]，+匹配1或多个正好在它之前的那个字符，
# ignores = {r'image\d+'}  意思是以 image 开头的，image后面是数字的图片名的使用情况，例如能搜索到的图片是 image1、image2等等
# ignores = {r'(image | group)\d+'} 意思是以 image 或 group开头，后面跟数字的图片名，例如：image1、image2、group1、group2等等
# ignoresImg = {r'image\0d+'}


def find_un_used():

    img_names = [os.path.basename(pic)[:-9] for pic in images]
    unused_imgs = []
    for i in range(0, len(images)):
        pic_name = img_names[i]
        print("pic_name:", pic_name)

        # print("是否是ignore图片：",is_ignore(pic_name))
        # if is_ignore(pic_name):
        #     continue
        if pic_name == "code" or pic_name == "phone":  # 跳过是因为会报错
            continue
        # command = 'ag "我的_我的邀请_首页_17" /Users/admin/iosdeleteYoushangcheng/fmapp'
        command = 'ag "%s" %s' % (pic_name, srcpath)
        print("command是 ==== ", command)  # ag "我的_我的邀请_首页_17" /Users/admin/iosdeleteYoushangcheng/fmapp
        # os.popen 执行bash命令， .read()读取执行的结果。
        result = os.popen(command).read()
        print("\n 执行结果：", result, "\n")
        if result == '':
            if not is_ignore(pic_name):  # 判断是否是动态加载图片,True是动态加载，不删除
                unused_imgs.append(images[i])
                print('remove %s' % (images[i]))
                # 先不删除
                # os.system('rm -rf %s' % (images[i])) # 直接执行bash命令
    text_path = 'unused.txt'
    tex = '\n'.join(sorted(unused_imgs))
    os.system('echo "%s" > %s' % (tex, text_path))
    print('unuse res:%d' % (len(unused_imgs)))
    print('Done!')

def is_ignore(str):
    ignore = str[:-1]  # 将字符串 未标题-1_0、未标题-1_1 等，去掉最后数字,如果是2位数字的，可能会有问题。例如： 未标题-1_20、未标题-1_21，动态添加是把20整体变成不确定的数值
    dynamic_str = ignore+'%d'

    command = 'ag "%s" %s' % (dynamic_str, path)
    print("is_ignore == command是 ==== ", command)  # ag "我的_我的邀请_首页_17" /Users/admin/iosdeleteYoushangcheng/fmapp
    result = os.popen(command).read()
    print("is_ignore == \n执行结果：", result, "\n")
    if result == '':
        return False
    else:
        return True

    # for ignore in ignores: # 判断是否是动态
    #     if re.match(ignore, str):
    #         return True
    # return False


if __name__ == '__main__':

    # '/Users/admin/iosdeleteYoushangcheng/fmapp'
    path = input("Images.xcassets的文件夹路径并点击Enter开始：\n")  # /Users/admin/ios/fmapp/Images.xcassets
    srcpath = input("输入xcodeproj文件所在文件夹路径并按Enter开始：\n")  # /Users/admin/ios

    testTwo = '%s/%s' % (srcpath, os.path.basename(path))  # /Users/admin/iosdeleteYoushangcheng/Images.xcassets

    if not os.path.exists(testTwo):
        shutil.move(path, srcpath)  # 将文件进行移动原因，如果不把文件移动出来，在查找的时候，会再次查找一遍Images.xcassets文件，导致很多没引用的图片也能搜到

    images = glob.glob('%s/*/*.imageset' % testTwo)
    print("images的长度：", len(images))
    find_un_used()

    # images = glob.glob('%s/Images.xcassets/*/*.imageset' % srcpath)


# import glob
# import os
# import re
#
# path = 'ios'
#
# ignores = {r'image_\d+'}
# images = glob.glob('ios/images.xcassets/*/*.imageset')
#
# def find_un_used():
#     img_names = [os.path.basename(pic)[:-9] for pic in images]
#     unused_imgs = []
#     for i in range(0, len(images)):
#         pic_name = img_names[i]
#         if is_ignore(pic_name):
#             continue
#         command = 'ag "%s" %s' % (pic_name, path)
#         result = os.popen(command).read()
#         if result == '':
#             unused_imgs.append(images[i])
#             print 'remove %s' % (images[i])
#             os.system('rm -rf %s' % (images[i]))
#
#
#     text_path = 'unused.txt'
#     tex = '\n'.join(sorted(unused_imgs))
#     os.system('echo "%s" > %s' % (tex, text_path))
#     print 'unuse res:%d' % (len(unused_imgs))
#     print 'Done!'
#
#
# def is_ignore(str):
#     for ignore in ignores:
#         if re.match(ignore, str):
#             return True
#     return False
#
#
# if __name__ == '__main__':
#     find_un_used()#     find_un_used()#     find_un_used()
