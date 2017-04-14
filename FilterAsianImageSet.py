# -*- coding: utf-8 -*-
import os.path
import re

# note: this file filter the image in not .jpg


def getFileList(folderName):
    imgList = os.listdir(folderName)
    if 'Thumbs.db' in imgList:
        imgList.remove('Thumbs.db')
    return imgList

root_dir = r'F:\china_face'
for parent, dirNames, fileNames in os.walk(root_dir + os.sep + 'Asian_face'):
    if len(dirNames) != 0:
        for dirName in dirNames:
            if re.match('temp', dirName):
                continue
            print dirName
            imageList = getFileList(os.path.join(parent, dirName))
            for imageItem in imageList:
                if imageItem.strip().split('.')[-1] != 'jpg':
                    oldName = os.path.join(parent, dirName, imageItem)
                    # newname = os.path.join(parent, 'temp', dirName+'_'+imageItem)
                    newname = root_dir + os.sep + 'temp' + os.sep + dirName + '_' + imageItem
                    os.rename(oldName, newname)
    else:
        break