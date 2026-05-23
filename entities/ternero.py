from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Ternero:
    nombre: str = ""
    rp: str = ""
    r_de_control: str = ""
    raza: str = ""
    hba: str = ""
    sexo: str = ""
    color: str = ""
    fecha_nac: Optional[date] = None
    padre_rp: str = ""
    padre_hba: str = ""
    nombre_padre: str = ""
    madre_rp: str = ""
    madre_hba: str = ""
    madre_cal: str = ""
    nombre_madre: str = ""
    foto_izquierda: str = ""
    foto_derecha: str = ""
