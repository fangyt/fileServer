import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# 设置文件上传目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 配置日志记录
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# 上传日志处理器
upload_log_handler = RotatingFileHandler('upload.log', maxBytes=1024 * 1024, backupCount=5)
upload_log_handler.setFormatter(log_formatter)
upload_log_handler.setLevel(logging.INFO)

# 下载日志处理器
download_log_handler = RotatingFileHandler('download.log', maxBytes=1024 * 1024, backupCount=5)
download_log_handler.setFormatter(log_formatter)
download_log_handler.setLevel(logging.INFO)

# 将处理器添加到 app.logger
app.logger.addHandler(upload_log_handler)
app.logger.addHandler(download_log_handler)

# 路由：首页
@app.route('/')
def index():
    # 获取已上传文件列表
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    try:
        app.logger.info('User accessed the homepage.')
    except Exception as e:
        print(f'Error writing to log file: {e}')

    return render_template('index.html', files=files)

# 路由：文件上传
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    try:
        app.logger.info(f'File uploaded: {file.filename}')
    except Exception as e:
        print(f'Error writing to log file: {e}')
    return "{'code':'0','msg':'File uploaded successfully'}"

# 路由：文件下载
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        app.logger.info(f'User requested to download file: {filename}')
    except Exception as e:
        print(f'Error writing to log file: {e}')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
