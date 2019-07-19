import random
import itertools
import numpy as np
import matplotlib.pyplot as plt

cars = ["hiro", "shiori", "asako", "kyoko", "yukio", "miyako"]
tvos = [20, 40, 80]
vsps = [40, 60, 80, 120]
funcs = ["one", "two"]
weights = [1.0, 0.5]

def get_eval():
    return (int(random.random()*10), int(random.random()*100))

data = np.empty((len(vsps), len(tvos), len(cars), len(funcs)), float)

for i, j, k in itertools.product(range(len(vsps)), range(len(tvos)), range(len(cars))):
    data[i, j, k] = get_eval()

data = np.transpose(data, axes=(0, 1, 3, 2))
data_std = 50 + data / np.std(data, axis=3, keepdims=True) * 10
weights_t = np.reshape(weights, (-1, 1))
data_std_weighted = data_std * weights_t
func_total = np.sum(data_std_weighted, axis=2)
func_rank = np.argsort(-func_total, axis=2)
tvo_total = np.sum(func_total, axis=1)
tvo_rank = np.argsort(-tvo_total, axis=1)



pos = 1
x = np.arange(len(cars))
car_label = np.array(cars)
for i, j in itertools.product(range(len(vsps)), range(len(tvos))):
    bottom = np.zeros(len(cars))
    plt.subplot(len(vsps), len(tvos), pos)
    plt.xticks(x, car_label[func_rank[i,j]])
    for k in range(len(funcs)):
        plt.bar(x, data_std_weighted[i,j,k][func_rank[i,j]], 0.5, bottom)
        bottom += data_std_weighted[i,j,k][func_rank[i,j]]
    pos += 1

plt.show()

