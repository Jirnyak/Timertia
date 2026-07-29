<div align="center">

# 🤖 TIMERTIA — Telegram Maid Bot & Game World Engine

[![Language](https://img.shields.io/badge/Python-Telegram%20Bot-blue?style=for-the-badge&logo=python)]()
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue?style=for-the-badge&logo=telegram)]()
[![License](https://img.shields.io/badge/License-Free%20Use-brightgreen?style=for-the-badge)](LICENSE.md)
[![Stars](https://img.shields.io/github/stars/Jirnyak/Timertia?style=for-the-badge&color=gold)]()

> **A Telegram maid bot with world-building capabilities — procedural map generation, market simulation, player management, and game-master tools in a single Python bot.**

[🤖 Bot Demo](#) &nbsp;·&nbsp; [🐛 Issues](../../issues) &nbsp;·&nbsp; [🤝 Contribute](#)

</div>

---

## 📖 About

**TIMERTIA** is a free-to-fork Telegram bot that combines a classic maid-bot assistant with a surprisingly deep game world engine. It generates procedural maps, simulates markets and economies, tracks player stats, and handles a text-based game world — all through Telegram messages.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗺️ **Procedural Map Gen** | `map_gen.py` + `mazegen.py` — generates world maps and maze layouts |
| 💹 **Market Simulation** | `market.txt` + `market_log.txt` — commodity prices, supply/demand, transaction log |
| 👥 **Player Registry** | `players.txt` — tracks registered players, stats, inventory |
| 🏦 **Money System** | `money_buffer.txt` — currency buffer and transaction management |
| 📰 **Rumor Engine** | `mrumors.txt` — rumors propagate through the game world |
| 🎲 **Random Word Gen** | `random_word.txt` — procedural name and word generation |
| 🔤 **Font System** | `Bibold.txt`, `capital.py` — custom text rendering for map display |
| 🎵 **Audio** | `mapple.mp3` — embedded audio asset |

---

## 🔨 Getting Started

```bash
git clone https://github.com/Jirnyak/Timertia.git
cd Timertia

pip install python-telegram-bot

# Configure your bot token in timertia.py
# BOT_TOKEN = "your_token_here"

python timertia.py
```

---

## 🤝 Contributing

Free to use, free to change, free to fork. No strings attached.

---

## 📜 License

Free Use — Jirnyak. Fork it, break it, improve it.

---

<details>
<summary>🇷🇺 Русская Версия</summary>

**TIMERTIA** — Telegram-бот с движком игрового мира. Генерирует процедурные карты, симулирует рынок и экономику, отслеживает игроков, распространяет слухи — всё через Telegram. Свободен для использования и модификации.

</details>
