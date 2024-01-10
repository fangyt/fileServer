import os
import logging
from flask import Flask, render_template, request, send_from_directory
from logging import handlers

app = Flask(__name__)

# 设置文件上传目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
access_log_file_path = './log/access/'
error_log_file_path = './log/error/'


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


# 路由：首页
@app.route('/')
def index():
    # 获取已上传文件列表
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    try:
        Logger(os.path.join(access_log_file_path, 'index_access.log'), level='debug').logger.info(
            'User accessed the homepage.')
    except Exception as e:
        print(f'Error writing to log file: {e}')
        Logger(os.path.join(error_log_file_path, 'index_error.log'), level='debug').logger.error(f'Error writing to log file: {e}')


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
        Logger(os.path.join(access_log_file_path, 'upload_access.log'), level='debug').logger.info('info')(
            f'File uploaded: {file.filename}')
        return "{'code':'0','msg':'File uploaded successfully'}"
    except Exception as e:
        print(f'Error writing to log file: {e}')
        Logger(os.path.join(error_log_file_path, 'upload_error.log'), level='debug').logger.error(
            f'Error writing to log file: {e}')


# 路由：文件下载
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        Logger(os.path.join(access_log_file_path, 'download_access.log'), level='debug').logger.info(f'User requested to download file: {filename}')

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        Logger(os.path.join(error_log_file_path, 'download_error.log')).logger.error(f'Error writing to log file: {e}')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
