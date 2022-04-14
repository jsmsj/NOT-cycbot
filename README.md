# This is not the source code of the official "cycbot" .
#### Now that being out of the way, you can continute reading this.
---

>Note: In this, "I", "me", "my" refers to me, jsmsj#5252
**whereas**
"you", "yourself" refers to you who is reading this.

> More importantly, "NOT-cycbot", "this bot", "This bot" refers to the mirror of "cycbot" made by me
**whereas**
"Cycbot" or "cycbot" refers to the actual "cycbot" being used in the megadrive server, which is developed and maintained by Cyclism.


------------


> ### The credit for help-text used in this bot including but not limited to :
>- ### emojis,
>- ### images,
>- ### graphics,
>- ### command names,
>### Et cetera goes to Cyclism


------------

## Features of "Cycbot" : 
- Moderation Commands
- Utility
- General Commands
- Logging commands
- Stats commands
- Google Drive Utilities
- Slash Commands
- Request Tracker
- Levelling system
- Starboard system

and much more!!


## Why have i made "NOT-cycbot" ?
This is my take at "cycbot". This is not 100% accurate or the actual source code.
This bot will serve as a place to add commands which i feel should be present in "cycbot".

## Can you host it for yourself ?
Yes you can but make sure if you use the same assets as provided in this repository, then do give the credit to Cyclism as he has made them.

Moreover i have made this bot in a way that you can use specific modules which you need. For example: if you need the starboard system only, then you can configure it accordingly in the .env file.

## Is this accurate ?
**No** it is not at all accurate, because i do not know what some of the commands in "cycbot" do as i do not have access to those commands, but i have tried my best to think of what purpose they would fulfill.

## Progress Checklist for "NOT-cycbot" :
Short term Goals: 
- [x] Moderation Commands
- [x] Utility
- [x] Add database + other stuff
- [x] Google Drive Utilities
- [x] General Commands
- [x] Starboard system

Mid term Goals: 
- [ ] Help for all commands
- [x] Auto starring a message with google drive links
- [ ] Levelling system
- [ ] Logging commands
- [x] Stats commands
- [ ] Request Tracker
- [ ] Error handling


Long term goals
- [ ] Convert all commands to Slash Commands as well.
- [ ] Add Heroku Support + shift to MongoDB !!

## TODO:
- [x] Contributor Stats in `whois` command

## Commands Table:

### Moderation :

"Cycbot" command | Has been implemented in this bot ? 
:---------------- | :--------------------------------:
`purge`           | ✅

### Utility :

"Cycbot" command | Has been implemented in this bot ? 
:---------------- | :--------------------------------:
`avatar`           | ✅
`ping` | ✅
`uptime` | ✅
`whois` | ✅

### Stats :

"Cycbot" command | Has been implemented in this bot ? 
:---------------- | :--------------------------------:
`stats`           | ✅


### Drive Utils :

"Cycbot" command | Has been implemented in this bot ? 
:---------------- | :--------------------------------:
`clone`           | ✅
`get_urls`        | ❌ (Dont know what this does yet)
`md5`             | ❌ (Dont know what this does yet)


### General :

"Cycbot" command | Has been implemented in this bot ? 
:---------------- | :--------------------------------:
`about`           | ✅
`invite`           | ✅
`secret`            | ❌ (Dont know what this does yet)
`secret`             | ❌ (Dont know what this does yet)
`state`             | ✅


### Starboard :

"Cycbot" command | Has been implemented in this bot ? 
:---------------- | :--------------------------------:
`stars`           | ✅
`stars @member`           | ✅



----

## Additional Commands, which are not present in "cycbot"

### Drive Utils :
\>`size` \<drive url\>

---


## How to host ?

### Not recommended right now.

1. Change the values in .env_sample file and rename it to .env
2. In the command prompt do, `pip install -r requirements.txt`
3. Run `main.py` file.
