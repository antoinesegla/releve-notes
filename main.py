import flet as ft

def main(page: ft.Page):
    page.bgcolor = "#0b0d10"
    page.add(
        ft.Column([
            ft.Text("CA MARCHE !", size=30, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("Si tu vois ça, le build fonctionne", color="green"),
            ft.ElevatedButton("Bouton test", on_click=lambda e: print("ok"))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(main)
