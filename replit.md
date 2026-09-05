# Auto Rename Bot

## Run

Install dependencies with `pip install -r requirements.txt`, then start the bot with
`python bot.py`. The process also exposes `/` and `/health` on `PORT` (default `5000`)
for Render/Replit health checks.

## Required environment variables

`API_ID`, `API_HASH`, `BOT_TOKEN`, `DB_URL`, `OWNER_ID`, and `LOG_CHANNEL` are required.
`DB_NAME` defaults to `auto_rename`; `PORT` defaults to `5000`.

Never commit Telegram or MongoDB credentials. Configure them as Replit Secrets or Render
environment variables. The support text and health response identify this as the CodeRips
auto-rename bot.