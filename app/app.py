import os
import datetime
import schedule
import time
import logging
import atexit
from flask import Flask, render_template, request, send_from_directory
from logging import handlers
from flask import jsonify

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


def delete_old_files(folder_path=UPLOAD_FOLDER, days_to_keep=2):
    # 获取当前日期
    current_date = datetime.datetime.now()

    # 计算删除的日期阈值
    threshold_date = current_date - datetime.timedelta(days=days_to_keep)

    try:
        # 遍历文件夹内的文件
        for filename in os.listdir(folder_path):

            file_path = os.path.join(folder_path, filename)

            print(os.path.isfile(file_path))
            print(os.path.getmtime(file_path))
            print(threshold_date.timestamp())
            # 检查文件是文件而不是子文件夹，并且最后修改时间早于阈值
            if os.path.isfile(file_path) and os.path.getmtime(file_path) < threshold_date.timestamp():
                # 删除文件
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

    except Exception as e:
        print(f"Error deleting files: {e}")


# 路由：首页
@app.route('/')
def index():
    # 获取已上传文件列表
    mian()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    try:
        Logger(os.path.join(access_log_file_path, 'index_access.log'), level='info').logger.info(
            'User accessed the homepage.')
    except Exception as e:
        print(f'Error writing to log file: {e}')
        Logger(os.path.join(error_log_file_path, 'index_error.log'), level='info').logger.error(
            f'Error writing to log file: {e}')

    return render_template('index.html', files=files)


# 路由：文件上传
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'code': '1', 'msg': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'code': '1', 'msg': 'No selected file'})

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    try:
        Logger(os.path.join(access_log_file_path, 'upload_access.log'), level='info').logger.info(
            f'File uploaded: {file.filename}')
        return jsonify({'code': '0', 'msg': 'File uploaded successfully'})
    except Exception as e:
        print(f'Error writing to log file: {e}')
        Logger(os.path.join(error_log_file_path, 'upload_error.log'), level='info').logger.error(
            f'Error writing to log file: {e}')
        return jsonify({'code': '1', 'msg': f'Error uploading file: {e}'})


# 路由：文件下载
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        Logger(os.path.join(access_log_file_path, 'download_access.log'), level='debug').logger.info(
            f'User requested to download file: {filename}')

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        Logger(os.path.join(error_log_file_path, 'download_error.log')).logger.error(f'Error writing to log file: {e}')


def mian():
    job = schedule.every().day.at("01:00").do(delete_old_files)
    atexit.register(lambda: job.cancel())
    # 无限循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)
    
