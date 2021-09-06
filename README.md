## What Is ModMail? 
ModMail is a discord bot which allows users to communicate with higher ups easier and quicker.

The bot is free to use for everyone, just give credits.

## How Does It Work?
When a member messages the bot it will create a channel with the name of their ID. Any messages in that channel will send to the member.

## Features 
* Customizable:
    * Custom Prefix
    * Custom Bot Activity
* Blacklist 
    * Blacklist users from using the bot
    * Unblacklist users
    * Show blacklisted users
For help with these commands type `?help` 

## Installation 
* Discord
  1. First create a bot [Discord Developer](https://discord.com/developers/applications)
  2. Under the bot section enable both intents `SERVER MEMBERS INTENT`, `PRESENCE INTENT`
  3. Copy the token and put it in the config file
* MongoDB
  1. Create a account for mongoDB [MongoDB](https://www.mongodb.com)
  2. Then create a free cluster name it whatever you want
  3. Inside the cluster create a database called main
  4. Under main create 2 collections `servers`,`users`
  5. Go to Database Access create a user with cluster admin
  6. Next go to Network Access click add a ip and press connect from anywhere
  7. Then go back to databases click connect python3 and click that link
  8. Finally go to the config file and put your mongo link in there switch `<password>` for the password you created in step 5
* Config File
  1. Copy the category ID you want the channels to go to put it in the config file
  2. Copy your server ID and put it in the config file
  3. Finally if you want to go ahead and chage the bots acitivity

## Hosting 

* Locally
  1. Open command prompt and navigate to the folder
  2. Once there type `pip install -r requirements.txt`
  3. Double click main.py
  4. Enjoy!

## Credits
This bot was made by Scritpz#0001 free to use by anyone aslong as you give credits
