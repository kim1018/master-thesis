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
from PIL import Image
import shutil
from flask import Flask, request, jsonify, redirect, url_for

app = Flask(__name__)

# 设置随机种子和CUDA
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


# 预测函数
def predict(img_path, model):
    test_files = get_data(img_path)
    test_dataloader = DataLoader(ChaojieDataset(test_files, test=True), batch_size=1, shuffle=False, pin_memory=False)
    best_model = torch.load(
        config.best_models + os.sep + config.model_name + os.sep + str(fold) + os.sep + 'model_best.pth.tar',
        map_location='cpu')
    model.load_state_dict(best_model["state_dict"])
    csv_map = OrderedDict({"filename": [], "probability": []})
    model.to(device)
    model.eval()
    submit_results = []
    for i, (input, filepath) in enumerate(tqdm(test_dataloader)):
        filepath = [os.path.basename(x) for x in filepath]
        with torch.no_grad():
            image_var = Variable(input)
            y_pred = model(image_var)
            smax = nn.Softmax(1)
            smax_out = smax(y_pred)
        csv_map["filename"].extend(filepath)
        for output in smax_out:
            prob = ";".join([str(i) for i in output.data.tolist()])
            csv_map["probability"].append(prob)
    result = pd.DataFrame(csv_map)
    result["probability"] = result["probability"].map(lambda x: [float(i) for i in x.split(";")])
    for index, row in result.iterrows():
        pred_label = np.argmax(row['probability'])
        if pred_label > 43:
            pred_label = pred_label + 2
        return pred_label


def show_image_with_prediction(img_path, predicted_label):
    img = plt.imread(img_path)
    plt.imshow(img)
    plt.axis('off')
    plt.title(f'Predicted Label: {predicted_label}')
    plt.show()


@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Image</title>
    </head>
    <body>
        <h1>Upload Image</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # 确定保存上传文件的文件夹路径
    uploads_dir = os.path.join(os.getcwd(), 'uploads')  # 保存在当前目录下的 "uploads" 文件夹中
    os.makedirs(uploads_dir, exist_ok=True)

    # 保存上传的图片
    saved_img_path = os.path.join(uploads_dir, file.filename)
    file.save(saved_img_path)

    model = get_net()
    model.to(device)

    predicted_label = predict(saved_img_path, model)
    print(f"Predicted Label Index: {predicted_label}")

    return redirect(url_for('show_prediction', img_path=saved_img_path, predicted_label=predicted_label))


@app.route('/show_prediction')
def show_prediction():
    img_path = request.args.get('img_path')
    predicted_label = request.args.get('predicted_label')

    img_tag = f'<img src="{img_path}" width="300">'
    pred_tag = f'<h2>Predicted Label: {predicted_label}</h2>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prediction Result</title>
    </head>
    <body>
        {img_tag}
        {pred_tag}
    </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True)
