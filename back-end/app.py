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
import ssl
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify
import json
from zhipuai import ZhipuAI

app = Flask(__name__)
# 使用通配符让所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
ssl._create_default_https_context = ssl._create_unverified_context
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


@app.route('/upload', methods=['POST'])
def upload_image():
    label_map = {
        0: "Apple healthy",
        1: "Apple Scab general",
        2: "Apple Scab serious",
        3: "Apple Frogeye Spot",
        4: "Cedar Apple Rust general",
        5: "Cedar Apple Rust serious",
        6: "Cherry healthy",
        7: "Cherry Powdery Mildew general",
        8: "Cherry Powdery Mildew serious",
        9: "Corn healthy",
        10: "Cercospora zeae-maydis general",
        11: "Cercospora zeae-maydis serious",
        12: "Puccinia polysora general",
        13: "Puccinia polysora serious",
        14: "Corn Curvularia leaf spot fungus general",
        15: "Corn Curvularia leaf spot fungus serious",
        16: "Maize dwarf mosaic virus",
        17: "Grape healthy",
        18: "Grape Black Rot Fungus general",
        19: "Grape Black Rot Fungus serious",
        20: "Grape Black Measles Fungus general",
        21: "Grape Black Measles Fungus serious",
        22: "Grape Leaf Blight Fungus general",
        23: "Grape Leaf Blight Fungus serious",
        24: "Citrus healthy",
        25: "Citrus Greening Disease general",
        26: "Citrus Greening Disease serious",
        27: "Peach healthy",
        28: "Peach Bacterial Spot general",
        29: "Peach Bacterial Spot serious",
        30: "Pepper healthy",
        31: "Pepper Scab general",
        32: "Pepper Scab serious",
        33: "Potato healthy",
        34: "Potato Early Blight Fungus general",
        35: "Potato Early Blight Fungus serious",
        36: "Potato Late Blight Fungus general",
        37: "Potato Late Blight Fungus serious",
        38: "Strawberry healthy",
        39: "Strawberry Scorch general",
        40: "Strawberry Scorch serious",
        41: "Tomato healthy",
        42: "Tomato Powdery Mildew general",
        43: "Tomato Powdery Mildew serious",
        44: "Tomato Bacterial Spot general",
        45: "Tomato Bacterial Spot serious",
        46: "Tomato Early Blight Fungus general",
        47: "Tomato Early Blight Fungus serious",
        48: "Tomato Late Blight Water Mold general",
        49: "Tomato Late Blight Water Mold serious",
        50: "Tomato Leaf Mold Fungus general",
        51: "Tomato Leaf Mold Fungus serious",
        52: "Tomato Target Spot Bacteria general",
        53: "Tomato Target Spot Bacteria serious",
        54: "Tomato Septoria Leaf Spot Fungus general",
        55: "Tomato Septoria Leaf Spot Fungus serious",
        56: "Tomato Spider Mite Damage general",
        57: "Tomato Spider Mite Damage serious",
        58: "Tomato Yellow Leaf Curl Virus general",
        59: "Tomato Yellow Leaf Curl Virus serious",
        60: "Tomato Yellow Leaf Curl Virus"
    }
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # 确定保存上传文件的文件夹路径
    uploads_dir = os.path.join(os.getcwd(), 'images')  # 保存在当前目录下的 "uploads" 文件夹中
    # uploads_dir = "/Users/hbin"  # 保存在当前目录下的 "uploads" 文件夹中
    os.makedirs(uploads_dir, exist_ok=True)

    # 保存上传的图片
    saved_img_path = os.path.join(uploads_dir, file.filename)
    file.save(saved_img_path)

    model = get_net()
    model.to(device)

    predicted_label = predict(saved_img_path, model)
    print(f"Predicted Label Index: {predicted_label}")

    # 删除保存的图像
    os.remove(saved_img_path)

    predict_text = label_map.get(predicted_label)

    data = {
        'predicted_label': str(predicted_label),
        'predicted_text': predict_text
    }
    print(data)
    return jsonify(data)  # 将 predicted_label 转换为字符串



@app.route("/", methods=['POST'])
def index():
    data = {'success': True}
    return jsonify(data)
client = ZhipuAI(api_key="bf0fe72a10717d5c8dbd85f83186ee46.wW8zoOvkHyu1DtmS")
@app.route('/gpt-chat', methods=['GET'])
def gpt_chat():
    try:
        data = request.args.get('data')
        messages = [{"role": "user", "content": data}]

        response = client.chat.completions.create(
            model="glm-4",
            messages=messages,
        )
        return jsonify({'message': response.choices[0].message.content})
    except Exception as e:
        # 处理异常，返回错误信息
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, port=5000, host='0.0.0.0')
