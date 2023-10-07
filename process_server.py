import logging
import os
import sys

from flask import Flask, jsonify
from flask_restful import reqparse
from flask_cors import CORS
from werkzeug.datastructures import FileStorage
from core.process_pipeline import start_process

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)
CORS(app=app)

@app.route("/")
def welcome():
    """welcome"""
    return "hello world"

@app.route("/process", methods=['POST'])
def video_process_pipeline():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('video', type=FileStorage, location='files',
                            help="The video file to be processed.")  # 上传的视频文件
        parser.add_argument('origin_language', required=True, type=str, location='form',
                            help="The original language of the video.")  # 源语言
        parser.add_argument('target_language', required=True, type=str, location='form',
                            help="The target language for translation.")  # 目标语言
        args = parser.parse_args()

        start_process(args)
    except Exception as e:
        logging.info(e)
        return jsonify({
            "error": e
        })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
