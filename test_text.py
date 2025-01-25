# Создание большого текстового файла для тестирования
with open('input.txt', 'w', encoding='utf-8') as file:
    for i in range(1000):  # 1000 строк
        file.write(f"Это строка номер {i}. " * 10 + "\n")