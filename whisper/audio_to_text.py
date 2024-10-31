import whisper

model = whisper.load_model("base")
result = model.transcribe(r"C:\Clutchgod\Beta_Male\Saved_Audio\audio.wav")
print(result["text"])