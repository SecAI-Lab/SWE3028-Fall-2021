#!/usr/bin/env python
# coding: utf-8



### Module Import ###

import yfinance as yf
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px
import tensorflow as ft
import os
import os.path
import pandas as pd
import seaborn
from datetime import datetime
from plotly.subplots import make_subplots
from tqdm import tqdm
import numpy as np
from PIL import Image
from numpy import asarray
from keras import backend as K
import cv2


def predict(stockName):
    ### Input Stock-name ###

    stock_name = input("Write your stock name: ")
    stock = yf.Ticker(stock_name)

    stock_history = stock.history(period="5d", interval="15m")
    stock_history_2 = stock.history(period="250d", interval="1h")
    #print(stock_history)

    df_stock = stock_history
    df_stock_2 = stock_history_2



    ### Candle-stick Image for CNN ###

    img_size= 350
    data = [[0] for _ in range(50)]
    df_open=[]
    df_high=[]
    df_low=[]
    df_close=[]
    df_blank = [i for i in range(50)]

    for i in range(50):
        df_open.append(df_stock['Open'][len(df_stock)-(4*i)-1])
        df_high.append(df_stock['High'][len(df_stock)-(4*i)-1]) 
        df_low.append(df_stock['Low'][len(df_stock)-(4*i)-1]) 
        df_close.append(df_stock['Close'][len(df_stock)-(4*i)-1]) 

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Candlestick(x=df_blank,
                    open=df_open,
                    high=df_high,
                    low=df_low,
                    close=df_close,
                    increasing_line_color='red',
                    decreasing_line_color='blue',
                    showlegend=False),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df_blank,
                    y=df_close,
                    mode="lines",
                    line_color='black',
                    showlegend=False),
                 row=1, col=1)

    fig.update_layout(height=img_size, 
                      width=img_size, 
                      xaxis_rangeslider_visible=False, 
                      plot_bgcolor="white")

    fig.layout.xaxis.color = 'white'
    #fig.show()



    ### CNN Input ###

    fig.write_image("./img.png")
    input_CNN = []

    image = Image.open('./img.png').convert('RGB')

    img_data = np.asarray(image)
    img_data = img_data/255.0
    input_CNN.append(img_data)
    input_CNN = np.array(input_CNN).reshape(1,img_size,img_size,3)




    ### LSTM Input ###

    input_LSTM=[]
    for i in range(50):
        input_LSTM.append(np.log10(df_close[i]))

    input_LSTM = np.array(input_LSTM).reshape(1,50,1)



    ### CNN / LSTM dataset for calculate Correction Constant ###

    data2 = [[0]  for _ in range(100)]
    for i in range(100):
        if(i+51>=len(df_stock_2)):
            break
        else:
            df1 = df_stock_2.iloc[i:i+50]
            df2 = df_stock_2.iloc[i+51]  

            data2[i][0] = np.array(np.log10(df2['Close']))

            fig = make_subplots(rows=1, cols=1)
            fig.add_trace(go.Candlestick(x=df_blank,
                            open=df1['Open'],
                            high=df1['High'],
                            low=df1['Low'],
                            close=df1['Close'],
                            increasing_line_color='red',
                            decreasing_line_color='blue',
                            showlegend=False),
                        row=1, col=1)

            fig.add_trace(go.Scatter(x=df_blank,
                            y=df1['Close'],
                            mode="lines",
                            line_color='black',
                            showlegend=False),
                         row=1, col=1)

            fig.update_layout(height=img_size, 
                              width=img_size, 
                              xaxis_rangeslider_visible=False, 
                              plot_bgcolor="white")

            fig.layout.xaxis.color = 'white'

            fig.write_image("./%d.png"%i)


    X_CNN = []
    Y_CNN = []

    for i in range(100):
        image_CNN = Image.open('./%d.png'%i).convert('RGB')
        img_data_CNN = np.asarray(image_CNN)
        img_data_CNN = img_data_CNN/255.0
        X_CNN.append(img_data_CNN)
        Y_CNN.append(data2[i])

    X_CNN = np.array(X_CNN)
    Y_CNN = np.array(Y_CNN)

    X_LSTM=[]
    Y_LSTM=[]

    for i in range(100):
        X_LSTM.append(np.log10(df_stock_2.iloc[i:i+50]['Close']))
        Y_LSTM.append(np.log10([df_stock_2.iloc[i+51]['Close']]))

    X_LSTM = np.array(X_LSTM)
    Y_LSTM = np.array(Y_LSTM)      




    ### Model & Weight ###

    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D,MaxPooling2D,Flatten,Dense
    from tensorflow.keras.layers import Dense, Dropout, Activation, BatchNormalization
    class ResidualUnit(tf.keras.layers.Layer):
      def __init__(self, filters, strides=1, activation ='relu', **kwargs):
        super().__init__(**kwargs)
        self.activation = tf.keras.activations.get(activation)
        self.filters = filters
        self.strides = strides
        self.main_layers = [
                            tf.keras.layers.Conv2D(filters, 3, strides=strides, padding='same', use_bias =False),
                            tf.keras.layers.BatchNormalization(),
                            self.activation,
                            tf.keras.layers.Conv2D(filters, 3, strides=1, padding='same', use_bias = False),
                            tf.keras.layers.BatchNormalization()
        ]
        self.skip_layers =[
                           tf.keras.layers.Conv2D(filters, 1, strides=strides, use_bias = False),
                           tf.keras.layers.BatchNormalization()
        ]

        def get_config(self):
            config = super().get_config()
            config.update({
                "activation": self.activation,
                "strides": self.strides,
                "filters": self.filters,
            })
            return config

        def call(self, inputs):
          Z = inputs
          for layers in self.main_layers:
            Z = layer(Z)

          skip_Z = inputs
          for layer in self.skip_layers:
            skip_Z = layer(skip_Z)
          return self.activation(Z + skip_Z)


    inputs_CNN = tf.keras.Input(shape=(img_size,img_size,3))

    conv1_layer = tf.keras.layers.Conv2D(64, 7, strides=2, input_shape=[img_size, img_size, 3], padding = 'same', use_bias=False)(inputs_CNN)
    max_pool_layer1 = tf.keras.layers.MaxPool2D(
            pool_size=(3, 3), padding='VALID', strides=(2, 2),
            name="MaxPooling"
        )(conv1_layer)
    BN1 = tf.keras.layers.BatchNormalization()(max_pool_layer1)
    Relu1 = tf.keras.layers.Activation('relu')(BN1)
    max_pool_layer2 = tf.keras.layers.MaxPooling2D(pool_size=3, strides=2)(Relu1)
    prev_filters = 64


    ResnetList = []
    ResnetList.append(ResidualUnit(filters = 64, strides= 1)(max_pool_layer2))
    for i, filters in enumerate([64]*2 + [128]*4 + [256] *6 + [512]*3):
        strides = 1 if filters == prev_filters else 2
        ResnetList.append(ResidualUnit(filters = filters, strides= strides)(ResnetList[i]))
        prev_filters = filters


    extractLayer = tf.keras.layers.Conv2D(512, 1, strides=1, input_shape=[87, 87, 512], padding = 'same', use_bias=False)(ResnetList[-1])
    GA = tf.keras.layers.GlobalAveragePooling2D()(extractLayer)
    flatten_CNN = tf.keras.layers.Flatten()(GA)
    from tensorflow.keras import layers, models
    def create_lstm_model(log_inputs: tf.keras.Input) -> layers.Layer:
        lstm_layer_1 = layers.LSTM(50, batch_input_shape=(None, 50, 1), return_sequences=True)(log_inputs)
        lstm_layer_2 = layers.LSTM(50, batch_input_shape=(None, 50, 50))(lstm_layer_1)
        flatten_layer = layers.Flatten()(lstm_layer_2)
        full_connected_1 = layers.Dropout(0.5)(
            layers.Dense(500, activation='relu', use_bias=True)(flatten_layer)
        )
        full_connected_2 = layers.Dropout(0.5)(
            layers.Dense(100, activation='relu', use_bias=True)(full_connected_1)
        )
        full_connected_3 = layers.Dropout(0.5)(
            layers.Dense(25, activation='relu', use_bias=True)(full_connected_2)
        )
        output_layer = layers.Dense(1, activation='linear')(full_connected_3)
        return output_layer, flatten_layer


    inputs_LSTM = tf.keras.Input(shape=(50, 1))

    _, cell_output = create_lstm_model(inputs_LSTM)

    combined_feature = layers.Concatenate(
                axis=1)([cell_output, flatten_CNN])
    flatten_layer = layers.Flatten()(combined_feature)

    full_connected_1 = layers.Dropout(0.5)(
                layers.Dense(500, activation='relu', use_bias=True)(flatten_layer)
            )
    full_connected_2 = layers.Dropout(0.5)(
                layers.Dense(100, activation='relu',
                             use_bias=True)(full_connected_1)
            )
    full_connected_3 = layers.Dropout(0.5)(
                layers.Dense(25, activation='relu',
                             use_bias=True)(full_connected_2)
            )
    lstm_cnn_output = layers.Dense(
                1, activation='linear')(full_connected_3)

    lstm_cnn_model = models.Model(
                inputs=[inputs_LSTM, inputs_CNN], outputs=lstm_cnn_output
            )


    ### Load Weight ###

    model = models.Model(
                inputs=[inputs_LSTM, inputs_CNN], outputs=lstm_cnn_output
            )
    model.load_weights('./%s.h5' %stock_name)




    ### Calculate Correction Constant ###

    predictions = lstm_cnn_model.predict([X_LSTM, X_CNN])
    predictions = np.array(predictions)


    gap_ratio = []
    gap_sign = []
    for i in range(len(Y_LSTM)):
        gap_ratio.append(abs(Y_LSTM[i] - predictions[i])) 
        gap_sign.append(Y_LSTM[i] - predictions[i])
    gap_avg = sum(gap_ratio) / len(Y_LSTM)
    sign = sum(gap_sign)
    deviation = np.std(gap_sign)

    if sign > 0:
        pred_ex = 10**(predictions + gap_avg * (1 + deviation))
    else:
        pred_ex = 10**(predictions - gap_avg * (1 - deviation))

    real_ex = 10**Y_LSTM
    error = []
    for i in range(len(real_ex)):
        error.append(abs(real_ex[i] - pred_ex[i]))

    error_avg = sum(error) / len(error)




    ### Predict & Calculate Ratio of surge/plunge ###

    pred_stock_price = model.predict([input_LSTM, input_CNN])
    latest_stock_price = input_LSTM[0,-1,0]

    if sign > 0:
        pred = 10**(pred_stock_price + gap_avg * (1 + deviation))
    else:
        pred = 10**(pred_stock_price - gap_avg * (1 - deviation))

    stock_ratio_up = (pred - 10**latest_stock_price + error_avg)/(10**latest_stock_price) * 100 
    stock_ratio_down = (pred - 10**latest_stock_price - error_avg)/(10**latest_stock_price) * 100
    #print("Stock price's ratio is: %.2f < X < %.2f" %(stock_ratio_down,stock_ratio_up))

    # stock_ratio > 0 : surge
    # stock_ratio < 0 : plunge




    ### Heatmap ###

    def gradCAM(orig, intensity=0.5, res=350):
        image = Image.open(orig).convert('RGB')
        temp=[]
        d = np.asarray(image)
        d = d/255.0
        d = d.reshape(1,350,350,3)
        temp.append(d)
        data=np.array(np.array(temp[0])).reshape(1,img_size,img_size,3)
        data_LSTM = input_LSTM           
        preds = lstm_cnn_model.predict([data_LSTM, data])

        lstm_cnn_model.inputs = [data_LSTM, data]
        with tf.GradientTape() as tape:
            #conv_layer = model_CNN.get_layer(index=20)
            conv_layer = extractLayer
            iterate = tf.keras.models.Model(lstm_cnn_model.input, [lstm_cnn_model.output, conv_layer])
            model_out, conv_layer = iterate([data_LSTM, data])
            class_out = model_out[:,np.argmax(model_out[0])]
            grads = tape.gradient(model_out, conv_layer)
            pooled_grads = K.mean(grads, axis=(0, 1))
            # pooled_grads = tf.reduce_mean(grads, axis=(0,1))
            pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))

        heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_layer), axis=-1)
        heatmap = np.maximum(heatmap, 0)

        if(np.max(heatmap) != 0):
            heatmap /= np.max(heatmap)

        heatmap = heatmap.reshape((43, 43))

        img = cv2.imread(orig, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = cv2.applyColorMap(np.uint8(255*heatmap), cv2.COLORMAP_JET)

        overlayed = cv2.addWeighted(img, 1, heatmap, 0.75, 0)
        combined = np.concatenate((img,heatmap,overlayed),axis=1)

        img = heatmap * intensity + img

        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        #plt.imshow(image, alpha=.6)
        #plt.imshow(heatmap, alpha=.6)
        plt.savefig('./heatmap.png')
        
        final_img = Image.open('./heatmap.png')
        
    image_gradCAM = './img.png'
    gradCAM(image_gradCAM)    


    ### Image removal ###

    os.remove('./heatmap.png')
    os.remove('./img.png')

    for i in range(100):
        os.remove('./%d.png' %i)
        
    
    return {'val_upper': stock_ratio_up, 'val_lower' : stock_ratio_down 'plt' : final_img}

