import os


def generate_image_from_prompt(prompt):
    # Создаем папку для изображений, если её нет
    os.makedirs('app/static/generated', exist_ok=True)

    # Здесь должна быть ваша логика генерации изображения
    # Временно создаем пустой файл для демонстрации
    filename = f"static/generated/{prompt[:10]}_demo.png"
    with open(filename, 'wb') as f:
        f.write(b'')  # Создаем пустой файл

    return filename