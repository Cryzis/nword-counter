# nword counter
a funny discord bot made for a friend that counts the amount of nwords said. This bot has a leaderboard system using MongoDB. When a user types the nword, the bot would respond to that message with one of the custom messages which you can change. This bot also has a total amount of nwords said in that discord (or the same mongodb used). Typing !nwords would bring the menu up. I am planning on adding a AI to the bot so it would detect when the user does typos while saying the nword or replaces certain words to try to bypass it.

## Installation
You need to install [discord.py](https://pypi.org/project/discord.py/) and [pymongo](https://pypi.org/project/pymongo/) package for the bot to work. 
```bash
pip install discord.py
pip install pymongo
```

## Configuration
For the discord bot to work succesfully, you need to fill the data below in the bot.py

```python
bot.run('TOKEN')
mongo_client = pymongo.MongoClient("Your MongoDB")
```

## Credits
[Cryzis](https://cryzis.uk)

You are welcome to use my code, though this is licensed with MIT
