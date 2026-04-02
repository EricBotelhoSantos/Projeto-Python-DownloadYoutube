import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

def create_modern_bg():
    print("Gerando background ultra moderno e sofisticado para o NexusTube...")
    # Resolução Alta 1920x1080
    width, height = 1920, 1080
    
    # 1. Criar camada base (Dark Mode premium, um grafite azulado profundo)
    backdrop = Image.new("RGBA", (width, height), (15, 17, 22, 255))
    draw = ImageDraw.Draw(backdrop)
    
    # 2. Grid de interface sutil cyberpunk/hacker
    grid_color = (255, 255, 255, 5) # quase invisível
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        
    # 3. Adicionar brilho desfocado ao invés de formas duras (estilo Glassmorphism / UI Moderna)
    # Criamos uma camada separada que será muito borrada
    glow_layer = Image.new("RGBA", (width, height), (0,0,0,0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Orbe verde neon grande no centro escuro
    gx, gy = width//2, height//2
    glow_radius = 500
    glow_draw.ellipse(
        [(gx - glow_radius, gy - glow_radius), 
         (gx + glow_radius, gy + glow_radius)],
        fill=(0, 230, 118, 30) # #00E676 (Verde do seu botão) com transparência
    )
    
    # Aplicar Gaussian Blur forte para dissolver a luz
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(150))
    
    # Mesclar o brilho no backdrop
    image = Image.alpha_composite(backdrop, glow_layer)
    draw = ImageDraw.Draw(image)
    
    # 4. Ondas e linhas tecnológicas fluindo do canto
    random.seed(99) # Fixo para padronizar
    for i in range(-500, width+height, 120):
        # Linhas oblíquas ultra modernas
        draw.line([(i, -100), (i+1500, height+100)], fill=(0, 230, 118, 15), width=2)
        
    # 5. Adicionando partículas de rede (nós quânticos esparsos)
    for _ in range(120):
        px = random.randint(0, width)
        py = random.randint(0, height)
        raio = random.randint(1, 3)
        # Ponto luminoso
        draw.ellipse([(px-raio, py-raio), (px+raio, py+raio)], fill=(120, 255, 200, 180))
        
        # Conexões em linha reta sutis com outro nó fantasma
        if random.random() > 0.6:
            dx = px + random.randint(-150, 150)
            dy = py + random.randint(-150, 150)
            draw.line([(px, py), (dx, dy)], fill=(0, 230, 118, 35), width=1)

    # Converter de volta para RGB para salvar normalmente como PNG opaco
    final_image = image.convert("RGB")
    file_path = "bg.png"
    
    final_image.save(file_path, "PNG", optimize=True)
    print(f"Sucesso! Imagem moderna '{file_path}' (Glassmorphism + Neon) foi gerada!")

if __name__ == "__main__":
    create_modern_bg()
