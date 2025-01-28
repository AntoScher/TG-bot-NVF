def split_file(input_file, output_prefix, max_chars=9999):
    # Чтение файла и подсчет общего количества символов
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        total_chars = sum(len(line) for line in lines)  # Общее количество символов

    print(f"Общее количество символов в {input_file}: {total_chars}")

    # Очистка текста: удаление пустых строк, строк с # и лишних пробелов внутри строк
    cleaned_lines = []
    for line in lines:
        stripped_line = line.rstrip()  # Удаляем пробелы справа, сохраняем отступы слева
        if stripped_line and not stripped_line.lstrip().startswith('#'):
            cleaned_lines.append(line)  # Сохраняем исходную строку с отступами

    # Разделение текста на части
    parts = []
    current_part = []
    current_length = 0

    for line in cleaned_lines:
        line_length = len(line)
        if current_length + line_length > max_chars:
            # Если добавление текущей строки превысит max_chars, сохраняем текущую часть
            parts.append(''.join(current_part))
            current_part = []
            current_length = 0
        current_part.append(line)
        current_length += line_length

    # Добавляем последнюю часть, если она не пустая
    if current_part:
        parts.append(''.join(current_part))

    # Сохранение частей в отдельные файлы и подсчет символов в каждой части
    for i, part in enumerate(parts):
        output_file = f"{output_prefix}_part_{i+1}.txt"
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(part)
        part_chars = len(part)
        print(f"Создан файл: {output_file}, количество символов: {part_chars}")

    # Подсчет общего количества символов в выходных файлах
    total_output_chars = sum(len(part) for part in parts)
    print(f"Общее количество символов в выходных файлах: {total_output_chars}")

# Пример использования
input_file = 'input.txt'  # Замените на имя вашего файла
output_prefix = 'output'  # Префикс для выходных файлов
split_file(input_file, output_prefix)