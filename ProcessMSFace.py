# -*-coding:utf-8 -*-
import os.path
import shutil

def getFileList(dirName):
    imgList = os.listdir(dirName)
    if 'Thumbs.db' in imgList:
        imgList.remove('Thumbs.db')
    return imgList

def DeleteFolderLessThanThresh(rootDir, threshValue = 10):
    recordArr = []
    for parent, dirNames, fileNames in os.walk(rootDir):
        if len(dirNames) == 0:
            break
        else:
            for dirName in dirNames:
                imageList = getFileList(os.path.join(parent, dirName))
                if len(imageList) <= threshValue:
                    str_tmp = dirName + "\t" + str(len(imageList)) + '\n'
                    recordArr.append(str_tmp)
                    shutil.rmtree(os.path.join(parent, dirName))
            if len(recordArr) != 0:
                savePathName = 'DeleteFolderLessThanThresh.txt'
                with open(savePathName, 'w') as train_fid:
                    train_fid.writelines(recordArr)

if __name__ == '__main__':
    actionType = 1
    root_dir = r"D:\test - 1"
    if actionType == 1:
        DeleteFolderLessThanThresh(root_dir, 10)
    else:
        print "other thing to be done"
        print "hahaha"
