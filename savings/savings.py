import os
import re
from PIL import Image

from drawings.dibujar_ternero import generar_planilla_imagen
from entities.ternero import Ternero


def generar_imagen(t: Ternero) -> Image.Image:
    return generar_planilla_imagen(t)


def guardar_imagen(img: Image.Image, path: str) -> None:
    img.save(path, "PNG")


def guardar_multiple(
    terneros: list[Ternero], output_dir: str = "planillas_lote"
) -> tuple[int, int]:
    os.makedirs(output_dir, exist_ok=True)
    errores = 0
    for t in terneros:
        try:
            img = generar_planilla_imagen(t)
            filename = sanitize_filename(f"{t.nombre}_{t.rp}.png")
            img.save(os.path.join(output_dir, filename), "PNG")
        except Exception:
            errores += 1
    exitosos = len(terneros) - errores
    return exitosos, errores


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[/\\:*?"<>|]', "-", filename)
