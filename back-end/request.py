# request.py
import requests

# 定义上传的图像文件路径
image_path = 'uploads/IMG1.jpeg'

# 定义服务器的 URL
url = 'http://localhost:5000/predict'

# 创建一个包含图像文件的字典
files = {'file': open(image_path, 'rb')}

# 发送 POST 请求
response = requests.post(url, files=files)

# 解析响应
if response.status_code == 200:
    data = response.json()
    predicted_labels = data['predicted_labels']
    print(f'Predicted Labels: {predicted_labels}')
else:
    print('Error:', response.text)
