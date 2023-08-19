import random

# Создаем список слов
words = ["apple", "banana", "cherry", "orange", "grapefruit"]

# Выбираем случайное слово
word = random.choice(words)

# Перемешиваем буквы в слове
shuffled_word = list(word)
random.shuffle(shuffled_word)
shuffled_word = ''.join(shuffled_word)

# Инициализируем переменные для подсчета количества угаданных слов
guessed_words = 0
total_words = 0

# Главный цикл игры
while True:
    # Показываем перепутанное слово пользователю
    print("Перепутанное слово:", shuffled_word)

    # Читаем ответ пользователя
    answer = input("Попробуйте угадать слово: ")

    # Увеличиваем счетчик угаданных слов
    total_words += 1

    # Проверяем, совпадает ли ответ пользователя с исходным словом
    if answer.lower() == word:
        print("Правильно!")
        guessed_words += 1
    else:
        print("Неправильно!")

    # Спрашиваем пользователя, хочет ли он продолжить игру
    play_again = input("Хотите сыграть еще? (да/нет) ")

    # Если пользователь не хочет продолжать игру, завершаем цикл
    if play_again.lower() != 'да':
        break

    # Выбираем новое случайное слово для следующей итерации
    word = random.choice(words)
    shuffled_word = list(word)
    random.shuffle(shuffled_word)
    shuffled_word = ''.join(shuffled_word)

# Выводим статистику игры
print("\nИгра окончена!")
print("Угадано слов:", guessed_words)
print("Всего слов:", total_words)