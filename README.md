view a formatted version on
https://github.com/mithom/streamlabs_chatbot_hangman

# streamlabs_chatbot_hangman
This code is meant for use as script in streamlabs chatbot. The cloud version currently does not support scripts. You do not run this code, but import it into the scripts tab from SL chatbot.

if you like the script, you can always support me:
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](http://paypal.me/ThomasMichiels)

### this scripts adds the hangman minigame.
the available commands are:
* !startHangman {word} (whisper to chatbot)
* !startHangman {number} (whisper to chatbot)
* !startHangman (whisper to chatbot)
* !guess {letter}
* !guess {word} (depending on config)
* !guessWord {word} (other situation)

if you want to be able to use the game with random words, request an api-key at [wordnik](http://developer.wordnik.com/).
Or mail me to get mu api-key after verification of usage.

### Overlay options
They will be kept in sync in real-time
* unsolvedWord.txt
* turns.txt
* solution.txt
* usedLetters.txt
* overlay/overlay.html

the overlay.html needs to be shown as a browser source (local file). For this to work you need to insert api key into
the script by right clicking on it and selecting 'insert API_Key'. Mind! this is not the same api key as the wordnik 
Api Key.

## Youtube compatibility mode
in the settings you can enable that !startHangman {number} can also be used in chat instead of in whisper.
In addition you can fill in a word, number (or leave empty) in the settings, press save settings and then press
 'start game' to start a game without the whole chat knowing the word.

## lots of customisation options
* global & user cooldown
* command names
* custom messages
* min & max word length for random words
* costs & rewards
* max turns & what counts as turn
* combined or separate commands
* do/don't send info to chat that can be shown on stream
* do/don't warn when not enough currency
* autostart new games after previous one ends
* do/don't use multiplier for nb occurrences of letter
* random words retrieved from api or given file
* color of hangman overlay
* how long overlay lingers after finishing game
* option to ignore already used/guessed letters
* shown letters

### requested features (in no particular order):
* remember used words so they don't come again
* option to lock out on wrong (word) guess
* option to add timer before which the next guess has to happen / the words need to be found
* add picture of streamer as head of overlay
* option to end game if nobody found something for a while (probably not)
* your feature request here? mail me @ mi_thom@hotmail.com

## see it in action?
streamers that are using this script:
* [DaveBave](https://www.twitch.tv/davebave)
* [-Kel- ](https://www.twitch.tv/Kelemvore)
* [Billie_bob](https://www.twitch.tv/billie_bob)
* [mrvideofreak](https://www.twitch.tv/mrvideofreak)
* [MathiasAC](https://www.twitch.tv/mathiasamazingchannel)
* [「RizakH」](https://www.twitch.tv/rizakh)
* [WolfSaviour25](https://www.twitch.tv/wolfsaviour25)

### changelog:
v 1.7.6
* fix overlay crash and wrong displaying images
* fix randomness in chatbot
* fix same word in same session again

v 1.7.5
* fix youtube
* allow to mix api & file listed words
* allow whispering answers
* fix ASCII issues

v 1.7.3: 
* do not reset on ascii symbols
* ability to mix file words with api words

v 1.7.2: added shown_letters option

v 1.7.1: added option to ignore already used/guessed letters

v 1.7.0: added customisable messages

v 1.6.0: keep track of used letters

v 1.5.1: make overlay robuster in multiple ways

v 1.5.0: draw hangman as overlay (sliced for too big amount)

v 1.4.2: fix word_guess_counts_as_turn option

v 1.4.1: everything is case insensitive

v 1.4.0: add possibility to read words from file instead of api

v 1.3.0: add multiplier option

v 1.2.1: fix a lot of youtube issues + add option to remove '/me '

v 1.2.0: add 'online only option to aut_start & bugfix when no saved settings'

v 1.1.0: add option to auto start games after delay

v 1.0.3: compatibility mode for youtube

v 1.0.2: support for mixer

v 1.0.1: add max_word_length option

v 1.0.0: made public
