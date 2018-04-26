view a formatted version on
https://github.com/mithom/streamlabs_chatbot_easy_counters

# streamlabs_chatbot_easy_counters

### this scripts adds easy managable counters with lots of options.
the available commands are:
* !addcounter !a_new_counter (non-default display text)
* !removeCounter !an_old_counter
* !editCounter !an_existing_counter (non-default message or nothing to get back on default)
* !addCounterPermission !an_existing_counter Permission (extra_info)
* !removeCounterPermission !an_existing_counter
* !counterPermission !an_existing_counter
* !counterPermissions
* !toggleCounterPermissions

By default each command is linked to a global toggle between moderator and a configurable option. Counters can get their own fixed permission by using the !addCounterPermission command. The toggle will not affect the specified counter anymore. To get it back on the global toggle, just remove the permission again using !removePermission. The Global permission can be checked using !counterPermissions.

All config commands are Moderator only without cooldown (this is why you can disable the toggle in settings), All show functions are for everyone with the configured cooldown.

example counter:

    !addCounter !burp
    !addCounter !some_other_counter my count gets displayed in this way: {1}
    !editCounter !burp now burp also gets displayed differently: {1}
    !editCounter !burp                  #this is now back on default message
    !burp 10
    !burp +
    !burp -
    !burp
    !addCounterPermission !burp Min_hours 10

## On top of these commands, it has some configurable settings
* Use Cooldowns?
* Individual/global cooldown
* length of cooldown
* a shorter cooldown to prevent multiple people counting the same event
* global permission in non-moderator toggle stance
* disable the global permission toggle
* custom command names
* custom response messages for all user commands

### parsing of custom messages
`{0}` is always the counter (empty for global)

`{1}` is either the count or the Permission level

`{2}` is the extra info for the permission level

### Files to read for showing on stream
They will be kept in sync in real-time
* Counters.json
* permissions.json
* messages.json

### To be expected:
* other platforms then twitch
* your feature request here? mail me @ mi_thom@hotmail.com

## see it in action?
streamers that are using this script:
* [Billie_bob](http://www.twitch.tv/billie_bob)

### changelog:
v 1.2.0: ability to change message from specific counters

v 1.1.1:
* added custom message for when counter does not exists

* bugfix for problem with 'getUserChangePermissionGlobal' setting

v 1.1.0: added custom messages for commands that users can use

v 1.0.1: added custom command names & file sync

v 1.0.0: made public
