view a formatted version on
https://github.com/mithom/streamlabs_chatbot_hangman

# streamlabs_chatbot_hangman

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

## lots of customisation options
* global & user cooldown
* command names
* min & max word length for random words
* costs & rewards
* max turns & what counts as turn
* combined or separate commands
* do/don't send info to chat that can be shown on stream
* do/don't warn when not enough currency

### To be expected:
* custom messages
* your feature request here? mail me @ mi_thom@hotmail.com

## see it in action?
streamers that are using this script:
* [DaveBave](https://www.twitch.tv/davebave)
* [Billie_bob](http://www.twitch.tv/billie_bob)

### changelog:
v 1.0.3: compatibility mode for youtube

v 1.0.2: support for mixer

v 1.0.1: add max_word_length option

v 1.0.0: made public
