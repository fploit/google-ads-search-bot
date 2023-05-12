# google-ads-search-bot
Find sites that have purchased Google ads for your target keywords  List of sites and control of the bot with Telegram

### Install dependency (ubuntu)
```sh
sudo apt install python3
sudo apt install python3-pip
sudo apt install screen

# install python libraries:

pip3 install pyTelegramBotAPI
pip3 install beautifulsoup4
pip3 install selenium-wire
```

### edit files
1- edit telegram bot token and admin user id in ```config.json```
<br>
2- change ```chromedriver``` to your chrome version.

### run

```sh
cd google-ads-search-bot

screen python3 bot.py
```
