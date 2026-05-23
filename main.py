import flet as ft

from ui.cargar_ternero import FormPage
from ui.importar_csv import ImportPage


def main(page: ft.Page) -> None:
    page.title = "Gestión de Terneros - Cabaña Pastoral"
    page.window.width = 1100
    page.window.height = 750
    page.padding = 16

    form_page = FormPage(page)
    import_page = ImportPage(page)

    tabs = ft.Tabs(
        length=2,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Cargar Ternero", icon=ft.Icons.EDIT_NOTE),
                        ft.Tab(label="Importar CSV", icon=ft.Icons.LIST_ALT),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(content=form_page.build(), expand=True, padding=8),
                        ft.Container(content=import_page.build(), expand=True, padding=8),
                    ],
                ),
            ],
        ),
    )

    page.add(tabs)


if __name__ == "__main__":
    ft.run(main)
