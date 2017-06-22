# levelsBot 1.3

A Discord bot written in Python 3.5.2, that allows you to give users stars (or levels). The bot requires discord.py module to run.

Features in Early Testing (working features, but still in development):

- Command to list all stars (works, but needs testing on a large server to verify that it works with a large amount of users)
- Changing peoples nicknames with their star count in brackets (currently only works with default usernames not nicknames. Has to be triggered by a command, however this will be automatic in the future, with a option to toggle off the star count nicknames. Also, this command cannot change users' nicknames with Administrator on their role who are above the bot's role in the role hierachy.)

Features Coming Soon (features closer to the top will be worked on first):

- Live updating to .txt files (no more using ?backup or ?shutdown to save stars. This saves alot of hassle in the future)
- Add web-based star lists through Flask or Django
- Add support for multiple servers (multiple txt files and python files)
