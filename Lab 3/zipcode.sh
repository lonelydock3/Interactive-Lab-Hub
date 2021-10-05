#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*

say " What is your zipcode? "

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav zipcode_rec.wav

# python3 test_words.py zipcode_rec.wav
