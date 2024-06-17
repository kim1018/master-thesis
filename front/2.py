from flask import Flask, request, jsonify
import json
from zhipuai import ZhipuAI

app = Flask(__name__)

# 初始化客户端
client = ZhipuAI(api_key="bf0fe72a10717d5c8dbd85f83186ee46.wW8zoOvkHyu1DtmS")

@app.route('/gpt-chat', methods=['GET'])
def gpt_chat():
    try:
        # 从查询参数中获取数据
        data = request.args.get('data')

        # 创建消息
        messages = [{"role": "user", "content": data}]

        # 调用ZhipuAI的API
        response = client.chat.completions.create(
            model="glm-4",
            messages=messages,
        )

        # 尝试将message转换为JSON兼容的字符串
       
        return jsonify({'message': response.choices[0].message.content})
    except Exception as e:
        # 处理异常，返回错误信息
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
