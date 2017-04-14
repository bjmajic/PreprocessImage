# -*-coding:utf-8-*-
# import os
import os.path
import random
import sys


def getFileList(dirname):
    imgList = os.listdir(dirname)
    if 'Thumbs.db' in imgList:
        imgList.remove('Thumbs.db')
    return imgList


def CreateDataList(rootdir, thresh=100):
    labelIndex = 0
    trainPath = os.path.join(rootdir, 'train.txt')
    valPath = os.path.join(rootdir, 'test.txt')
    testSet = []
    trainSet = []
    if os.path.exists(trainPath):
        os.remove(trainPath)
    if os.path.exists(valPath):
        os.remove(valPath)
    for parent, dirnames, filenames in os.walk(rootdir):
        if len(dirnames) != 0:
            for dirname in dirnames:
                image_list = getFileList(os.path.join(parent, dirname))
                dataLen = len(image_list)
                if dataLen < thresh:
                    print dirname
                    continue
                else:
                    testNum = int(thresh * 0.2)
                    trainNum = int(thresh * 0.8)
                trainingSet = range(dataLen)

                for i in range(testNum):
                    randIndex = int(random.uniform(0, len(trainingSet)))
                    recordStr = dirname + os.sep + image_list[trainingSet[randIndex]] + ' ' + str(labelIndex) + '\n'
                    testSet.append(recordStr)
                    del(trainingSet[randIndex])
                for i in range(trainNum):
                    randIndex = int(random.uniform(0, len(trainingSet)))
                    recordStr = dirname + os.sep + image_list[trainingSet[randIndex]] + ' ' + str(labelIndex) + '\n'
                    trainSet.append(recordStr)
                    del (trainingSet[randIndex])
                print labelIndex  #  本次循环有效
                labelIndex += 1
        else:
            break
    # 写入文件
    with open(trainPath, 'a+') as train_fid:
        train_fid.writelines(trainSet)
    with open(valPath, 'a+') as test_fid:
        test_fid.writelines(testSet)


if __name__ == '__main__':

    # the first param is rootdir
    # the second param is thresh value
    root_dir = r'F:\WebFace'
    CreateDataList(root_dir, 100)
    """"
    argc = len(sys.argv)
    if argc <= 1:
        print 'less param count'
    elif argc == 2:
        root_dir = sys.argv[1]
        CreateDataList(root_dir, 100)
    elif argc == 3:
        root_dir = sys.argv[1]
        threshValue = int(sys.argv[2])
        CreateDataList(root_dir, threshValue)
    else:
        print "too many params"
    """
