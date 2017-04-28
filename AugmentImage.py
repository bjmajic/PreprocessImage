# -*- coding: utf-8 -*-
import cv2
import os.path
import random
import sys
import re

def GrayTrans(imageName):
    imgSrc = cv2.imread(imageName.encode('gbk'))
    if len(imgSrc.shape) != 3:
        return
    imgGray = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2GRAY)
    saveTrans(imgGray, imageName, 'gray')
    return imgGray


def BlurTrans(imageName, method='Gaussian', kernel=7):
    if method == 'Gaussian':
        imgSrc = cv2.imread(imageName.encode('gbk'))
        imgBlur = cv2.GaussianBlur(imgSrc, (kernel, kernel), 0.8)
    saveTrans(imgBlur, imageName, 'gauss')
    return imgBlur


def saveTrans(image, imageName, transType='gauss'):
    ext = imageName[-4:]
    saveName = imageName[0: -4] + '_' + transType + ext;
    cv2.imwrite(saveName.encode('gbk'), image)


def getFileList(dirname):
    imgList = os.listdir(dirname)
    if 'Thumbs.db' in imgList:
        imgList.remove('Thumbs.db')
    if 'record.txt' in imgList:
        imgList.remove('record.txt')
    return imgList


def ExpandImage(listRootDir=[], lowthresh=20, expandSize=100):
    '''
    扩充样本的数量，规则为灰度化或者高斯模糊
    :param listRootDir: 根目录列表, 根目录需要写到包含各个类别目录的父目录
    :param expandSize: 需要扩充到数量
    :param lowthresh: 低于这个阈值，则不进行灰度化和高斯模糊来扩充样本
    :return:
    '''
    if len(listRootDir) == 0:
        return
    for root_dir in listRootDir:
        for parent, dirnames, filenames in os.walk(root_dir):
            if len(dirnames) != 0:
                for dirname in dirnames:
                    print dirname
                    image_list = getFileList(os.path.join(parent, dirname))
                    needGrayTrans = True
                    if len(image_list) < lowthresh:
                        continue
                    while len(image_list) < expandSize:
                        imageSet = range(len(image_list))
                        if needGrayTrans:
                            for i in range(expandSize - len(image_list)):
                                if len(imageSet) == 0:
                                    break
                                randIndex = int(random.uniform(0, len(imageSet)))
                                imagePath = os.path.join(parent, dirname, image_list[imageSet[randIndex]])
                                print imagePath
                                del (imageSet[randIndex])
                                GrayTrans(imagePath)
                            needGrayTrans = False
                            image_list = getFileList(os.path.join(parent, dirname))
                        else:
                            # print len(image_list)
                            for i in range(expandSize - len(image_list)):
                                if len(imageSet) == 0:
                                    break
                                randIndex = int(random.uniform(0, len(imageSet)))
                                imagePath = os.path.join(parent, dirname, image_list[imageSet[randIndex]])
                                del (imageSet[randIndex])
                                BlurTrans(imagePath, 'Gaussian', 2 * (randIndex % 4) + 1)  # 限制kernel的大小为1,3,5,7
                            image_list = getFileList(os.path.join(parent, dirname))
            else:
                break


def deleteImage(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):
        if len(dirnames) != 0:
            for dirname in dirnames:
                print dirname
                print dirname
                image_list = os.listdir(os.path.join(parent, dirname))
                for img in image_list:
                    splitArr = img.split('.')
                    if splitArr[-1] != 'jpg':
                        print os.path.join(parent, dirname, img)
                        os.remove(os.path.join(parent, dirname, img))
        else:
            break


def createPairs(rootdir, one_match=10, one_dis_match=20):
    match = []
    file_Path = os.path.join(rootdir, 'pairs.txt')
    if os.path.exists(file_Path):
        os.remove(file_Path)

    for parent, dirnames, filenames in os.walk(rootdir):
        if len(dirnames) != 0:
            foldername = dirnames[:]
        else:
            break
    for dirname in foldername:
        image_list = getFileList(os.path.join(rootdir, dirname))
        listLen = len(image_list)
        if listLen != 0:
            # matchNum = listLen/2
            matchSet = range(listLen)
            for i in range(one_match):
                randIndex = int(random.uniform(0, len(matchSet)))
                name1 = image_list[matchSet[randIndex]].split('.')[0]
                del (matchSet[randIndex])

                randIndex = int(random.uniform(0, len(matchSet)))
                name2 = image_list[matchSet[randIndex]].split('.')[0]
                del (matchSet[randIndex])

                recordStr = dirname + '\t' + name1 + '\t' + name2 + '\n'
                match.append(recordStr)
    disMatchPerson = len(foldername) / 2
    personSet = range(len(foldername))
    for i in range(disMatchPerson):
        randIndex = int(random.uniform(0, len(personSet)))
        name1 = foldername[personSet[randIndex]]
        del (personSet[randIndex])

        randIndex = int(random.uniform(0, len(personSet)))
        name2 = foldername[personSet[randIndex]]
        del (personSet[randIndex])

        list1 = getFileList(os.path.join(rootdir, name1))
        listLen1 = len(list1)

        list2 = getFileList(os.path.join(rootdir, name2))
        listLen2 = len(list2)

        if listLen1 < one_dis_match or listLen2 < one_dis_match:
            continue
        matchSet1 = range(listLen1)
        matchSet2 = range(listLen2)
        for j in range(one_dis_match):
            randIndex = int(random.uniform(0, len(matchSet1)))
            index1 = list1[matchSet1[randIndex]].split('.')[0]
            del (matchSet1[randIndex])
            randIndex = int(random.uniform(0, len(matchSet2)))
            index2 = list2[matchSet2[randIndex]].split('.')[0]
            del (matchSet2[randIndex])
            dismatchRec = name1 + '\t' + index1 + '\t' + name2 + '\t' + index2 + '\n'
            match.append(dismatchRec)

    # 写入文件
    with open(file_Path, 'a+') as train_fid:
        train_fid.writelines(match)


def CreateDataListNoArg(rootdir, train_port=1.0, test_port=0.1):
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
                if re.match('temp', dirname):
                    continue
                image_list = getFileList(os.path.join(parent, dirname))
                dataLen = len(image_list)

                testNum = max(int(dataLen * test_port), 1)
                trainNum = int(dataLen * train_port)

                trainingSet = range(dataLen)
                for i in range(testNum):
                    randIndex = int(random.uniform(0, len(trainingSet)))
                    print  dirname
                    print "randIndex = " , randIndex
                    print "length = ", len(trainingSet)
                    recordStr = dirname + os.sep + image_list[trainingSet[randIndex]] + ' ' + str(labelIndex) + '\n'
                    testSet.append(recordStr)
                    del (trainingSet[randIndex])

                if trainNum == dataLen: # 如果训练样本需要包含整个样本集合，否则剔除测试样本后，在选择训练样本
                    trainingSet = range(dataLen)
                for i in range(trainNum):
                    randIndex = int(random.uniform(0, len(trainingSet)))
                    recordStr = dirname + os.sep + image_list[trainingSet[randIndex]] + ' ' + str(labelIndex) + '\n'
                    trainSet.append(recordStr)
                    del (trainingSet[randIndex])
                print labelIndex  # 本次循环有效
                labelIndex += 1
        else:
            break
    # 写入文件
    with open(trainPath, 'a+') as train_fid:
        train_fid.writelines(trainSet)
    with open(valPath, 'a+') as test_fid:
        test_fid.writelines(testSet)


def PartitionList(input_list, list_len):
    list_pos = []
    whole_set = range(list_len)
    for index in range(list_len / 2):
        randIndex = int(random.uniform(0, len(whole_set)))
        img_select = input_list[whole_set[randIndex]]
        list_pos.append(img_select)
        del (whole_set[randIndex])
        # del (input_list[whole_set[randIndex]])
    list_neg = list(set(input_list).difference(set(list_pos)))
    return list_pos, list_neg


def CreateTrainTest(root, train_port=1.0, test_port=0.1):
    # labelIndex = 0
    trainPath = os.path.join(root, 'train.txt')
    valPath = os.path.join(root, 'val.txt')
    trainSet = []
    valSet = []
    posSet = []
    negSet = []
    if os.path.exists(trainPath):
        os.remove(trainPath)
    if os.path.exists(valPath):
        os.remove(valPath)
    for parent, dirnames, filenames in os.walk(root):
        dir_Num = len(dirnames)
        if 0 == dir_Num:
            break
        else:
            if 1 == dir_Num % 2:
                dir_Num -= 1
            for i in range(0, dir_Num, 2):
                img_list_i = getFileList(os.path.join(parent, dirnames[i]))
                img_list_j = getFileList(os.path.join(parent, dirnames[i+1]))

                img_list_i_pos, img_list_i_neg = PartitionList(img_list_i, len(img_list_i))
                img_list_j_pos, img_list_j_neg = PartitionList(img_list_j, len(img_list_j))
                
                pos_len = min(len(img_list_i_pos), len(img_list_j_pos))
                if 1 == pos_len % 2:
                    pos_len -= 1
                for index_pos in range(0, pos_len, 2):
                    recordStr1 = dirnames[i] + os.sep + img_list_i_pos[index_pos] + ' ' + str(i) + '\n' + \
                                 dirnames[i] + os.sep + img_list_i_pos[index_pos + 1] + ' ' + str(i) + '\n'
                   
                    recordStr2 = dirnames[i+1] + os.sep + img_list_j_pos[index_pos] + ' ' + str(i+1) + '\n' + \
                                 dirnames[i+1] + os.sep + img_list_j_pos[index_pos + 1] + ' ' + str(i+1) + '\n'
                  
                    posSet.append(recordStr1)
                    posSet.append(recordStr2)
                   
                print "pos i = ", i
                neg_len = min(len(img_list_i_neg), len(img_list_j_neg))
                for index_neg in range(neg_len):
                    recordStr1 = dirnames[i] + os.sep + img_list_i_neg[index_neg] + ' ' + str(i) + '\n' + \
                                 dirnames[i + 1] + os.sep + img_list_j_neg[index_neg] + ' ' + str(i + 1) + '\n'
                    negSet.append(recordStr1)
                print "neg i = ", i+1
    
    sampleLen = min(len(posSet), len(negSet))
    trainNum = int(sampleLen * train_port)
    valNum = int(sampleLen * test_port)
    
    trainingSet = range(sampleLen)
    for index in range(valNum):
        randIndex = int(random.uniform(0, len(trainingSet)))
        recordStr_p = posSet[trainingSet[randIndex]]
        valSet.append(recordStr_p)
        recordStr_n = negSet[trainingSet[randIndex]]
        valSet.append(recordStr_n)
        del (trainingSet[randIndex])
    if trainNum == sampleLen:
        trainingSet = range(sampleLen)
    for i in range(trainNum):
        randIndex = int(random.uniform(0, len(trainingSet)))
        # print "i = ", i, ", randindex = ", randIndex
        # print len(trainingSet)
        # print "trainingSet[randIndex] = ", trainingSet[randIndex]
        recordStr_p = posSet[trainingSet[randIndex]]
        trainSet.append(recordStr_p)
        recordStr_n = negSet[trainingSet[randIndex]]
        trainSet.append(recordStr_n)
        del (trainingSet[randIndex])
        
    with open(trainPath, 'a+') as train_fid:
        train_fid.writelines(trainSet)
    with open(valPath, 'a+') as test_fid:
        test_fid.writelines(valSet)
        
                                    
if __name__ == '__main__':
    # str = [u'F:\Asianperson\人脸提交给王雷20170113下午']
    # root_dir = r'D:\image\rrr'
    root_dir = r'E:\new_webface'
    # CreateTrainTest(root_dir, 0.95, 0.05)
    # createPairs(root_dir, 10, 20)
    CreateDataListNoArg(root_dir, 1.0, 0.1)
    # the first param is rootdir
    # the second param is weather delete the image whose ext is not .jpg
    # the third param is low thresh value
    # the forth param is low thresh value
    """
    argc = len(sys.argv)
    if argc <= 1:
        print 'less param count'
    elif argc == 2:
        root_dir = sys.argv[1]
        ExpandImage([root_dir], 20, 100)
    elif argc == 3:
        root_dir = sys.argv[1]
        if int(sys.argv[2]) == 1:
            deleteImage(root_dir)
        ExpandImage([root_dir], 20, 100)
    elif argc == 4:
        root_dir = sys.argv[1]
        if int(sys.argv[2]) == 1:
            deleteImage(root_dir)
        lowThresh = int(sys.argv[3])
        ExpandImage([root_dir], lowThresh, 100)
    elif argc == 5:
        root_dir = sys.argv[1]
        if int(sys.argv[2]) == 1:
            deleteImage(root_dir)
        lowThresh = int(sys.argv[3])
        highThresh = int(sys.argv[4])
        ExpandImage([root_dir], lowThresh, highThresh)
    else:
        print "too many params"
    """
    # rootdir = r'F:\YanZhengSample'
    # createPairs(rootdir)
