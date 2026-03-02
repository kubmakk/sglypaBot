# Telegram Markov Chain Chatbot

## About the Project
This is a self-learning, entertaining Telegram chatbot written in Python. Inspired by popular "shitpost" bots, it uses Markov Chains to analyze chat messages in real-time and generate absurd, funny, and contextually relevant replies based entirely on the users' vocabulary.

The bot starts with zero knowledge and builds its dictionary dynamically as users chat.

## How It Works
The bot's text generation is powered by two interconnected dictionaries:

1. **Internal Chain (`chain_internal`):** Learns the sentence structure by analyzing how words follow each other within a single message.
2. **Bridge Chain (`chain_bridge`):** Builds a logical "bridge" between messages. It links the *last word* of a user's previous message to the *first word* of their new message. This allows the bot to predict conversational flow and continue thoughts.

*Note: By default, the bot responds to messages with a 50% probability to avoid spamming the chat.*

## Prerequisites
- Python 3.x
- `pyTelegramBotAPI` library

## Installation & Setup

1. **Clone or download the repository.**
2. **Install the required library:**
   ```bash
   pip install pyTelegramBotAPI