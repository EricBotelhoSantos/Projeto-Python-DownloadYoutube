import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter


def create_modern_bg():
    """Gera o background Glassmorphism premium para o NexusTube Downloader."""
    print("Gerando background ultra moderno e sofisticado para o NexusTube...")

    width, height = 1920, 1080

    # 1. Camada base (Dark Mode premium)
    backdrop = Image.new("RGBA", (width, height), (15, 17, 22, 255))
    draw = ImageDraw.Draw(backdrop)

    # 2. Grid sutil cyberpunk
    grid_color = (255, 255, 255, 5)
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # 3. Brilho Glassmorphism desfocado
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    gx, gy = width // 2, height // 2
    glow_radius = 500
    glow_draw.ellipse(
        [(gx - glow_radius, gy - glow_radius),
         (gx + glow_radius, gy + glow_radius)],
        fill=(0, 230, 118, 30)
    )

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(150))

    image = Image.alpha_composite(backdrop, glow_layer)
    draw = ImageDraw.Draw(image)

    # 4. Linhas oblíquas tecnológicas
    random.seed(99)
    for i in range(-500, width + height, 120):
        draw.line([(i, -100), (i + 1500, height + 100)], fill=(0, 230, 118, 15), width=2)

    # 5. Partículas de rede (nós quânticos)
    for _ in range(120):
        px = random.randint(0, width)
        py = random.randint(0, height)
        raio = random.randint(1, 3)
        draw.ellipse([(px - raio, py - raio), (px + raio, py + raio)], fill=(120, 255, 200, 180))

        if random.random() > 0.6:
            dx = px + random.randint(-150, 150)
            dy = py + random.randint(-150, 150)
            draw.line([(px, py), (dx, dy)], fill=(0, 230, 118, 35), width=1)

    # Salvar na pasta de assets do desktop
    final_image = image.convert("RGB")

    # Caminho de saída: desktop/assets/bg.png
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "desktop", "assets")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "bg.png")

    final_image.save(file_path, "PNG", optimize=True)
    print(f"Sucesso! Imagem '{file_path}' (Glassmorphism + Neon) gerada!")


if __name__ == "__main__":
    create_modern_bg()
