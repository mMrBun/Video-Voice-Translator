class VideoTranslateParam:
    """video translate param"""
    def __init__(self,video_path,source_language,target_language) -> None:
        self.video_path=video_path
        self.source_language=source_language
        self.target_language=target_language