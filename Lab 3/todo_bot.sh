#https://elinux.org/rpi_text_to_speech_(speech_synthesis)

#!/bin/bash
say() { local ifs=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=utf-8&client=tw-ob&q=$*&tl=en"; }
#say $*

while [ 1 ] 
do
    
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
        dt=`python3 get_info.py "date"`
        say $dt
    fi
    
    # time
    if [[ "$result" == *"time"* ]]; then
        echo "time gotten"
        tt=`python3 get_info.py "time"`
        say $tt
    fi
    
    # agenda
    if [[ "$result" == *"agenda"* ]] || [[ "$result" == *"to do list"* ]]; then
        echo "todo gotten"
        echo $result
        if [[ "$result" == *"what"* ]]; then
            echo "playback"
            say "Here is what is on your to do list"
            aplay todo_list.wav
        fi
        if [[ "$result" == *"read"* ]]; then
            echo "playback"
            say "Here is what is on your to do list"
            aplay todo_list.wav
        fi
    
        if [[ "$result" == *"add"* ]]; then
            echo "adding"
            say "Please record your to do list"
            arecord -D hw:2,0 -f cd -c1 -r 48000 -d 10 -t wav todo_list.wav
        fi
    fi

done

