#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "date time to do list agenda")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        # print(rec.Result())
        print("accept")
    else:
        # print(rec.PartialResult())
        print("partial")
print(rec.FinalResult())

# if ("date" in words):
#     print("date")
#     sys.exit(0)
# 
# if ("time" in words):
#     print("time")
#     sys.exit(0)
# 
# if (("to do list" in words) or ("agenda" in words)):
#     print("todo")
#     sys.exit(0)
