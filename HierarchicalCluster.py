# -*- coding: utf-8 -*-
import numpy as np


def Cosine_distance(vector1, vector2):
    if type(vector1) != 'numpy.ndarray':
        vector1 = np.array(vector1)
    if type(vector2) != 'numpy.ndarray':
        vector2 = np.array(vector2)
    cosDistance = np.dot(vector1, vector2.T) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cosDistance


def LoadMatrix(dataArray):
    if type(dataArray) is not 'numpy.ndarray':
        dataArray = np.array(dataArray)
    distanceMatrix = np.zeros([len(dataArray), len(dataArray)])
    for i in range(len(dataArray)):
        for j in range(i + 1, len(dataArray)):
            distance = 1 - Cosine_distance(dataArray[i], dataArray[j])
            distanceMatrix[i][j] = distance
    return distanceMatrix


def findMinValueOfMatrix(disMat):
    minValue = float('inf')
    leftIndex = 0
    rightIndex = 0
    for i in range(len(disMat)):
        for j in range(i+1, len(disMat)):
            if (minValue > disMat[i][j]) and (disMat[i][j] != 0):
                minValue = disMat[i][j]
                leftIndex = i
                rightIndex = j
    return [leftIndex, rightIndex], minValue


def ProcessHierarchical(filePath):
    cluster = []
    if 'str' == type(filePath):
        return
    else:
        dataMat = LoadMatrix(filePath)
        print "****************datamat src**************"
        print dataMat
        while True:
            nodeTuple, minValue = findMinValueOfMatrix(dataMat)
            if nodeTuple[0] == nodeTuple[1]:
                break
            dataMat[nodeTuple[0]][nodeTuple[1]] = 0
            for i in range(len(dataMat)):
                if dataMat[i][nodeTuple[0]] <= dataMat[i][nodeTuple[1]]:
                    dataMat[i][nodeTuple[1]] = 0
                else:
                    dataMat[i][nodeTuple[0]] = 0
            for i in range(len(dataMat)):
                if dataMat[nodeTuple[0]][i] <= dataMat[nodeTuple[1]][i]:
                    dataMat[nodeTuple[1]][i] = 0
                else:
                    dataMat[nodeTuple[0]][i] = 0
            print "update, clusterCentor = ", nodeTuple[0], nodeTuple[1]
            print dataMat

            cluster.append(nodeTuple)
        selectList = [True] * len(cluster)
        for i in range(len(cluster)):
            if selectList[i]:
                for j in range(i + 1, len(cluster)):
                    if selectList[j]:
                        for item in cluster[j]:
                            if item in cluster[i]:
                                cluster[i].extend(cluster[j])
                                selectList[j] = False
                                break
        for index in range(len(selectList)):
            if selectList[index]:
                print cluster[index]


if __name__ == '__main__':
    tempdata = [[0.7, 1.2], [0.8, 2], [2, 1], [2.6, 0.8], [2.5, 1.5]]
    ProcessHierarchical(tempdata)

