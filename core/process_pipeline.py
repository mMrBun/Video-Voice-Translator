import os
import tempfile
from flask import jsonify
from service.video_processor import VideoProcessor
from service.text_processor import TextProcessor


def start_process(args):
    """start"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = os.path.join(temp_dir, args.video.filename)
            args.video.save(video_path)
            # extract text use whisper
            video_processor = VideoProcessor(temp_dir=temp_dir, video_path=video_path, file_name=args.video.filename)
            audio_text = video_processor.extract_text()
            # translate origin language to target language
            text_processor = TextProcessor()
            translated_text = text_processor.translate(audio_text)
            # todo tone clone
            # ...
            return jsonify({"output_video_path"})
    except Exception as e:
        print(e)
        return e
