import os
import time
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


def delete_old_files(folder_path=UPLOAD_FOLDER, days=3):
    """
    删除三天以前的文件
    """
    # 获取当前时间戳
    current_time = time.time()

    # 遍历文件夹内的文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 检查文件是否是普通文件且最后一次修改时间在指定天数之前
        if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > (days * 24 * 3600):
            try:
                # 删除文件
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


# 调用函数删除过期文件

if __name__ == '__main__':
    app.run(debug=True)
    delete_old_files()
