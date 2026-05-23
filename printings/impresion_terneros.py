import io
import os
import platform
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from fpdf import FPDF
from PIL import Image

from drawings.dibujar_ternero import generar_planilla_imagen
from entities.ternero import Ternero

PDF_WIDTH_MM = 160
PDF_HEIGHT_MM = 260
PDF_IMG_Y_OFFSET = 10
TMP_DELETE_DELAY_S = 120


def _tmp_pdf_path() -> str:
    return os.path.join(tempfile.gettempdir(), "planillas_terneros.pdf")

# PNG compress_level=1 is ~10x faster than default (6) with ~20% larger output —
# acceptable for a temporary print file that gets deleted in 2 minutes.
_PNG_COMPRESS_LEVEL = 1


def imprimir_terneros(terneros: list[Ternero]) -> None:
    """Generate + encode every planilla in parallel, then assemble the PDF."""
    workers = min(len(terneros), (os.cpu_count() or 2) * 2)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        # executor.map preserves order — no manual index tracking needed
        paginas: list[bytes] = list(pool.map(_generar_y_codificar, terneros))

    _ensamblar_e_imprimir(paginas)


def imprimir_imagenes(imgs: list[Image.Image]) -> None:
    """Encode already-generated images in parallel, then assemble the PDF."""
    workers = min(len(imgs), (os.cpu_count() or 2) * 2)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        paginas: list[bytes] = list(pool.map(_codificar_png, imgs))

    _ensamblar_e_imprimir(paginas)


# ── Per-thread work units ──────────────────────────────────────────────────────

def _generar_y_codificar(t: Ternero) -> bytes:
    """Generate planilla image and encode to PNG bytes in one thread — avoids
    a second synchronisation barrier between generation and encoding."""
    img = generar_planilla_imagen(t)
    return _codificar_png(img)


def _codificar_png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=False, compress_level=_PNG_COMPRESS_LEVEL)
    return buf.getvalue()


# ── PDF assembly (sequential — fpdf2 is not thread-safe) ──────────────────────

def _ensamblar_e_imprimir(paginas: list[bytes]) -> None:
    pdf = FPDF(unit="mm", format=[PDF_WIDTH_MM, PDF_HEIGHT_MM])
    for png_bytes in paginas:
        pdf.add_page()
        pdf.image(
            io.BytesIO(png_bytes),
            x=0,
            y=PDF_IMG_Y_OFFSET,
            w=PDF_WIDTH_MM,
            h=PDF_HEIGHT_MM - PDF_IMG_Y_OFFSET,
        )

    path = _tmp_pdf_path()
    pdf.output(path)
    threading.Thread(target=_auto_delete, args=(path,), daemon=True).start()
    _imprimir_pdf(path)


def _imprimir_pdf(path: str) -> None:
    system = platform.system()
    if system == "Windows":
        abs_path = os.path.abspath(path)
        subprocess.run(["cmd", "/c", "start", "", "/wait", abs_path], check=True)
    elif system == "Linux":
        result = subprocess.run(["lp", path], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"lp falló: {result.stderr}")
    else:
        raise RuntimeError(f"SO no soportado: {system}")


def _auto_delete(path: str) -> None:
    time.sleep(TMP_DELETE_DELAY_S)
    try:
        os.remove(path)
    except OSError:
        pass
