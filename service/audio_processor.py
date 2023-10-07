import openai


class AudioProcessor:
    """audio handle"""
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def audio_to_text(self):
        """audio to text"""
        audio_file = open(self.audio_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript
