import os
import whisper
from moviepy.audio.io.AudioFileClip import AudioFileClip


class VideoProcessor:
    def __init__(self, temp_dir, video_path, file_name):
        self.temp_dir = temp_dir
        self.video_path = video_path
        self.file_name = file_name

    def extract_audio(self) -> str:
        output_audio_path = os.path.join(self.temp_dir, f'{self.file_name.split(".")[0]}.wav')
        my_audio_clip = AudioFileClip(self.video_path)
        my_audio_clip.write_audiofile(output_audio_path)
        if os.path.exists(output_audio_path):
            return output_audio_path
        else:
            return ''

    def extract_text(self, model_type="base", resource_language="en") -> str:
        model = whisper.load_model(model_type)
        result = model.transcribe(self.video_path, language=resource_language)
        return result['text']
