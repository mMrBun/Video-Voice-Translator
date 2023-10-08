import whisper

model = whisper.load_model("base")
result = model.transcribe("/data/demo.mp4")
print(result["text"])
