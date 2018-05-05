view a formatted version on
https://github.com/mithom/streamlabs_chatbot_hangman

# streamlabs_chatbot_hangman
if you like the script, you can always support me:
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](paypal.me/ThomasMichiels)

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

## Youtube compatibility mode
in the settings you can enable that !startHangman {number} can also be used in chat instead of in whisper.
In addition you can fill in a word, number (or leave empty) in the settings, press save settings and then press
 'start game' to start a game without the whole chat knowing the word.

### Files to read for showing on stream
They will be kept in sync in real-time
* unsolvedWord.txt
* turns.txt
* solution.txt
* usedLetters.txt
* needs to be shown with browser plugin: overlay/overlay.html

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

### To be expected:
* option for used letters to not count as wrong guesses (no double wrong)
* option to lock out on wrong (word) guess
* option to add timer before which the next guess has to happen / the words need to be found
* add picture of streamer as head of overlay
* option to end game if nobody found something for a while (probably not)
* your feature request here? mail me @ mi_thom@hotmail.com

## see it in action?
streamers that are using this script:
* [DaveBave](https://www.twitch.tv/davebave)
* [-Kel- (mixer)](https://www.mixer.com/-kel-)
* [Billie_bob](https://www.twitch.tv/billie_bob)
* [mrvideofreak](https://www.twitch.tv/mrvideofreak)
* [MathiasAC](https://www.twitch.tv/mathiasamazingchannel)

### changelog:
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
