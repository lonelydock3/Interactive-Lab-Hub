#https://elinux.org/rpi_text_to_speech_(speech_synthesis)

#!/bin/bash
say() { local ifs=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=utf-8&client=tw-ob&q=$*&tl=en"; }
#say $*

# Device is sleeping until sensor picks something up
python3 wake_up.py

#When device wakes up
say "Hello, what can I do for you?"

# Record the response
arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav response.wav

# Get response
result=`python3 expected.py response.wav`


# What was it asking?
# date
if [[ "$result" == *"date"* ]]; then
    echo "date gotten"
fi

# time
if [[ "$result" == *"time"* ]]; then
    echo "time gotten"
fi

# agenda
if [[ "$result" == *"agenda"* ]]; then
    echo "todo gotten"
fi

if [[ "$result" == *"to do list"* ]]; then
    echo "todo gotten"
fi

# say " what is your zipcode? "
# 
# arecord -d hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav zipcode_rec.wav

# python3 test_words.py zipcode_rec.wav
