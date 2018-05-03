# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import json
import codecs
import re
import os
import clr
clr.AddReference("IronPython.Modules.dll")
import urllib
import time
import random


# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Hangman"
Website = "https://www.twitch.tv/mi_thom"
Description = "play the hangman game in chat"
Creator = "mi_thom"
Version = "1.5.0"

# ---------------------------------------
#   Set Global Variables
# ---------------------------------------
ScriptSettings = None
m_SettingsFile = os.path.join(os.path.dirname(__file__), "hangmanSettings.json")
m_ModeratorPermission = "Moderator"
m_allowed_permissions = ["Everyone", "Regular", "Subscriber", "GameWisp_Subscriber", "User_Specific", "Min_Rank",
                         "Min_Points", "Min_Hours", "Moderator", "Editor", "Caster"]
m_vowels = ["a", "e", "i", "o", "u"]
m_CurrentWord = None
m_CurrentSolution = None
m_GameRunning = False
m_WordFile = os.path.join(os.path.dirname(__file__), "unsolvedWord.txt")
m_SolutionFile = os.path.join(os.path.dirname(__file__), "solution.txt")
m_TurnsFile = os.path.join(os.path.dirname(__file__), "turns.txt")
m_Client = None
m_turns = 0
m_LastGame = 0
m_random_words_from_file = []


# ---------------------------------------
# Classes
# ---------------------------------------
class Settings(object):
    """ Load in saved settings file if available else set default values. """

    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            # random_words
            self.api_key = "Your key here"
            self.use_file = False
            self.file_name = "words.txt"

            # Config
            self.use_different_guess_command = False
            self.start_game_permission = m_ModeratorPermission
            self.start_game_info = ""
            self.min_word_length = 4
            self.max_word_length = 8
            self.send_message_if_not_enough_points = True
            self.send_progress_after_guess = True
            self.auto_start_game = False
            self.auto_delay = 60
            self.only_online = True

            # Game play
            self.global_cd = 5
            self.user_cd = 15
            self.end_after_x_turns = False
            self.nb_turns = 7
            self.word_guess_counts_as_turn = True
            self.use_multiplier = False

            # Command costs & rewards
            self.guess_cost = 0
            self.guess_word_cost = 0
            self.guess_vowel_cost = 0
            self.find_letter_reward = 0
            self.finish_word_reward = 0

            # Command names
            self.start_game_command = "!startHangman"
            self.guess_command = "!guess"
            self.guess_word_command = "!guessWord"
            self.currency_name = "points"

            # Overlay
            self.vanish_delay = 10
            self.hangman_color = "rgba(0,0,0,255)"

            # Youtube compatibility
            self.not_show_me = False
            self.allow_chat_message = False
            self.next_word = ""
        self.save(settingsfile)

    def reload(self, jsondata):
        """ Reload settings from Chatbot user interface by given json data. """
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        self.save(m_SettingsFile)
        return

    def save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return


class WordsApi(object):

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def getRandomWord(self, **kwargs):
        """Returns a single random WordObject

        Args:
            includePartOfSpeech, str: CSV part-of-speech values to include (optional)
            excludePartOfSpeech, str: CSV part-of-speech values to exclude (optional)
            hasDictionaryDef, str: Only return words with dictionary definitions (optional)
            minCorpusCount, int: Minimum corpus frequency for terms (optional)
            maxCorpusCount, int: Maximum corpus frequency for terms (optional)
            minDictionaryCount, int: Minimum dictionary count (optional)
            maxDictionaryCount, int: Maximum dictionary count (optional)
            minLength, int: Minimum word length (optional)
            maxLength, int: Maximum word length (optional)

        Returns: WordObject
        """

        allParams = ['includePartOfSpeech', 'excludePartOfSpeech', 'hasDictionaryDef', 'minCorpusCount',
                     'maxCorpusCount', 'minDictionaryCount', 'maxDictionaryCount', 'minLength', 'maxLength']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method getRandomWord" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/words.{format}/randomWord'
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if 'hasDictionaryDef' in params:
            queryParams['hasDictionaryDef'] = self.apiClient.toPathValue(params['hasDictionaryDef'])
        if 'includePartOfSpeech' in params:
            queryParams['includePartOfSpeech'] = self.apiClient.toPathValue(params['includePartOfSpeech'])
        if 'excludePartOfSpeech' in params:
            queryParams['excludePartOfSpeech'] = self.apiClient.toPathValue(params['excludePartOfSpeech'])
        if 'minCorpusCount' in params:
            queryParams['minCorpusCount'] = self.apiClient.toPathValue(params['minCorpusCount'])
        if 'maxCorpusCount' in params:
            queryParams['maxCorpusCount'] = self.apiClient.toPathValue(params['maxCorpusCount'])
        if 'minDictionaryCount' in params:
            queryParams['minDictionaryCount'] = self.apiClient.toPathValue(params['minDictionaryCount'])
        if 'maxDictionaryCount' in params:
            queryParams['maxDictionaryCount'] = self.apiClient.toPathValue(params['maxDictionaryCount'])
        if 'minLength' in params:
            queryParams['minLength'] = self.apiClient.toPathValue(params['minLength'])
        if 'maxLength' in params:
            queryParams['maxLength'] = self.apiClient.toPathValue(params['maxLength'])
        postData = (params['body'] if 'body' in params else None)

        response = self.apiClient.callAPI(resourcePath, method, queryParams,
                                          postData, headerParams)
        response = json.loads(response)
        Parent.Log(ScriptName, str(queryParams))
        if response['status'] == 200:
            return json.loads(response['response'])['word']
        else:
            Parent.Log(ScriptName, str(response))
        return None


class ApiClient:
    """Generic API client for Swagger client library builds"""

    def __init__(self, apiKey=None, apiServer=None):
        if apiKey == None:
            raise Exception('You must pass an apiKey when instantiating the '
                            'APIClient')
        self.apiKey = apiKey
        self.apiServer = apiServer
        self.cookie = None

    def callAPI(self, resourcePath, method, queryParams, postData,
                headerParams=None):

        url = self.apiServer + resourcePath
        headers = {}
        if headerParams:
            for param, value in headerParams.iteritems():
                headers[param] = value

        headers['Content-type'] = 'application/json'
        headers['api_key'] = self.apiKey

        if self.cookie:
            headers['Cookie'] = self.cookie

        data = None

        if method == 'GET':

            if queryParams:
                # Need to remove None values, these should not be sent
                sentQueryParams = {}
                for param, value in queryParams.items():
                    if value != None:
                        sentQueryParams[param] = value
                url = url + '?' + urllib.urlencode(sentQueryParams)
        return Parent.GetRequest(url, headers)

    def toPathValue(self, obj):
        """Convert a string or object to a path-friendly value
        Args:
            obj -- object or string value
        Returns:
            string -- quoted value
        """
        if type(obj) == list:
            return urllib.quote(','.join(obj))
        elif type(obj) == unicode:
            return urllib.quote(obj.encode('utf8'))
        else:
            return urllib.quote(str(obj))


# ---------------------------------------
#   Init & Cleanup functions
# ---------------------------------------
def save_game():
    try:
        with open(m_WordFile, "w") as f:
            f.write(m_CurrentWord or "")
        with open(m_SolutionFile, "w") as f:
            f.write(m_CurrentSolution or "")
        with open(m_TurnsFile, "w") as f:
            if m_GameRunning:
                if ScriptSettings.end_after_x_turns:
                    f.write(str(m_turns) + "/" + str(int(ScriptSettings.nb_turns)))
                else:
                    f.write(str(m_turns))
            else:
                f.write("")
    except:
        Parent.Log(ScriptName, "Failed to save the current game")
    return


def load_game():
    global m_GameRunning, m_CurrentWord, m_CurrentSolution, m_turns
    try:
        with open(m_SolutionFile, "r") as f:
            m_CurrentSolution = f.read()
        with open(m_WordFile, "r") as f:
            m_CurrentWord = f.read()
        with open(m_TurnsFile, 'r') as f:
            var = f.read()
            if len(var) > 0:
                m_turns = int(var.split("/")[0])
            else:
                m_turns = 0
        if len(m_CurrentSolution) == 0:
            m_CurrentWord = None
            m_CurrentSolution = None
            m_GameRunning = False
        else:
            m_GameRunning = True
            to_send = 'current game is still in progress'
            Parent.SendStreamMessage(format_message(to_send))
            send_progress()
    except:
        Parent.Log(ScriptName, "failed to load current game, game has been reset")


def load_random_words():
    global m_random_words_from_file
    if ScriptSettings.use_file:
        with open(os.path.join(os.path.dirname(__file__), ScriptSettings.file_name), "r") as f:
            m_random_words_from_file = f.readlines()
        for i in xrange(len(m_random_words_from_file)):
            m_random_words_from_file[i] = m_random_words_from_file[i].strip()


# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global ScriptSettings, m_Client, m_LastGame
    m_LastGame = time.clock()
    api_url = 'http://api.wordnik.com/v4'
    ScriptSettings = Settings(m_SettingsFile)
    m_Client = ApiClient(ScriptSettings.api_key, api_url)
    load_game()
    load_random_words()
    return


# ---------------------------------------
#   [Optional] Reload settings (Only called on save button press)
# ---------------------------------------
def ReloadSettings(jsondata):
    # load in json after pressing save settings button
    global ScriptSettings, m_Client
    ScriptSettings.reload(jsondata)
    Parent.BroadcastWsEvent("EVENT_RELOAD_SETTINGS_HANGMAN", jsondata)
    api_url = 'http://api.wordnik.com/v4'
    m_Client = ApiClient(ScriptSettings.api_key, api_url)
    Parent.Log(ScriptName, "saving settings successful")
    load_game()
    load_random_words()
    return


# ---------------------------------------
#   [Optional] Save data (Only called on exit chatbot)
# ---------------------------------------
def Unload():
    # Triggers when the bot closes / script is reloaded
    save_game()
    return


def ScriptToggle(state):
    # Tells you if the script is enabled or not, state is a boolean
    return


# ---------------------------------------
#   Processing functions
# ---------------------------------------
def has_command_format(first_word):
    return first_word[0] == "!"


def start_game():
    global m_GameRunning
    global m_turns
    if m_GameRunning:
        return False
    else:
        m_GameRunning = True
        m_turns = 0
        Parent.BroadcastWsEvent("EVENT_START_HANGMAN", "")
        return True


def end_game():
    global m_GameRunning, m_CurrentWord, m_CurrentSolution, m_LastGame
    m_GameRunning = False
    m_CurrentWord = ""
    m_CurrentSolution = ""
    m_LastGame = time.clock()
    save_game()
    Parent.BroadcastWsEvent("EVENT_END_HANGMAN", "")


def start_game_command(user, **kwargs):
    global m_CurrentWord, m_CurrentSolution
    if kwargs.get('is_bot', False):
        user = 'auto_start'
    if Parent.HasPermission(user, ScriptSettings.start_game_permission, ScriptSettings.start_game_info) or \
            kwargs.get('is_bot', False):
        if start_game():
            if "length" in kwargs:
                word = get_random_word_with_length(kwargs["length"])
            elif "word" in kwargs:
                word = kwargs["word"]
            else:
                word = get_random_word()
            if word is None:
                end_game()
                Parent.SendStreamWhisper(user, "failed to retrieve a random word, check your connection & api-key")
                return
            m_CurrentSolution = word.lower().replace(" ", "-").replace("_", "-")
            m_CurrentWord = "_ " * len(word)
            save_game()
            to_send = "a game of hangman has been started, start guessing now using %s {letter}" % \
                      ScriptSettings.guess_command
            if ScriptSettings.use_different_guess_command:
                to_send += " and %s" % ScriptSettings.guess_word_command
            Parent.SendStreamMessage(format_message(to_send))
            send_progress()
        else:
            Parent.SendStreamWhisper(user, "current game still in progress")


def get_random_word():
    if ScriptSettings.use_file:
        return get_random_word_from_file(ScriptSettings.min_word_length, ScriptSettings.max_word_length)
    else:
        words_api = WordsApi(m_Client)
        return words_api.getRandomWord(hasDictionaryDef=True, minLength=int(ScriptSettings.min_word_length),
                                       maxLength=int(ScriptSettings.max_word_length), minCorpusCount=200)


def get_random_word_with_length(length):
    if ScriptSettings.use_file:
        return get_random_word_from_file(length, length)
    else:
        words_api = WordsApi(m_Client)
        return words_api.getRandomWord(hasDictionaryDef=True, minLength=int(length), maxLength=int(length),
                                       minCorpusCount=200)


def get_random_word_from_file(min_length, max_length):
    possibilities = m_random_words_from_file
    while len(possibilities) > 0:
        word = random.choice(possibilities)
        if max_length >= len(word) >= min_length:
            return word
        else:
            possibilities.remove(word)


def guess_word_or_letter(user, word):
    if len(word) == 1:
        guess_letter(user, word)
    else:
        guess_word(user, word)


def add_turn():
    global m_turns
    m_turns += 1
    if ScriptSettings.end_after_x_turns and m_turns >= ScriptSettings.nb_turns:
        if not is_finished():
            to_send = 'the word has not been found within the turn limit, the solution was %s' % m_CurrentSolution
            Parent.SendStreamMessage(format_message(to_send))
        end_game()
    save_game()


def is_on_cooldown(user):
    return Parent.IsOnCooldown(ScriptName, "guess") or Parent.IsOnUserCooldown(ScriptName, "guess", user)


def add_cooldown(user):
    Parent.AddCooldown(ScriptName, "guess", ScriptSettings.global_cd)
    Parent.AddUserCooldown(ScriptName, "guess", user, ScriptSettings.user_cd)


def guess_word(user, word):
    global m_CurrentWord
    if m_GameRunning:
        if not is_on_cooldown(user):
            add_cooldown(user)
            username = Parent.GetDisplayName(user)
            if Parent.RemovePoints(user, username, ScriptSettings.guess_word_cost):
                word = word.lower()
                if word == m_CurrentSolution:
                    m_CurrentWord = ' '.join(m_CurrentSolution)
                    reward(user, word)
                    send_progress()
                    end_game()
                else:
                    to_send = '%s, the word %s is incorrect, better luck next time' % (username, word)
                    Parent.SendStreamMessage(format_message(to_send))
                    if ScriptSettings.word_guess_counts_as_turn:
                        Parent.BroadcastWsEvent("EVENT_GUESSED_WORD_WRONG_HANGMAN", json.dumps({"word": word}))
                        add_turn()
            elif ScriptSettings.send_message_if_not_enough_points:
                current_user_points = Parent.GetPoints(user)
                to_send = "%s, you don't have enough %s, you need %i and only have %i" % (
                    username, ScriptSettings.currency_name, ScriptSettings.guess_word_cost, current_user_points)
                Parent.SendStreamMessage(format_message(to_send))
    else:
        to_send = 'there is currently no hangman game running, pls start one using %s' % \
                  ScriptSettings.start_game_command
        Parent.SendStreamMessage(format_message(to_send))


def guess_letter(user, letter):
    if len(letter) == 1:
        if m_GameRunning:
            if not is_on_cooldown(user):
                add_cooldown(user)
                letter = letter.lower()
                if letter in m_vowels:
                    cost = ScriptSettings.guess_vowel_cost
                else:
                    cost = ScriptSettings.guess_cost
                username = Parent.GetDisplayName(user)
                if Parent.RemovePoints(user, username, cost):
                    if letter in m_CurrentSolution and letter not in m_CurrentWord:
                        fill_in_letter(letter)
                        reward(user, letter)
                    else:
                        to_send = "%s, %s is not in the word" % (username, letter)
                        Parent.SendStreamMessage(format_message(to_send))
                        Parent.BroadcastWsEvent("EVENT_GUESSED_LETTER_WRONG_HANGMAN", json.dumps({"letter":letter}))
                        add_turn()
                    if is_finished():
                        end_game()
                    else:
                        send_progress()
                elif ScriptSettings.send_message_if_not_enough_points:
                    current_user_points = Parent.GetPoints(user)
                    to_send = "%s, you don't have enough %s, you need %i and only have %i" % (
                        username, ScriptSettings.currency_name, ScriptSettings.guess_cost, current_user_points)
                    Parent.SendStreamMessage(format_message(to_send))
        else:
            to_send = 'no hangman game running (%s)' % ScriptSettings.start_game_command
            Parent.SendStreamMessage(format_message(to_send))


def fill_in_letter(letter):
    global m_CurrentWord
    for m in re.finditer(letter, m_CurrentSolution):
        m_CurrentWord = m_CurrentWord[:m.start() * 2] + letter + m_CurrentWord[m.start() * 2 + 1:]
    save_game()


def is_finished():
    return "_" not in m_CurrentWord


def reward(user, letter_or_word):
    username = Parent.GetDisplayName(user)
    if len(letter_or_word) == 1:
        if is_finished():
            Parent.AddPoints(user, username, ScriptSettings.finish_word_reward)
            Parent.SendStreamMessage(
                format_message("%s found the last letter (%s) and has been rewarded %s %s for finishing the word." % (
                    username, letter_or_word, ScriptSettings.finish_word_reward, ScriptSettings.currency_name)))
        else:
            points = ScriptSettings.find_letter_reward
            if ScriptSettings.use_multiplier:
                points *= m_CurrentSolution.count(letter_or_word)
            Parent.AddPoints(user, username, points)
            Parent.SendStreamMessage(format_message("%s found %s, reward: %s %s." % (
                username, letter_or_word, points, ScriptSettings.currency_name)))
    else:
        Parent.AddPoints(user, username, ScriptSettings.finish_word_reward)
        Parent.SendStreamMessage(format_message("%s has found the correct word and has been rewarded %s %s." % (
            username, ScriptSettings.finish_word_reward, ScriptSettings.currency_name)))


def format_message(to_send):
    if not ScriptSettings.not_show_me:
        to_send = '/me ' + to_send
    return to_send


def send_progress():
    if ScriptSettings.send_progress_after_guess:
        to_send = m_CurrentWord
        if ScriptSettings.end_after_x_turns:
            to_send = "turn %i / %i : " % (m_turns, ScriptSettings.nb_turns) + to_send
        Parent.SendStreamMessage(format_message(to_send))


def process_command(data):
    param1 = data.GetParam(0)
    p_count = data.GetParamCount()
    if data.IsWhisper():
        if param1 == ScriptSettings.start_game_command:
            if p_count == 1:
                start_game_command(data.User)
            elif p_count == 2:
                param2 = data.GetParam(1)
                if param2.isdigit():
                    start_game_command(data.User, length=int(param2))
                else:
                    start_game_command(data.User, word=param2)
    elif data.IsChatMessage():
        if ScriptSettings.allow_chat_message:
            if param1 == ScriptSettings.start_game_command:
                if p_count == 1:
                    start_game_command(data.User)
                elif p_count == 2:
                    param2 = data.GetParam(1)
                    if param2.isdigit():
                        start_game_command(data.User, length=int(param2))
        if p_count == 2:
            param2 = data.GetParam(1)
            if ScriptSettings.use_different_guess_command:
                if param1 == ScriptSettings.guess_command:
                    guess_letter(data.User, param2)
                elif param1 == ScriptSettings.guess_word_command:
                    guess_word(data.User, param2)
            else:
                if param1 == ScriptSettings.guess_command:
                    guess_word_or_letter(data.User, param2)


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    if not data.IsFromDiscord():
        param1 = data.GetParam(0)
        if (data.IsChatMessage() or data.IsWhisper()) and has_command_format(param1):
            process_command(data)
    return


# ---------------------------------------
#   [button] Called when pressing the start game button
# ---------------------------------------
def StartHangmanButton():
    next_word = ScriptSettings.next_word
    user = Parent.GetChannelName()
    if len(next_word) == 0:
        start_game_command(user)
    elif next_word.isdigit():
        start_game_command(user, length=int(next_word))
    else:
        start_game_command(user, word=next_word)


# ---------------------------------------
#   [Required] Tick Function
# ---------------------------------------
def Tick():
    global m_LastGame
    if (not ScriptSettings.only_online) or Parent.IsLive():
        if (not m_GameRunning) and ScriptSettings.auto_start_game:
            if (time.clock() - m_LastGame) > ScriptSettings.auto_delay:
                m_LastGame = time.clock()
                start_game_command(None, is_bot=True)


# ---------------------------------------
#   Button function
# ---------------------------------------
def GetWordnikApiKey():
    os.system("start \"\" http://developer.wordnik.com")


def OpenScriptFolder():
    os.startfile(os.path.dirname(__file__))
