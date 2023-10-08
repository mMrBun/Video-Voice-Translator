from gtts import gTTS  
import os  
  
text = "你好时间"  # 要转换为语音的文本  
output = gTTS(text=text, lang='zh-cn')  # 将文本转换为语音
  
output.save("output.mp3")  # 保存语音到文件