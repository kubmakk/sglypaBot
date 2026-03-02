import telebot
import random

# Вставь сюда токен твоего бота от @BotFather
TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

# --- НАШИ ЦЕПИ МАРКОВА ---
# 1. Обычная цепь: как слова идут друг за другом внутри сообщения
chain_internal = {} 

# 2. Мост: ПОСЛЕДНЕЕ слово старого сообщения -> ПЕРВОЕ слово нового сообщения
chain_bridge = {}   

# 3. Память бота: запоминаем последнее написанное слово каждого пользователя
# Формат: {id_пользователя: "последнее_слово"}
user_last_words = {} 

def train_bot(text, user_id):
    """Функция обучения бота на основе входящего сообщения"""
    words = text.lower().split()
    if not words:
        return

    # Шаг 1: Обучаем внутреннюю цепь (связи внутри текста)
    for i in range(len(words) - 1):
        curr_word = words[i]
        next_word = words[i + 1]
        
        if curr_word not in chain_internal:
            chain_internal[curr_word] = []
        chain_internal[curr_word].append(next_word)

    # Шаг 2: Обучаем мост (связь между сообщениями)
    first_word = words[0]
    if user_id in user_last_words:
        # Достаем последнее слово из ПРЕДЫДУЩЕГО сообщения этого юзера
        prev_last_word = user_last_words[user_id] 
        
        if prev_last_word not in chain_bridge:
            chain_bridge[prev_last_word] = []
        chain_bridge[prev_last_word].append(first_word)

    # Запоминаем последнее слово ТЕКУЩЕГО сообщения для следующего раза
    user_last_words[user_id] = words[-1]


def generate_reply(user_id):
    """Генерация ответа, предугадывающая мысль пользователя"""
    # Если мы еще не знаем, что юзер писал последним, сгенерировать ответ сложно
    if user_id not in user_last_words:
        return None
        
    prev_last_word = user_last_words[user_id]
    
    # Пытаемся предсказать ПЕРВОЕ слово по нашему "Мосту"
    if prev_last_word in chain_bridge:
        current_word = random.choice(chain_bridge[prev_last_word])
    else:
        # Если моста нет, берем любое случайное слово из внутренних знаний
        if not chain_internal: return None 
        current_word = random.choice(list(chain_internal.keys()))

    generated_message = [current_word]

    # Строим остальное сообщение по внутренней цепи (максимум 15 слов)
    for _ in range(15):
        if current_word in chain_internal:
            next_word = random.choice(chain_internal[current_word])
            generated_message.append(next_word)
            current_word = next_word
        else:
            break # Если продолжения нет, обрываем фразу

    return " ".join(generated_message)


# --- ОБРАБОТЧИК СООБЩЕНИЙ В TELEGRAM ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    
    # 1. Бот читает сообщение и обучается
    train_bot(text, user_id)
    
    # 2. Бот пытается сгенерировать ответ в стиле пользователя
    # Чтобы бот не спамил на каждое сообщение, сделаем так, 
    # чтобы он отвечал с вероятностью 50% (или если ему написали напрямую)
    if random.choice([True, False]): 
        reply_text = generate_reply(user_id)
        
        if reply_text:
            bot.reply_to(message, reply_text.capitalize())

print("Бот запущен и готов учиться!")
bot.infinity_polling()