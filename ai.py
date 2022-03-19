from keras.models import load_model
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from solve_cudnn_error import *
solve_cudnn_error()
label = np.array(['not','tissue'])
# 載入模型
model = load_model('final3_tissue3.h5')
# 導入圖片
input_shape = model.input_shape[1:3]

def predict_image_with_path(path,thresh=0.6):

	img = load_img(path, target_size=input_shape, interpolation='lanczos')
	img = img_to_array(img) / 255.
	#print(img)
	conf = model.predict(img.reshape(-1, *img.shape))[0][0]
	conf = round(conf,3)
	print(img)	
	thing = '不是' if conf < thresh else '是'
	return thing+'衛生紙','辨別為衛生紙的機率是:',conf

#print(predict_image_with_path('2351411.jpg'))

