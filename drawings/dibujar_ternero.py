import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from entities.ternero import Ternero
from utils.imagen import escalar_y_recortar_imagen

def _assets_dir() -> Path:
    # sys._MEIPASS is set by PyInstaller when running as a frozen bundle
    import sys
    base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent.parent
    return base / "assets"

ASSETS_DIR = _assets_dir()
PLANILLA_TEMPLATE = ASSETS_DIR / "planillaVacia.jpg"
FONT_PATH = ASSETS_DIR / "LiberationSans-Regular.ttf"
FONT_SIZE = 52

# Pixel coordinates on the template (x, y) matching the original Go layout.
# y is the text baseline position, same as gg.DrawString behavior.
CAMPO_CONFIG: dict[str, dict] = {
    "Nombre":          {"x": 415,  "y": 128},
    "RP":              {"x": 1606, "y": 128},
    "RDeControl":      {"x": 2063, "y": 127},
    "Raza":            {"x": 405,  "y": 208},
    "HBA":             {"x": 1657, "y": 206},
    "Sexo":            {"x": 2070, "y": 204},
    "Color":           {"x": 374,  "y": 290},
    "FechaNacimiento": {"x": 1584, "y": 290},
    "Tambo":           {"x": 2100, "y": 288},
    "PadreRP":         {"x": 424,  "y": 1208},
    "PadreHBA":        {"x": 781,  "y": 1208},
    "PadreNombre":     {"x": 412,  "y": 1290},
    "MadreRP":         {"x": 1491, "y": 1209},
    "MadreHBA":        {"x": 1854, "y": 1209},
    "MadreCAL":        {"x": 2271, "y": 1209},
    "MadreNombre":     {"x": 1460, "y": 1293},
}

RECT_IMAGENES: dict[str, dict] = {
    "FotoIzquierda": {"x": 360,  "y": 428, "w": 802, "h": 564},
    "FotoDerecha":   {"x": 1440, "y": 428, "w": 802, "h": 564},
}

_FALLBACK_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def _get_font(size: int = FONT_SIZE) -> ImageFont.FreeTypeFont:
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    for path in _FALLBACK_FONTS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def generar_planilla_imagen(t: Ternero) -> Image.Image:
    template = Image.open(PLANILLA_TEMPLATE).convert("RGB")
    draw = ImageDraw.Draw(template)
    font = _get_font()

    def render_campo(nombre: str, valor: str) -> None:
        if not valor:
            return
        cfg = CAMPO_CONFIG.get(nombre)
        if not cfg:
            return
        # anchor="ls" = left baseline, matching gg.DrawString(x, y) where y is the baseline
        draw.text((cfg["x"], cfg["y"]), valor, font=font, fill="black", anchor="ls")

    render_campo("Nombre", "Pastoral " + t.nombre)
    render_campo("RP", t.rp)
    render_campo("RDeControl", t.r_de_control)
    render_campo("Raza", t.raza)
    render_campo("HBA", t.hba)
    render_campo("Sexo", t.sexo)
    render_campo("Color", t.color)

    if t.fecha_nac:
        cfg = CAMPO_CONFIG["FechaNacimiento"]
        draw.text(
            (cfg["x"], cfg["y"]),
            t.fecha_nac.strftime("%d/%m/%Y"),
            font=font,
            fill="black",
            anchor="ls",
        )

    render_campo("PadreRP", t.padre_rp)
    render_campo("PadreHBA", t.padre_hba)
    render_campo("PadreNombre", t.nombre_padre)
    render_campo("MadreRP", t.madre_rp)
    render_campo("MadreHBA", t.madre_hba)
    render_campo("MadreCAL", t.madre_cal)
    render_campo("MadreNombre", t.nombre_madre)

    _render_imagen(draw, template, "FotoIzquierda", t.foto_izquierda)
    _render_imagen(draw, template, "FotoDerecha", t.foto_derecha)

    # Rotate 90° counter-clockwise to match the original Go behavior
    return template.rotate(90, expand=True)


def _render_imagen(
    draw: ImageDraw.ImageDraw,
    template: Image.Image,
    nombre: str,
    ruta: str,
) -> None:
    rect = RECT_IMAGENES.get(nombre)
    if not rect:
        return

    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]

    if not ruta or not os.path.exists(ruta):
        _dibujar_placeholder(draw, x, y, w, h, "Sin imagen")
        return

    try:
        img = Image.open(ruta).convert("RGB")
        img_scaled = escalar_y_recortar_imagen(img, w, h)
        template.paste(img_scaled, (x, y))
    except Exception:
        _dibujar_placeholder(draw, x, y, w, h, "Error cargando")


def _dibujar_placeholder(
    draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, texto: str
) -> None:
    draw.rectangle([x, y, x + w, y + h], fill=(240, 240, 240), outline=(128, 128, 128), width=2)
    font_small = _get_font(24)
    draw.text(
        (x + w // 2, y + h // 2),
        texto,
        font=font_small,
        fill=(139, 0, 0),
        anchor="mm",
    )
