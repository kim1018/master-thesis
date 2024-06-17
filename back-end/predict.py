import os
import warnings
import matplotlib.pyplot as plt
from collections import OrderedDict
from torch.autograd import Variable
from torch.utils.data import DataLoader
from dataset.dataloader import *
from models.model import *
from utils import *
import sys




# 1. set random.seed and cudnn performance
random.seed(config.seed)
np.random.seed(config.seed)
torch.manual_seed(config.seed)
torch.cuda.manual_seed_all(config.seed)
os.environ["CUDA_VISIBLE_DEVICES"] = config.gpus
torch.backends.cudnn.benchmark = True
warnings.filterwarnings('ignore')


fold = 0

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def get_data(root):
    # for test
    files = [root]
    files = pd.DataFrame({"filename": files})
    return files


# 3. test model on public dataset and save the probability matrix
def predict(img_path, model):
    # get data()函数里的参数为要预测的图片的保存路径
    test_files = get_data(img_path)
    label_map={
    5
    }

    test_dataloader = DataLoader(ChaojieDataset(test_files, test=True), batch_size=1, shuffle=False, pin_memory=False)
    best_model = torch.load(
        config.best_models + os.sep + config.model_name + os.sep + str(fold) + os.sep + 'model_best.pth.tar', map_location='cpu')
    model.load_state_dict(best_model["state_dict"])
    # 3.1 confirm the model converted to cuda
    csv_map = OrderedDict({"filename": [], "probability": []})
    model.to(device)
    model.eval()
    submit_results = []
    for i, (input, filepath) in enumerate(tqdm(test_dataloader)):
        # 3.2 change everything to cuda and get only basename
        filepath = [os.path.basename(x) for x in filepath]
        with torch.no_grad():
            image_var = Variable(input)
            y_pred = model(image_var)
            smax = nn.Softmax(1)
            smax_out = smax(y_pred)
        # 3.4 save probability to csv files
        csv_map["filename"].extend(filepath)
        for output in smax_out:
            prob = ";".join([str(i) for i in output.data.tolist()])
            csv_map["probability"].append(prob)
    result = pd.DataFrame(csv_map)
    result["probability"] = result["probability"].map(lambda x: [float(i) for i in x.split(";")])
    for index, row in result.iterrows():
        pred_label = np.argmax(row['probability'])
        # pred_acc = row['probability'][pred_label]
        if pred_label > 43:
            pred_label = pred_label + 2

        return pred_label,label_map[pred_label]


def show_image_with_prediction(img_path, predicted_label):
    # Load and display the image
    img = plt.imread(img_path)
    plt.imshow(img)
    plt.axis('off')

    # Display the predicted label
    plt.title(f'Predicted Label: {predicted_label}')

    # Show the plot
    plt.show()


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
model.to(device)



if __name__ == "__main__":
    img_path = '/Users/jinling/Downloads/IMG_5336.JPG'
   # / Users / jinling / Downloads / IMG_5336.JPG
    #/ Users / jinling / Desktop / pp1.jpeg
    predicted_label, label_name = predict(img_path, model)
    print(f"图像的标签为: {label_name}")
    show_image_with_prediction(img_path, label_name)
