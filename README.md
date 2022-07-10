# aiogram-bot-template

This is a template for my telegram bots. Also I provide small bot as example.

## Setup

1. Clone repo and install all dependencies first

   ```bash
   git clone https://github.com/boomb0om/aiogram-bot-template
   cd aiogram-bot-template
   pip install -r requirements.txt
   ```

2. Configure `config.py` file.

3. Now you can run your bot
   Run bot on main instance `python bot.py`
   Run bot on test instance `python bot.py --test`

   Those instances are configured in `config.py` file by placing your api keys in `api_key` and `test_api_key` variables