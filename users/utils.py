import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

def generate_avatar(name):
    # Берем первую букву имени или U по умолчанию
    letter = name[0].upper() if name else 'U'

    colors = ['#E57373', '#F06292', '#BA68C8', '#9575CD', '#7986CB', '#64B5F6', 
              '#4DD0E1', '#4DB6AC', '#81C784', '#AED581', '#FF8A65']
    bg_color = random.choice(colors)
    
    # Создаем изображение 200x200
    img = Image.new('RGB', (200, 200), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Пытаемся загрузить дефолтный шрифт + задаем размер
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()

    # Рисуем букву по центру (приблизительно)
    left, top, right, bottom = draw.textbbox((0, 0), letter, font=font)
    w, h = right - left, bottom - top
    draw.text(((200-w)/2, (200-h)/2 - 20), letter, fill="white", font=font)
    
    # Сохраняем в буфер
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{letter}.png')