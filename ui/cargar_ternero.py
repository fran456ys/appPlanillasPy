import asyncio
from datetime import datetime

import flet as ft

from entities.ternero import Ternero
from savings import savings


class FormPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.ternero = Ternero()

    def build(self) -> ft.Control:
        # Services auto-register with the page's ServiceRegistry on creation
        self.foto_izq_picker = ft.FilePicker()
        self.foto_der_picker = ft.FilePicker()
        self.save_picker = ft.FilePicker()

        # ── Datos Generales ──────────────────────────────────────────
        self.nombre_field = ft.TextField(label="Nombre", hint_text="Nombre del ternero", expand=2)
        self.rp_field = ft.TextField(label="R.P.", expand=1)
        self.r_control_field = ft.TextField(label="R. de Control", expand=1)
        self.raza_field = ft.TextField(label="Raza", expand=2)
        self.hba_field = ft.TextField(label="H.B.A.", expand=1)
        self.chapa_field = ft.TextField(label="Chapa", expand=1)
        self.color_field = ft.TextField(label="Color", expand=1)
        self.tambo_field = ft.TextField(label="Tambo", expand=1)

        self.fecha_label = ft.Text("Fecha: no seleccionada", size=14)
        self.date_picker = ft.DatePicker(
            on_change=self._on_date_change,
            first_date=datetime(1990, 1, 1),
            last_date=datetime(2035, 12, 31),
        )
        btn_fecha = ft.ElevatedButton(
            "Seleccionar Fecha",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.show_dialog(self.date_picker),
        )

        # ── Datos del Padre ──────────────────────────────────────────
        self.padre_rp_field = ft.TextField(label="R.P.", expand=1)
        self.padre_hba_field = ft.TextField(label="H.B.A.", expand=1)
        self.nombre_padre_field = ft.TextField(label="Nombre del Padre", expand=2)

        # ── Datos de la Madre ─────────────────────────────────────────
        self.madre_rp_field = ft.TextField(label="R.P.", expand=1)
        self.madre_hba_field = ft.TextField(label="H.B.A.", expand=1)
        self.madre_cal_field = ft.TextField(label="CAL", expand=1)
        self.nombre_madre_field = ft.TextField(label="Nombre de la Madre", expand=2)

        # ── Fotografías ───────────────────────────────────────────────
        self.slot_izq = _image_placeholder()
        self.slot_der = _image_placeholder()

        # ── Buttons ───────────────────────────────────────────────────
        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=12,
            controls=[
                ft.Text("Datos Generales", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([self.nombre_field, self.rp_field, self.r_control_field]),
                ft.Row([self.raza_field, self.hba_field, self.chapa_field,
                        self.color_field, self.tambo_field]),
                ft.Row([btn_fecha, self.fecha_label],
                       vertical_alignment=ft.CrossAxisAlignment.CENTER),

                ft.Divider(),
                ft.Text("Datos del Padre", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([self.padre_rp_field, self.padre_hba_field, self.nombre_padre_field]),

                ft.Divider(),
                ft.Text("Datos de la Madre", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([self.madre_rp_field, self.madre_hba_field,
                        self.madre_cal_field, self.nombre_madre_field]),

                ft.Divider(),
                ft.Text("Fotografías", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([
                        self.slot_izq,
                        ft.ElevatedButton(
                            "Cargar Foto Izquierda",
                            on_click=self._on_pick_foto_izq,
                        ),
                    ]),
                    ft.Column([
                        self.slot_der,
                        ft.ElevatedButton(
                            "Cargar Foto Derecha",
                            on_click=self._on_pick_foto_der,
                        ),
                    ]),
                ]),

                ft.Divider(),
                ft.Row([
                    ft.FilledButton("Guardar Ternero", on_click=self._on_guardar),
                    ft.FilledButton("Imprimir Planilla", on_click=self._on_guardar),
                ]),
            ],
        )

    # ── Callbacks ─────────────────────────────────────────────────────

    def _on_date_change(self, e: ft.ControlEvent) -> None:
        selected = self.date_picker.value
        if selected:
            self.ternero.fecha_nac = selected.date() if hasattr(selected, "date") else selected
            self.fecha_label.value = f"Fecha: {self.ternero.fecha_nac.strftime('%d/%m/%Y')}"
            self.page.update()

    async def _on_pick_foto_izq(self, e: ft.ControlEvent) -> None:
        files = await self.foto_izq_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["png", "jpg", "jpeg"],
        )
        if files:
            self.ternero.foto_izquierda = files[0].path
            _update_image_slot(self.slot_izq, files[0].path)
            self.page.update()

    async def _on_pick_foto_der(self, e: ft.ControlEvent) -> None:
        files = await self.foto_der_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["png", "jpg", "jpeg"],
        )
        if files:
            self.ternero.foto_derecha = files[0].path
            _update_image_slot(self.slot_der, files[0].path)
            self.page.update()

    async def _on_guardar(self, e: ft.ControlEvent) -> None:
        self._collect_fields()

        try:
            img = await asyncio.to_thread(savings.generar_imagen, self.ternero)
        except Exception as ex:
            _show_info(self.page, "Error", str(ex))
            return

        filename = savings.sanitize_filename(
            f"planilla_{self.ternero.nombre}_{self.ternero.rp}.png"
        )
        path = await self.save_picker.save_file(
            file_name=filename,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["png"],
        )
        if not path:
            return

        try:
            await asyncio.to_thread(savings.guardar_imagen, img, path)
            _show_info(self.page, "Éxito", f"Imagen guardada: {path}")
        except Exception as ex:
            _show_info(self.page, "Error", str(ex))

    def _collect_fields(self) -> None:
        self.ternero.nombre = self.nombre_field.value or ""
        self.ternero.rp = self.rp_field.value or ""
        self.ternero.r_de_control = self.r_control_field.value or ""
        self.ternero.raza = self.raza_field.value or ""
        self.ternero.hba = self.hba_field.value or ""
        self.ternero.sexo = self.chapa_field.value or ""
        self.ternero.color = self.color_field.value or ""
        self.ternero.padre_rp = self.padre_rp_field.value or ""
        self.ternero.padre_hba = self.padre_hba_field.value or ""
        self.ternero.nombre_padre = self.nombre_padre_field.value or ""
        self.ternero.madre_rp = self.madre_rp_field.value or ""
        self.ternero.madre_hba = self.madre_hba_field.value or ""
        self.ternero.madre_cal = self.madre_cal_field.value or ""
        self.ternero.nombre_madre = self.nombre_madre_field.value or ""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _image_placeholder() -> ft.Container:
    return ft.Container(
        width=200,
        height=200,
        border=ft.Border.all(1, ft.Colors.GREY_400),
        bgcolor=ft.Colors.GREY_100,
        content=ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE, color=ft.Colors.GREY_400, size=48),
        alignment=ft.Alignment.CENTER,
    )


def _update_image_slot(slot: ft.Container, path: str) -> None:
    slot.content = ft.Image(src=path, width=200, height=200, fit=ft.ImageFit.CONTAIN)


def _show_info(page: ft.Page, title: str, message: str) -> None:
    def on_ok(e):
        page.pop_dialog()

    page.show_dialog(ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[ft.TextButton("OK", on_click=on_ok)],
    ))
