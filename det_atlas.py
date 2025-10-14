import numpy as np
import time as tm
import pickle
# 设置随机种子
seed = 1333
np.random.seed(seed)

import tensorflow as tf
# 打印 TensorFlow 版本，确保使用的是 2.12
print("TensorFlow version:", tf.__version__)
tf.random.set_seed(seed)  # 设置 TensorFlow 随机种子
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence
start_time = None
x_test = []
z_test = []
user_artifact = ''
model = None
maxlen = 400
def init_data():
    global x_test, z_test,user_artifact
    global prediction_counterstart_time
    with open('output/user_artifact.txt') as file:
        user_artifact = file.readline().strip()
    with open('output/x_test.pkl','rb') as file:
        x_test = pickle.load(file)
    with open('output/z_test.pkl','rb') as file:
        z_test = pickle.load(file)

def model_init():
    global model
    print("Saved model output/model.h5 has been loaded!")
    model = load_model('output/model.h5', compile=False)


def predict_labels():
    global classified_words, classified_words_prediction, classified_words_proba
    global prediction, x_test,z_test,model

    filter_result = []
    false_positives = 0
    false_negatives = 0
    correctly_identified = 0
    total_sequences = 0
    predicted_malicious_labels = []
    labels_candidates = []
    prediction = None
    prediction_proba = None
    argmax = None
    init_time = tm.time()
    print("GPU Available:", tf.config.list_physical_devices('GPU'))
    proba_output = model.predict(x_test)
    print(proba_output)
    print("time cost:" + str(tm.time() - init_time))
    prediction = (proba_output > 0.5).astype(int).flatten()
    prediction_proba = proba_output.flatten()
    prediction = prediction.tolist()
    prediction_proba = prediction_proba.tolist()

    for x in range(0, len(prediction)):
        if prediction[x] == 1:
            labels_candidates.append((z_test[x], prediction_proba[x]))
        if prediction[x] == 0 and prediction_proba[x] > 0.5:
            print(z_test[x])

    return predicted_malicious_labels, labels_candidates  # labels_combos
if __name__ == '__main__':
    init_data()
    model_init()
    # print(x_test)
    # print(z_test)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen, padding="post")
    predicted_labels, labels_candidates = predict_labels()
    lll_c = 0
    i_to_del = []
    for lll in labels_candidates:
        if "c:/users/aalsahee/downloads" in lll[0]:
            i_to_del.append(lll_c)
        lll_c += 1

    for iii in reversed(i_to_del):
        del labels_candidates[iii]
    work_list = [[user_artifact]]
    result_labels = {}
    result_labels[1] = [[user_artifact]]
    lll_c = 0
    i_to_del = []
    for lll in labels_candidates:
        llll_c = 0
        for llll in lll[0]:
            if "192.168.223.128" in llll or "192.168.223.130" in llll:
                i_to_del.append(lll_c)
                break
            llll_c += 1
        lll_c += 1

    for iii in reversed(i_to_del):
        del labels_candidates[iii]

    labels_candidates = sorted(labels_candidates, key=lambda x: (x[1]), reverse=True)
    print(labels_candidates)
    for lc in labels_candidates:
        if not lc[0] in work_list:
            work_list.append(lc[0])
            lc0_len = len(lc[0])
            # print(result_labels)
            if lc0_len in list(result_labels):
                if lc[1] >= 0.50:  # 0.85
                    result_labels[lc0_len].append(lc)
            else:
                if lc[1] >= 0.50:  # 0.85
                    result_labels[lc0_len] = [lc]
    for k in list(result_labels):
        # print str(result_labels[k])[:8000] + " ..."
        saveres = "result.txt"
        file_res = open(saveres, "w")
        file_res.write(str(result_labels[k]))
        print(str(result_labels[k]))
        print("---------")
