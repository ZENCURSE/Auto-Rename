<div align="center">
  <img src="https://prod.assets.earlygamecdn.com/images/Chisa.jpg?transform=Banner+Webp" alt="Bot Banner" width="1920"/>
  <h1>Auto Rename Bot</h1>
  <p>
    <b>A powerful and dynamic Telegram bot designed to automatically rename large files up to a configurable 4 GiB limit, with a fully interactive, button-based UI that can be configured dynamically by the owner.</b>
  </p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
    <img src="https://img.shields.io/badge/Pyrogram-2.0-orange?style=for-the-badge&logo=telegram" alt="Pyrogram Version">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  </p>
</div>

---

## 🚀 Core Features

-   **✍️ Advanced Auto-Rename:** Automatically rename files based on a custom format, with support for season, episode, quality, and audio extraction.
-   **🖼️ Customization:** Set your own custom thumbnails and captions to give your files a personal touch.
-   **🎞️ Metadata Control:** View and manage metadata for your video files, including title, author, and more.
-   **🗂️ Sequence Mode:** Send multiple files and have them renamed and sent back in a perfect, ordered sequence.
-   **🔐 Force Subscribe:** Ensure users join designated channels before they can use the bot.
-   **⚙️ Dynamic Configuration:** The bot owner can manage all important settings directly from the bot's UI, without needing to restart.
-   **🏆 User Leaderboard:** A built-in leaderboard tracks user activity and showcases the top file renamers.
-   **🔒 Secure:** All sensitive information is loaded from environment variables, not hardcoded.
-   **⚡ Large-file fast path:** Rename-only jobs avoid unnecessary FFmpeg work; the maximum input size defaults to 4 GiB and can be changed with `MAX_FILE_SIZE`.

---

<details>
  <summary><h2>🤖 Bot Commands (Click to Expand)</h2></summary>
  
-   `/start` - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
-   `/autorename` - ᴛᴏ sᴇᴛ ᴀ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ
-   `/showformat` - Tᴏ sᴇᴇ ʏᴏᴜʀ ғᴏʀᴍᴀᴛ
-   `/tutorial` - sᴇᴇ ᴜsᴀɢᴇ ɢᴜɪᴅᴇ
-   `/leaderboard` - Tᴏ ᴠɪᴇᴡ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ
-   `/viewthumb` - ᴠɪᴇᴡ ᴛʜᴜᴍʙɴᴀɪʟ
-   `/delthumb` - ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ
-   `/set_caption` - sᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ᴄᴀᴘᴛɪᴏɴ
-   `/see_caption` - ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ
-   `/del_caption` - ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ
-   `/setmedia` - sᴇᴛ ᴏᴜᴛᴘᴜᴛ ғɪʟᴇ ᴛʏᴘᴇ
-   `/start_sequence` - sᴛᴀʀᴛ ғɪʟᴇ sᴇǫᴜᴇɴᴄɪɴɢ
-   `/end_sequence` - ᴇɴᴅ ғɪʟᴇ sᴇǫᴜᴇɴᴄɪɴɢ
-   `/metadata` - ᴠɪᴇᴡ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ
-   `/verify` - Tᴏ ᴠᴇʀɪғʏ
-   `/add_premium` - Tᴏ ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs (ᴀᴅᴍɪɴ)
-   `/remove_premium` - Tᴏ Rᴇᴍᴏᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs (ᴀᴅᴍɪɴ)
-   `/premium_users` - Tᴏ ᴠɪᴇᴡ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs (ᴀᴅᴍɪɴ)
-   `/premium_info` - Tᴏ ᴠɪᴇᴡ ᴘᴇʀsᴏɴᴀʟʟʏ ᴏɴᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ (ᴀᴅᴍɪɴ)
-   `/verify_settings` - Tᴏ ᴄʜᴀɴɢᴇ ᴠᴇʀɪғʏ sᴇᴛᴛɪɴɢs (ᴀᴅᴍɪɴ)
-   `/fsub_mode` - Tᴏ sᴇᴇ ᴛʜᴇ ғᴏʀᴄᴇ sᴜʙ ᴍᴏᴅᴇ (ᴀᴅᴍɪɴ)
-   `/addchnl` - ᴀᴅᴅ ᴀ ᴄʜᴀɴɴᴇʟ ғᴏʀ ғᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ (ᴀᴅᴍɪɴ)
-   `/delchnl` - ʀᴇᴍᴏᴠᴇ ᴀ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ (ᴀᴅᴍɪɴ)
-   `/listchnl` - ᴠɪᴇᴡ ᴀʟʟ ᴀᴅᴅᴇᴅ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟs (ᴀᴅᴍɪɴ)
-   `/add_admin` - ᴀᴅᴅ ᴀ ɴᴇᴡ ᴀᴅᴍɪɴ (ᴀᴅᴍɪɴ)
-   `/deladmin` - ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ (ᴀᴅᴍɪɴ)
-   `/admins` - ʟɪsᴛ ᴀʟʟ ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴs (ᴀᴅᴍɪɴ)
-   `/restart` - ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ (ᴀᴅᴍɪɴ)
-   `/broadcast` - ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ (ᴀᴅᴍɪɴ)
-   `/status` - Tᴏ ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛᴜs (ᴀᴅᴍɪɴ)
-   `/ban` - ʙᴀɴ ᴀ ᴜsᴇʀ (ᴀᴅᴍɪɴ)
-   `/unban` - ᴜɴʙᴀɴ ᴀ ᴜsᴇʀ (ᴀᴅᴍɪɴ)
-   `/banned` - sʜᴏᴡ ʙᴀɴɴᴇᴅ ᴜsᴇʀs (ᴀᴅᴍɪɴ)

</details>

---

## 🛠️ How to Deploy

You can easily deploy this bot yourself by following the steps below.

### **1. Prerequisites**

-   **Telegram Bot Token:** Get one from [@BotFather](https://t.me/BotFather).
-   **Telegram API ID & Hash:** Get them from [my.telegram.org](https://my.telegram.org).
-   **MongoDB Database URL:** Get a free one from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### **2. Deployment Steps**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ZENCURSE/Auto-Rename.git
    cd Auto-Rename
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables:**
    Create a `.env` file or set the following environment variables in your deployment environment:

| Variable      | Description                                | Required |
|---------------|--------------------------------------------|----------|
| `API_ID`      | Your Telegram App ID.                      | **Yes**  |
| `API_HASH`    | Your Telegram App Hash.                    | **Yes**  |
| `BOT_TOKEN`   | Your Telegram bot token from @BotFather.   | **Yes**  |
| `DB_URL`      | Your MongoDB connection URL.               | **Yes**  |
| `OWNER_ID`    | Your numerical Telegram User ID.           | **Yes**  |
| `LOG_CHANNEL` | The ID of the channel for bot logs.        | **Yes**  |
| `MAX_FILE_SIZE` | Maximum input size in bytes; defaults to 4 GiB. | No |
| `RENAME_CONCURRENCY` | Concurrent rename jobs; defaults to 2 for smooth large-file processing. | No |


4.  **Run the Bot:**
    ```bash
    python3 bot.py
    ```

---

## 🙏 Credits & Acknowledgements

This project was made possible by the inspiration and foundational work of others in the community.

-   **Base Repository:** A special thanks to **[Jishu Developer](https://github.com/JishuDeveloper)** for their original work.
-   **Inspiration & Support:** **[CantarellaBots](https://t.me/cantarellabots)**

### **Contributors**
-   **[ABHINAI](https://t.me/about_zani)**
-   **[ABHINAV](https://t.me/adityaabhinav)**
-   **[MASTER](https://t.me/V_Sbotmaker)**
