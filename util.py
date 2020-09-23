import os
import shutil


def delAllFiles(rootdir):
    filelist = []
    filelist = os.listdir(rootdir)  # list all the files
    for f in filelist:
        filepath = os.path.join(rootdir, f)  # path-absolute path
        if os.path.isfile(filepath):  # is file?
            os.remove(filepath)  # delete file
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)  # is dir


def mkdir(path):
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

        print(path + ' created')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' already existed')
        return False
