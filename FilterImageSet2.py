# -*-coding:utf-8 -*-

import numpy as np
import caffe
import os.path
import shutil
import re


def GetFileList(dir_name):
	imgList = os.listdir(dir_name)
	if 'Thumbs.db' in imgList:
		imgList.remove('Thumbs.db')
	return imgList

opt = {
    'debug': False,
    'caffeMode': 'gpu',
    'batchSize': 1,
    'inputWidth': 96,
    'inputHigh': 112,
    'net': 'ResNet',
	'rootdir': r'F:\china_face\Asian_face',
	'calcuFeature': True,
	'findBestBaseImg': False,
	'filteImage': False,
}

if opt['caffeMode'] == 'cpu':
    caffe.set_mode_cpu()
else:
    caffe.set_device(0)
    caffe.set_mode_gpu()

if opt['net'] == 'ResNet':
    model_def = './face_deploy.prototxt'
    # model_def = './face_deploy_halfout_no_five.prototxt'
    # model_def = './deploy.prototxt'
    model_weights = './face_train_test_iter_28000_whole.caffemodel'
    # model_weights = './googlenet_train_iter_320000.caffemodel'
else:
    print '[Error] no model exist'
    exit()
net = caffe.Net(model_def, model_weights, caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2, 1, 0))
transformer.set_mean('data', np.array([127.5, 127.5, 127.5]))
transformer.set_input_scale('data', 0.0078125)
net.blobs['data'].reshape(opt['batchSize'], 3, opt['inputHigh'], opt['inputWidth'])

testThresh = 0.466921

if opt['calcuFeature']:
	for parent, dirnames, filenames in os.walk(opt['rootdir']):
		if len(dirnames) != 0:
			for dirname in dirnames:
				if re.match('temp', dirname):
					continue
				similarityArr = []
				image_list = GetFileList(os.path.join(parent, dirname))
				for img in image_list:
					img_path = os.path.join(parent, dirname, img)
					image = caffe.io.load_image(img_path)
					transformed_image = transformer.preprocess('data', image)
					net.blobs['data'].data[...] = transformed_image
					output = net.forward()  # 这里output是CNN最后一层的输出向量
					feature = net.blobs['fc5'].data.copy().flatten()
					similarityArr.append(feature)
				saved_name = os.path.join(parent, dirname + '.npy')
				np.save(saved_name, np.array(similarityArr))
				print 'end culculate feature: ' + dirname
		else:
			break

if opt['findBestBaseImg']:
	for parent, dirnames, filenames in os.walk(opt['rootdir']):
		if len(dirnames) != 0:
			for dirname in dirnames:
				if re.match('temp', dirname):
					continue
				maxValue = 0
				maxValue_index = 0
				image_list = GetFileList(os.path.join(parent, dirname))
				data_a = np.load(os.path.join(opt['rootdir'], dirname+'.npy'))
				recordStr = []
				for i in range(len(image_list)):
					similarity_sum = 0.0
					for j in range(len(image_list)):
						feature1 = data_a[i]
						feature2 = data_a[j]
						similarity = np.dot(feature1, feature2.T) / (
						np.linalg.norm(feature1) * np.linalg.norm(feature2))
						similarity_sum += similarity
					tempStr = dirname + os.sep + image_list[i] + " " + str(similarity_sum) + '\n'
					recordStr.append(tempStr)
					if similarity_sum > maxValue:
						maxValue = similarity_sum
						maxValue_index = i
				tempStr = str(maxValue_index) + ' ' + dirname + os.sep + image_list[maxValue_index] + " " + str(maxValue) + '\n'
				recordStr.insert(0, tempStr)
				recordTxt = 'temp_best_txt'
				recordTxt = os.path.join(parent, recordTxt, dirname+'.txt')
				with open(recordTxt, 'w') as fid:
					fid.writelines(recordStr)
				shutil.copy(os.path.join(parent, dirname, image_list[maxValue_index]), os.path.join(parent, 'temp_best', image_list[maxValue_index]))
				os.rename(os.path.join(parent, 'temp_best', image_list[maxValue_index]), os.path.join(parent, 'temp_best', dirname+ '_' +image_list[maxValue_index]))
				print 'end find best image: ' + dirname
		else:
			break
if opt['filteImage']:
	for parent, dirnames, filenames in os.walk(opt['rootdir']):
		if len(dirnames) != 0:
			for dirname in dirnames:
				if re.match('temp', dirname):
					continue
				image_list = GetFileList(os.path.join(parent, dirname))
				data_a = np.load(os.path.join(opt['rootdir'], dirname+'.npy'))
				txt_str = os.path.join(os.path.join(parent, 'temp_best_txt', dirname + '.txt'))
				recordStrArr = []
				if os.path.exists(txt_str):
					txtfile = file(txt_str, 'r')
					lines = txtfile.readline()
					lineArr = lines.strip().split(" ")
					if len(lineArr) != 3:
						print "txt format is invalid"
						continue
					base_index = int(lineArr[0])
				else:
					base_index = 0
				feature_base = data_a[base_index]
				for i in range(len(image_list)):
					feature_other = data_a[i]
					similarity = np.dot(feature_base, feature_other.T) / (np.linalg.norm(feature_base) * np.linalg.norm(feature_other))
					recordStr = os.path.join(dirname, image_list[i])
					recordStr += ' ' + str(similarity) + '\n'
					recordStrArr.append(recordStr)
				recordTxt = dirname + '.txt'
				recordTxt = os.path.join(parent, recordTxt)
				with open(recordTxt, 'w') as fid:
					fid.writelines(recordStrArr)
				print dirname
		else:
			break

