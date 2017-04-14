# -*-coding:utf-8-*-
# import os
import os.path
import random
import sys

import numpy as np
import matplotlib.pyplot as plt


# 绘制roc曲线
def plot_roc(predict, groundTruth):
    predictArr = np.array(predict)
    groundArr = np.array(groundTruth)

    pos_num = np.sum(groundArr == 1)
    neg_num = np.sum(groundArr == 0)

    m = len(groundTruth)

    index = predictArr.flatten().argsort()
    sorted_predict = np.sort(predictArr.flatten());

    groundArr = groundArr[index]
    x = np.zeros(m+1)
    y = np.zeros(m+1)
    yoden = np.zeros(m)
    auc = 0.0
    x[0] = 1
    y[0] = 1
    yoden[0] = 0

    for i in range(1, m):
        TP = float(np.sum(groundArr[i:] == 1))
        FP = float(np.sum(groundArr[i:] == 0))
        x[i] = FP / neg_num
        y[i] = TP / pos_num
        auc += (y[i] + y[i-1]) * (x[i-1] - x[i]) / 2
        yoden[i] = y[i] + (1 - x[i]) - 1
    x[m] = 0
    y[m] = 0
    auc += y[m - 1] * x[m - 1] / 2

    print 'best thresh value = ', sorted_predict[np.argmax(yoden)]
    # fp = float(np.sum(predictArr.flatten()[0:3000] >= sorted_predict[np.argmax(yoden)]))
    # fn = float(np.sum(predict[:] <  sorted_predict[np.argmax(yoden)]))
    # print 'test acc = ', (fp + fn) / (len(predict) + len(groundTruth))

    plt.title("ROC curve of %s (AUC = %.4f)" % ('face', auc))
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.plot(x, y)  # use pylab to plot x and y
    plt.show()  # show the plot on the screen
    return sorted_predict[np.argmax(yoden)]


def GetData(txt_yes, txt_no):
    matchList = []
    dismatchList = []
    wholelist = []
    groundTrth = []
    try:
        fileObj = open(txt_yes)
        #dismatchlist = []
        for line in fileObj.readlines():
            curLine = line.strip().split()
            if len(curLine) == 1:
                score = float(curLine[0])
                matchList.append(score)
                wholelist.append(score)
                groundTrth.append(1)
            else:
                print 'txt format is invalid'
    except IOError:
        print txt_yes, 'is not exits'
    else:
        print 'succeed'

    try:
        fileObj = open(txt_no)
        for line in fileObj.readlines():
            curLine = line.strip().split()
            if len(curLine) == 1:
                score = float(curLine[0])
                wholelist.append(score)
                dismatchList.append(score)
                groundTrth.append(0)
            else:
                print 'txt format is invalid'
    except IOError:
        print txt_no, 'is not exits'
    else:
        print 'succeed'
    return wholelist, groundTrth,matchList,dismatchList


if __name__ == '__main__':

    # the first param is rootdir
    # the second param is thresh value
    txt_yes = r'D:\LWF_Yes.txt'
    txt_no = r'D:\LWF_No.txt'
    falseNum  = 0
    wholelist,groundtruth, matchList,dismatchList =  GetData(txt_yes, txt_no)
    print len(wholelist)
    print len(groundtruth)
    print len(matchList)
    print len(dismatchList)
    value_thresh =  plot_roc(wholelist, groundtruth)
    for i in matchList:
        if i < value_thresh:
            falseNum += 1
    for i in dismatchList:
        if i > value_thresh:
            falseNum += 1
    print float(falseNum)/len(wholelist)
    print 1 - float(falseNum)/len(wholelist)
    print falseNum


