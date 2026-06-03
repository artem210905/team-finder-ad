import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

AVATAR_SIZE = 200
AVATAR_COLORS = ['#E57373', '#F06292', '#BA68C8', '#9575CD', '#7986CB', '#64B5F6', '#4DD0E1', '#4DB6AC', '#81C784', '#AED581', '#FF8A65']

def generate_avatar(name):
    # Берем первую букву имени или U по умолчанию
    letter = name[0].upper() if name else 'U'
    bg_color = random.choice(AVATAR_COLORS)
    
    img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        # Размер шрифта зависит от размера картинки
        font = ImageFont.truetype("arial.ttf", AVATAR_SIZE // 2)
    except IOError:
        font = ImageFont.load_default()

    # Рисуем по центру, используя константу размера
    left, top, right, bottom = draw.textbbox((0, 0), letter, font=font)
    w, h = right - left, bottom - top
    draw.text(((AVATAR_SIZE-w)/2, (AVATAR_SIZE-h)/2 - 20), letter, fill="white", font=font)
    
    # Сохраняем в буфер
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{letter}.png')
