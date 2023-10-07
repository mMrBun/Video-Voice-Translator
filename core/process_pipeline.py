import logging
import os
import tempfile
from flask import jsonify
from service.video_processor import VideoProcessor
from service.audio_processor import AudioProcessor


def start_process(args):
    """start"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = os.path.join(temp_dir, args.video.filename)
            args.video.save(video_path)
            video_processor = VideoProcessor(temp_dir=temp_dir, video_path=video_path, file_name=args.video.filename)
            audio_path = video_processor.extract_audio()
            audio_processor = AudioProcessor(audio_path=audio_path)
            audio_processor.audio_to_text()
            return jsonify({"output_video_path"})
    except Exception as e:
        print(e)
        return e
