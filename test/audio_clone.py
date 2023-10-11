from voice_clone import voice_clone_tool

voice_clone_tool.auto_label('output.mp3')
voice_clone_tool.train('output.mp3')
voice_clone_tool.infer('大家好，我是美女！')