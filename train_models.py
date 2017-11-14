from preprocessor import preprocessor
from keras_models import piczak_CNN
from keras.callbacks import TensorBoard
from sklearn import metrics
import numpy as np
import pandas as pd
import utils

classes = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 'siren', 'street_music']
train_dirs = []

for i in range(1,11):
    train_dirs.append('fold{0}'.format(i))

def train_keras_cnn(epochs=100, output_model_file="./piczak_model.h5",
                    output_predictions_file="./test.csv"):

    pp = preprocessor(parent_dir='E:/Deep Learning Datasets/UrbanSound8K/audio')
    print("Loading the data...")
    pp.data_prep(train_dirs=train_dirs)

    tb = TensorBoard(log_dir='./TensorBoard')

    print("Building the model...")
    model = piczak_CNN(input_dim=pp.train_x[0].shape, output_dim=pp.train_y.shape[1])

    print("Training the model...")
    model.fit(pp.train_x, pp.train_y, epochs=epochs,
              batch_size=256, validation_split=0.2, verbose=2, callbacks=[tb])

    print("Saving the model to file: {0}".format(output_model_file))
    model.save(output_model_file)

    print("Evaluating test performance...")
    performance = model.evaluate(pp.test_x, pp.test_y, verbose=0)
    print("loss: {0}, test-acc: {1}".format(performance[0], performance[1]))

    print("Writing test predictions to csv file : {0}".format(output_predictions_file))
    def write_preds(preds, fname):
        pd.DataFrame({"Predictions": preds, "Actual": np.argmax(pp.test_y, axis=1)}).to_csv(fname, index=False,
                                                                                          header=True)

    preds = model.predict_classes(pp.test_x, verbose=0)
    write_preds(preds, output_predictions_file)
    confusion_matrix = metrics.confusion_matrix(np.argmax(pp.test_y, axis=1), preds)
    utils.plot_confusion_matrix(confusion_matrix, classes)


if __name__ == '__main__':
    train_keras_cnn()
