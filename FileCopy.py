# -*- coding:utf-8 -*-
import os.path
import re
import shutil

def getFileList(dirName):
    imgList = os.listdir(dirName)
    if 'Thumbs.db' in imgList:
        imgList.remove('Thumbs.db')
    if 'record.txt' in imgList:
        imgList.remove('record.txt')
    return imgList


def CopyFile(srcFolder, desFolder):
    for parent, dirnames, filenames in os.walk(srcFolder):
        if len(dirnames) != 0:
            for dirname in dirnames:
                imagelist = getFileList(os.path.join(parent, dirname))
                for imageItem in imagelist:
                    srcFile = os.path.join(parent, dirname, imageItem)
                    desPath = os.path.join(desFolder, dirname)
                    shutil.move(srcFile, desPath)
        else:
            break


def FindModifiedFolders(root1, root2):
    for parent, dirnames, filenames in os.walk(root1):
        if len(dirnames) != 0:
            dirnames_1 = dirnames[:]
        else:
            break
    for parent, dirnames, filenames in os.walk(root2):
        if len(dirnames) != 0:
            dirnames_2 = dirnames[:]
        else:
            break
    dirnames1_copy = dirnames_1[:]
    dirnames2_copy = dirnames_2[:]
    for dir1 in dirnames_1:
        if dir1 in dirnames_2:
            dirnames1_copy.remove(dir1)
            dirnames2_copy.remove(dir1)
    print dirnames1_copy
    print dirnames2_copy


def SaveImage2Txt(imageDir, saveDir):
    for parent, dirnams, filenames in os.walk(imageDir):
        if len(dirnams) != 0:
            for dirname in dirnams:
                txtname = dirname + '.txt'
                saveName = os.path.join(saveDir, txtname)
                recordArr = []
                imageList = getFileList(os.path.join(parent, dirname))
                for imageItem in imageList:
                    recordArr.append(imageItem + "\n")
                with open(saveName, 'w') as save_fid:
                    save_fid.writelines(recordArr)
        else:
            break

def DeleteFileNotInTxt(imageDir, txtDir):
    for parent, dirnames, filenames in os.walk(imageDir):
        if len(dirnames) != 0:
            for dirname in dirnames:
                txtname = dirname + '.txt'
                txtPath = os.path.join(txtDir, txtname)
                txtRecordArr = []
                with open(txtPath, 'r') as fid:
                    for line in fid.readlines():
                        txtRecordArr.append(line.strip())
                imageList = getFileList(os.path.join(parent, dirname))
                for img in imageList:
                    if img not in txtRecordArr:
                        os.remove(os.path.join(parent, dirname, img))
                print dirname
        else:
            break
def DeleteFolderLessThanThresh(imageDir, threshValue=10):
    for parent, dirnames, filenames in os.walk(imageDir):
        if len(dirnames) != 0:
            for dirname in dirnames:
                imageList = getFileList(os.path.join(parent, dirname))
                if len(imageList) <= threshValue:
                    shutil.rmtree(os.path.join(parent, dirname))
                    print os.path.join(parent, dirname)
        else:
            break

if __name__ == '__main__':
    # root1 = r'F:\samll_face_pic\temp_quan'
    # root2 = r'F:\WebFace2'
    # FindModifiedFolders(root1, root2)
    root1 = r'F:\webface_txt'
    root2 = r'E:\new_webface'
    # DeleteFileNotInTxt(root2, root1)
    DeleteFolderLessThanThresh(root2, 10)