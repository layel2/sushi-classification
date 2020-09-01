from PIL import Image
from io import BytesIO
import requests
from tensorflow import keras
#import tensorflow as tf
import numpy as np

#tf.reset_default_graph()

from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
pretrain = MobileNetV2(weights=None,input_shape = (255, 255, 3),include_top=False)

pretrain_out = pretrain.output
x = keras.layers.GlobalAveragePooling2D()(pretrain_out)
x = keras.layers.Dense(256,activation='relu',name='my_dense1')(x)
x = keras.layers.Dropout(0.2)(x)
x = keras.layers.Dense(6,activation='softmax')(x)

model = keras.Model(pretrain.input,x)
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['acc'])

model.load_weights('sushi_mobileNet2.h5')
#model._make_predict_function()
#keras.backend.clear_session()
pred_dict = {0: 'ebi', 1: 'ika', 2: 'ikura', 3: 'maguro', 4: 'salmon', 5: 'uni'}


def urlpred(url):
    r = requests.get(url)
    if r.status_code != 200:
    	return 'Url request error'
    try:
	    img = Image.open(BytesIO(r.content))
	    img = img.resize((255,255))
	    img = np.array(img)/255
	    #tf.reset_default_graph()
	    pred = model.predict(img.reshape(-1,255,255,3))
	    max_pred = np.argmax(pred)
	    proba = pred[0][max_pred]
	    return {'result':pred_dict[max_pred],'prob':float(proba)}
    except :
        return 'Please enter a picture Url'
        
