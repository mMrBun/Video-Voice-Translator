import whisper

model = whisper.load_model("base")
# result = model.transcribe("/data/demo.mp4")
result = model.transcribe("/workspaces/Video-Voice-Translator/DLAI - Learning Platform Beta.mp4")

print(result["text"])
