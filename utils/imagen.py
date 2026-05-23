from PIL import Image


def escalar_y_recortar_imagen(img: Image.Image, ancho_destino: int, alto_destino: int) -> Image.Image:
    ancho_origen, alto_origen = img.size

    escala_x = ancho_destino / ancho_origen
    escala_y = alto_destino / alto_origen
    escala = min(escala_x, escala_y)

    nuevo_ancho = int(ancho_origen * escala)
    nuevo_alto = int(alto_origen * escala)

    img_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    resultado = Image.new("RGB", (ancho_destino, alto_destino), (255, 255, 255))
    offset_x = (ancho_destino - nuevo_ancho) // 2
    offset_y = (alto_destino - nuevo_alto) // 2
    resultado.paste(img_redimensionada, (offset_x, offset_y))

    return resultado
