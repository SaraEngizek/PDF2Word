#!/usr/bin/env python3
"""
PDF2Word için modern uygulama ikonu oluştur
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_pdf2word_icon(size=1024):
    """Modern PDF2Word ikonu oluştur - PDF'ten Word'e dönüşüm konsepti"""

    # Yeni görüntü oluştur (RGBA)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Boyut oranları
    margin = size * 0.08
    corner_radius = size * 0.15

    # Ana renkler
    primary_color = (37, 99, 235)  # Canlı mavi
    secondary_color = (59, 130, 246)  # Açık mavi

    # Yuvarlak köşeli kare çiz
    def rounded_rectangle(draw, coords, radius, fill):
        x1, y1, x2, y2 = coords
        draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)
        draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)
        draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)
        draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)

    # Ana arka plan
    rounded_rectangle(draw,
                     [margin, margin, size - margin, size - margin],
                     corner_radius, primary_color)

    # İç gradient efekti
    inner_margin = margin + size * 0.025
    rounded_rectangle(draw,
                     [inner_margin, inner_margin,
                      size - inner_margin, size - inner_margin],
                     corner_radius * 0.9, secondary_color)

    # Sol taraf - PDF belgesi
    pdf_left = size * 0.14
    pdf_top = size * 0.20
    pdf_width = size * 0.30
    pdf_height = size * 0.48

    # PDF gölge
    draw.rectangle([pdf_left + 4, pdf_top + 4,
                   pdf_left + pdf_width + 4, pdf_top + pdf_height + 4],
                  fill=(20, 60, 180, 80))

    # PDF kağıt
    draw.rectangle([pdf_left, pdf_top, pdf_left + pdf_width, pdf_top + pdf_height],
                  fill=(255, 248, 248))

    # PDF üst kırmızı bant
    draw.rectangle([pdf_left, pdf_top, pdf_left + pdf_width, pdf_top + size * 0.07],
                  fill=(220, 53, 69))

    # PDF yazısı
    try:
        font_size = int(size * 0.04)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

    draw.text((pdf_left + size * 0.07, pdf_top + size * 0.015), "PDF",
              font=font, fill=(255, 255, 255))

    # PDF içi çizgiler
    line_y = pdf_top + size * 0.10
    for i in range(4):
        line_width = (pdf_width * 0.75 if i < 3 else pdf_width * 0.45) - size * 0.03
        draw.rectangle([pdf_left + size * 0.025, line_y,
                       pdf_left + size * 0.025 + line_width, line_y + size * 0.02],
                      fill=(210, 210, 210))
        line_y += size * 0.04

    # Ok işareti (ortada) - daha belirgin
    arrow_center_x = size * 0.50
    arrow_center_y = size * 0.44
    arrow_length = size * 0.10

    # Ok gövdesi (kalın)
    draw.rectangle([arrow_center_x - arrow_length * 0.6, arrow_center_y - size * 0.025,
                   arrow_center_x + arrow_length * 0.2, arrow_center_y + size * 0.025],
                  fill=(255, 255, 255))

    # Ok ucu (üçgen)
    arrow_points = [
        (arrow_center_x + arrow_length * 0.2, arrow_center_y - size * 0.06),
        (arrow_center_x + arrow_length * 0.2, arrow_center_y + size * 0.06),
        (arrow_center_x + arrow_length * 0.7, arrow_center_y),
    ]
    draw.polygon(arrow_points, fill=(255, 255, 255))

    # Sağ taraf - Word belgesi
    word_left = size * 0.56
    word_top = size * 0.20
    word_width = size * 0.30
    word_height = size * 0.48

    # Word gölge
    draw.rectangle([word_left + 4, word_top + 4,
                   word_left + word_width + 4, word_top + word_height + 4],
                  fill=(20, 60, 180, 80))

    # Word kağıt
    draw.rectangle([word_left, word_top, word_left + word_width, word_top + word_height],
                  fill=(255, 255, 255))

    # Word üst mavi bant
    draw.rectangle([word_left, word_top, word_left + word_width, word_top + size * 0.07],
                  fill=(43, 87, 151))

    # W harfi
    draw.text((word_left + size * 0.10, word_top + size * 0.012), "W",
              font=font, fill=(255, 255, 255))

    # Word içi çizgiler (mavi - düzenli metin)
    line_y = word_top + size * 0.10
    for i in range(4):
        line_width = word_width * 0.80 - size * 0.03
        draw.rectangle([word_left + size * 0.025, line_y,
                       word_left + size * 0.025 + line_width, line_y + size * 0.02],
                      fill=(100, 149, 237))
        line_y += size * 0.04

    # Alt yazı - "PDF2Word"
    try:
        font_size = int(size * 0.10)
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font_bold = ImageFont.load_default()

    text = "PDF2Word"
    text_bbox = draw.textbbox((0, 0), text, font=font_bold)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size - text_width) / 2
    text_y = size - margin - size * 0.16

    # Metin gölgesi
    draw.text((text_x + 2, text_y + 2), text, font=font_bold, fill=(20, 60, 150))
    # Ana metin
    draw.text((text_x, text_y), text, font=font_bold, fill=(255, 255, 255))

    return img


def save_icons(base_path):
    """Farklı boyutlarda ikon kaydet"""

    # Ana ikon
    icon = create_pdf2word_icon(1024)

    # PNG kaydet
    sizes = [1024, 512, 256, 128, 64, 32, 16]

    for s in sizes:
        resized = icon.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(base_path, f"icon_{s}.png"))
        print(f"Saved: icon_{s}.png")

    # Ana ikon
    icon.save(os.path.join(base_path, "app_icon.png"))
    print("Saved: app_icon.png")

    # macOS iconset
    try:
        iconset_path = os.path.join(base_path, "app.iconset")
        os.makedirs(iconset_path, exist_ok=True)

        iconset_sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png"),
        ]

        for s, name in iconset_sizes:
            resized = icon.resize((s, s), Image.Resampling.LANCZOS)
            resized.save(os.path.join(iconset_path, name))

        print(f"Created iconset at: {iconset_path}")

    except Exception as e:
        print(f"Could not create iconset: {e}")

    # Windows ICO
    try:
        ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        ico_images = []
        for s in ico_sizes:
            resized = icon.resize(s, Image.Resampling.LANCZOS)
            ico_images.append(resized)

        ico_path = os.path.join(base_path, "app.ico")
        ico_images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in ico_images])
        print(f"Saved: app.ico")
    except Exception as e:
        print(f"Could not create ICO: {e}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_icons(script_dir)
    print("\nPDF2Word icon creation complete!")
