import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import math
from sklearn.metrics import mean_squared_error, r2_score

##Read data
data = pd.read_excel("/content/BTC2.xlsx")
data = data.set_index('Tarih')
dataset = data.values

##Scale data

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

##Prepare train data
training_data_len = math.ceil(len(dataset) * .8)
train_data = scaled_data[0:training_data_len, :]

x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

##using callback
tf.keras.callbacks.EarlyStopping(
    'val_loss',
    min_delta=0,
    patience=3,
    verbose=1,
    restore_best_weights=True)

es_callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

##Build the model
model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=["accuracy"])
model.fit(x_train, y_train, epochs=100, validation_split=0.2, callbacks=[es_callback])

##Prepare test data
test_data = scaled_data[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, :]
for y in range(60, len(test_data)):
    x_test.append(test_data[y - 60:y, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

##Measure prediction rate
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
print(r2_score(y_test, predictions))

##Training, Test, Prediction in the chart
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Tahminler'] = predictions

plt.figure(figsize=(16, 8))
plt.title('model')
plt.xlabel('Tarih', fontsize=18)
plt.ylabel('Açılış Fiyatları', fontsize=18)
plt.plot(data['Açılış'], color="purple")
plt.plot(valid[['Açılış', 'Tahminler']])
plt.legend(['Eğitim', 'Değer', 'Tahminler'], loc='lower right')
plt.show()

## Only test and prediction in the chart
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Tahminler'] = predictions

plt.figure(figsize=(16, 8))
plt.title('model')
plt.xlabel('Tarih', fontsize=18)
plt.ylabel('Açılış Fiyatları', fontsize=18)
plt.plot(data['Açılış'], color="purple")
plt.plot(valid[['Açılış', 'Tahminler']])
plt.legend(['Eğitim', 'Değer', 'Tahminler'], loc='lower right')
plt.show()

##Prepare data
dataset = data.values
training_data_len = math.ceil(len(dataset) * .8)
train_dataa = dataset[0:training_data_len, :]
test_dataa = dataset[training_data_len - 60:, :]
train_dataa = pd.DataFrame(train_dataa)
train_dataa.rename(columns={0: 'Açılış'}, inplace=True)
test_dataa = pd.DataFrame(test_dataa)
test_dataa.rename(columns={0: 'Açılış'}, inplace=True)
total_dataset = pd.concat((train_dataa["Açılış"], test_dataa["Açılış"]), axis=0)
model_inputs = total_dataset[len(total_dataset) - len(test_data) - 60:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)
real_data = [model_inputs[len(model_inputs) + 1 - 60:len(model_inputs + 1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

##Next day forecast value
prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)

print(f"prediction:{prediction}")
{
    "folders": []
}