import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImagenesTernero:
    izquierda: str = ""
    derecha: str = ""


_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def autocargar_imagenes_ternero(rp: str, carpeta_imagenes: str) -> tuple[str, str]:
    if not rp or not carpeta_imagenes:
        return "", ""

    foto_izq = ""
    foto_der = ""

    for ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]:
        if not foto_izq:
            path = os.path.join(carpeta_imagenes, rp + "I" + ext)
            if os.path.exists(path):
                foto_izq = path
        if not foto_der:
            path = os.path.join(carpeta_imagenes, rp + "D" + ext)
            if os.path.exists(path):
                foto_der = path

    return foto_izq, foto_der


def buscar_imagenes_en_carpeta(carpeta: str) -> dict[str, ImagenesTernero]:
    resultado: dict[str, ImagenesTernero] = {}

    if not os.path.exists(carpeta):
        raise FileNotFoundError(f"La carpeta no existe: {carpeta}")

    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            continue

        p = Path(nombre)
        if p.suffix.lower() not in _IMAGE_EXTENSIONS:
            continue

        stem = p.stem
        if len(stem) < 2:
            continue

        ultimo = stem[-1].upper()
        rp = stem[:-1]

        if rp not in resultado:
            resultado[rp] = ImagenesTernero()

        if ultimo == "I":
            resultado[rp].izquierda = ruta
        elif ultimo == "D":
            resultado[rp].derecha = ruta

    return resultado


def validar_carpeta_imagenes(carpeta: str) -> int:
    if not os.path.exists(carpeta):
        raise FileNotFoundError("La carpeta no existe")

    contador = sum(
        1
        for nombre in os.listdir(carpeta)
        if os.path.isfile(os.path.join(carpeta, nombre))
        and Path(nombre).suffix.lower() in _IMAGE_EXTENSIONS
    )
    return contador
