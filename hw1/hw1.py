import random

#Эта функция приветствует игрока и просит выбрать тему,
#а затем считывает нужный список из файла
def choose():
    print('Привет! Выбери категорию, в которую хочешь играть и нажми нужную букву \nD - Динозавры \nE - для Европейские столицы \nM - для Музыкальные инструменты')
    name = input()
    if name == 'E':
        with open('capitals.txt', encoding='utf-8') as f:
            text = f.read()
            words = text.splitlines()
    elif name == 'D':
        with open('dinosaurs.txt', encoding='utf-8') as f:
            text = f.read()
            words = text.splitlines()
    elif name == 'M':
        with open('instruments.txt', encoding='utf-8') as f:
            text = f.read()
            words = text.splitlines()
    else:
        print('Ошибка ввода. Перезапусти программу и попробуй ещё раз')
    return words

#Эта функция выбирает случайное слово из списка
def choose_random(words):
    x = random.randint(0,9)
    print(x)
    word = words[x]
    return(word)

#Эта функция спрашивает букву, проверяет её и определяет, угадано ли слово
def guess(word):
    n = 0
    win = False
    allused = ''
    used = ''
    while (n < 6) and (win == False):
        letter = input('\nВведи букву:')
        if letter not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            print('Это не буква')
        elif letter in allused:
            print('Эту букву ты уже вводил')    
        elif letter in word:
            print('Ты угадал букву')
            win = True
            used = used + letter
            allused = allused + letter
            print(used)
            for i in word:
                if i not in used:
                    win = False
            if win:
                print('Поздравляю. Ты выиграл!')
        else:
            print('Такой буквы в слове нет')
            n = n + 1
            allused = allused + letter
        print('Осталось попыток:',6-n)
        for x in word:
            if x in used:
                print(x, end = ' ')
            else:
                print('_', end = ' ')
          
def main():
    wordlist = choose()
    #print(answer)
    word = choose_random(wordlist)
    print(word)
    print('_ '*len(word))
    guess(word)

main()

