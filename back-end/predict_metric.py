import os
import random
import time
import json
import torch
import torchvision
import numpy as np
import pandas as pd
import warnings
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime
from torch import nn, optim
from config import config
from collections import OrderedDict
from torch.autograd import Variable
from torch.utils.data import DataLoader
from dataset.dataloader import *
from sklearn.model_selection import train_test_split, StratifiedKFold
from timeit import default_timer as timer
from models.model import *
from utils import *

# 1. set random.seed and cudnn performance
random.seed(config.seed)
np.random.seed(config.seed)
torch.manual_seed(config.seed)
torch.cuda.manual_seed_all(config.seed)
os.environ["CUDA_VISIBLE_DEVICES"] = config.gpus
torch.backends.cudnn.benchmark = True
warnings.filterwarnings('ignore')


# 2. evaluate func
def evaluate(val_loader, model):
    model.cuda()
    model.eval()
    golds = []
    preds = []
    with torch.no_grad():
        for i, (input, target) in enumerate(tqdm(val_loader)):
            input = Variable(input).cuda()
            y_pred = model(input)
            smax = nn.Softmax(1)
            smax_out = np.argmax(smax(y_pred).cpu().numpy(), axis=1)

            golds.extend(target)
            preds.extend(smax_out)

    f1_report = classification_report(golds, preds)
    acc = accuracy_score(golds, preds)

    return f1_report, acc


    # return [losses.avg, top1.avg, top2.avg]


def main():
    fold = 0
    # 4.1 mkdirs
    if not os.path.exists(config.submit):
        os.mkdir(config.submit)
    if not os.path.exists(config.weights):
        os.mkdir(config.weights)
    if not os.path.exists(config.best_models):
        os.mkdir(config.best_models)
    if not os.path.exists(config.logs):
        os.mkdir(config.logs)
    if not os.path.exists(config.weights + config.model_name + os.sep + str(fold) + os.sep):
        os.makedirs(config.weights + config.model_name + os.sep + str(fold) + os.sep)
    if not os.path.exists(config.best_models + config.model_name + os.sep + str(fold) + os.sep):
        os.makedirs(config.best_models + config.model_name + os.sep + str(fold) + os.sep)
        # 4.2 get model and optimizer
    model = get_net()
    # model = torch.nn.DataParallel(model)
    model.cuda()

    # 4.5 get files and split for K-fold dataset
    # 4.5.1 read files
    train_ = get_files(config.train_data, "train")

    train_data_list, val_data_list = train_test_split(train_, test_size=0.15, stratify=train_["label"])

    val_dataloader = DataLoader(ChaojieDataset(val_data_list, train=False), batch_size=config.batch_size, shuffle=True,
                                collate_fn=collate_fn, pin_memory=False)

    best_model = torch.load(
        config.best_models + os.sep + config.model_name + os.sep + str(fold) + os.sep + 'model_best.pth.tar')
    model.load_state_dict(best_model["state_dict"])
    f1_report, acc = evaluate(val_dataloader, model)
    print(f"F1 Report\n{f1_report}\n\nAccuracy:{acc}")


if __name__ == "__main__":
    main()


# 86.5968

#               precision    recall  f1-score   support
#
#            0       0.98      0.96      0.97       203
#            1       0.87      0.75      0.81        36
#            2       0.80      0.77      0.78        26
#            3       0.96      0.97      0.97        73
#            4       0.75      1.00      0.86        24
#            5       1.00      0.29      0.44         7
#            6       0.99      0.99      0.99       102
#            7       0.90      0.95      0.92        19
#            8       0.94      0.84      0.89        19
#            9       0.98      1.00      0.99        64
#           10       0.70      0.58      0.63        33
#           11       0.69      0.62      0.65        29
#           12       0.85      0.89      0.87        83
#           13       0.78      0.84      0.81        61
#           14       0.60      0.81      0.69        36
#           15       0.78      0.79      0.78        85
#           16       1.00      0.99      1.00       140
#           17       1.00      1.00      1.00        50
#           18       0.70      0.66      0.68        65
#           19       0.74      0.76      0.75        79
#           20       0.74      0.90      0.81        87
#           21       0.85      0.65      0.74        72
#           22       0.75      0.30      0.43        10
#           23       0.94      0.99      0.96       108
#           24       1.00      1.00      1.00        63
#           25       0.72      0.81      0.76       315
#           26       0.78      0.67      0.72       309
#           27       0.90      0.88      0.89        43
#           28       0.91      0.93      0.92       147
#           29       0.94      0.91      0.92       132
#           30       0.99      0.98      0.99       176
#           31       0.75      0.78      0.76        49
#           32       0.81      0.86      0.84        65
#           33       0.99      1.00      0.99       245
#           34       0.85      0.94      0.89        35
#           35       0.97      0.90      0.93        87
#           36       0.77      0.93      0.84        43
#           37       0.93      0.82      0.87        77
#           38       1.00      0.98      0.99        42
#           39       0.73      0.82      0.77        33
#           40       0.94      0.89      0.91       100
#           41       1.00      0.99      0.99       207
#           42       0.59      0.75      0.66        55
#           43       0.91      0.83      0.87       166
#           44       0.84      0.88      0.86        43
#           45       0.87      0.91      0.89        76
#           46       0.62      0.80      0.70        45
#           47       0.92      0.85      0.88       190
#           48       0.68      0.93      0.79        56
#           49       0.83      0.59      0.69        58
#           50       1.00      1.00      1.00         7
#           51       0.50      0.50      0.50         4
#           52       0.84      0.88      0.86        72
#           53       0.93      0.88      0.91       138
#           54       0.87      0.85      0.86        93
#           55       0.78      0.70      0.74        46
#           56       0.80      0.79      0.80       242
#           57       0.88      0.89      0.88       424
#           58       0.90      0.98      0.94        45
#
#     accuracy                           0.87      5439
#    macro avg       0.85      0.84      0.83      5439
# weighted avg       0.87      0.87      0.87      5439
