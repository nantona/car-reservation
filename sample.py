import random
import collections
import dataclasses
import itertools
import numpy as np
import matplotlib.pyplot as plt
import evalfuncs as ef

cars = ["hiro", "shiori", "asako", "kyoko", "yukio", "miyako"]
tvos = [20, 40, 80]
vsps = [40, 60, 80, 120]
funcs = ["one", "two"]
#weights = [1.0, 0.5]

persons_eval = [
    [10, 20, 30, 40, 50, 60],
    [10, 20, 30, 40, 50, 60],
    [10, 20, 30, 40, 50, 60],
]


@dataclasses.dataclass
class Scores:
    score : np.ndarray
    func_total : np.ndarray
    func_rank : np.ndarray
    tvo_total : np.ndarray
    tvo_rank : np.ndarray

cache = {}

def read_csv(filepath):
    if filepath in cache:
        return cache[filepath]
    else:
        pass

def get_eval():
    return (int(random.random()*10), int(random.random()*100))


# スコアを計算する
def calc_score():
    data = np.empty((len(vsps), len(tvos), len(cars), len(funcs)), float)

    for i, j, k in itertools.product(range(len(vsps)), range(len(tvos)), range(len(cars))):
        data[i, j, k] = get_eval()

    # 処理しやすいようにデータ配列を転置
    data = np.transpose(data, axes=(0, 1, 3, 2))

    # 評価値毎に偏差値に変換
    data_std = 50 + data / np.std(data, axis=3, keepdims=True) * 10

    # 偏差値に重みをつける
    weights_t = np.reshape(ef.weights, (-1, 1))
    score = data_std * weights_t

    # 評価を合算しアクセル開度毎に総合評価値を計算する
    # ランキングもつけておく
    func_total = np.sum(score, axis=2)
    func_rank = np.argsort(-func_total, axis=2)

    # アクセル開度の総合評価を合算し、車速毎に総合評価値を計算する
    tvo_total = np.sum(func_total, axis=1)
    tvo_rank = np.argsort(-tvo_total, axis=1)

    result = Scores(score, func_total, func_rank, tvo_total, tvo_rank)
    return result


# グラフを作成する
def plot_scores(d):
    pos = 1
    x = np.arange(len(cars))
    car_label = np.array(cars)
    for i, j in itertools.product(range(len(vsps)), range(len(tvos))):
        bottom = np.zeros(len(cars))
        plt.subplot(len(vsps), len(tvos), pos)
        plt.xticks(x, car_label[d.func_rank[i,j]])
        for k in range(len(funcs)):
            plt.bar(x, d.score[i,j,k][d.func_rank[i,j]], 0.5, bottom)
            bottom += d.score[i,j,k][d.func_rank[i,j]]
        pos += 1

    plt.show()


# 相関係数の算出
def calc_coeff(d):
    result = []
    tgt = d.func_total[0]
    for score, person in zip (tgt, persons_eval):
        result.append(np.corrcoef(score, person)[0,1])
    return result


#plot_scores(calc_score())
#result = calc_score()
#print(calc_coeff(result))

weight_pattern = np.arange(0.1, 0.3, 0.1)
ratio_pattern = [(5, f) for f in np.arange(0.0, 35.0, 5.0)]

with open("result.txt", mode="w") as outfile:
    for w1, w2, w3, m in itertools.product(weight_pattern, weight_pattern, weight_pattern, ratio_pattern):
        ef.weights = [w1, w2]
        result = calc_coeff(calc_score())
        outline = f"{w1}, {w2}, {w3}, {m[0]}, {m[1]} {result[0]}, {result[1]}, {result[2]}\n"
        outfile.write(outline)
