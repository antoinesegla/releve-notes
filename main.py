
import flet as ft

MATIERES = [
    ("Français", "fr", 3), ("Anglais", "an", 2), ("Mathématiques", "ma", 4),
    ("EST", "es", 5), ("PCT", "pc", 4), ("Dessin", "de", 4),
    ("Technologie", "te", 2), ("Législation", "le", 1), ("Philosophie", "ph", 1),
    ("TP", "tp", 6), ("MEL", "me", 5), ("Électrotechnique", "el", 4), ("EPS", "ep", 1),
]

STORAGE_KEY = "releve_flet_v4_mobile"

def main(page: ft.Page):
    page.title = "Relevé de Notes"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b0d10"
    page.padding = 12
    page.scroll = ft.ScrollMode.ADAPTIVE

    coefs = {code: c for _, code, c in MATIERES}
    notes_data = {}
    coefs_inputs = {}

    txt_moyenne_generale = ft.Text("—", size=28, weight=ft.FontWeight.BOLD, color="white")
    txt_mention = ft.Text("Aucune note", size=11, color="#94a3b8")

    def calc_moyenne():
        total_points = 0
        total_coefs = 0
        for nom, code, _ in MATIERES:
            try:
                coef_val = float(coefs_inputs[code].value.replace(",", ".") or 0)
            except:
                coef_val = coefs[code]
            coefs[code] = coef_val
            
            notes = []
            for k in [f"{code}_i{i}" for i in range(1,5)] + [f"{code}_d{i}" for i in range(1,4)]:
                try:
                    v = notes_data[k].value
                    if v:
                        notes.append(float(v.replace(",", ".").strip()))
                except:
                    pass
            
            if notes:
                moy = sum(notes) / len(notes)
                notes_data[f"{code}_moy"].value = f"{moy:.2f}"
                notes_data[f"{code}_mc"].value = f"{moy * coef_val:.1f}"
                total_points += moy * coef_val
                total_coefs += coef_val
                # Moy inter / dev séparés si tu veux, ici on simplifie
                notes_data[f"{code}_moy_i"].value = f"{moy:.1f}"
            else:
                notes_data[f"{code}_moy"].value = "—"
                notes_data[f"{code}_mc"].value = "—"
                notes_data[f"{code}_moy_i"].value = "—"
        
        if total_coefs > 0:
            mg = total_points / total_coefs
            txt_moyenne_generale.value = f"{mg:.2f}"
            if mg >= 16: txt_mention.value = "Excellent"
            elif mg >= 14: txt_mention.value = "Très Bien"
            elif mg >= 12: txt_mention.value = "Bien"
            elif mg >= 10: txt_mention.value = "Passable"
            else: txt_mention.value = "Insuffisant"
        else:
            txt_moyenne_generale.value = "—"
            txt_mention.value = "Aucune note"
        
        # Sauvegarde
        try:
            data = {}
            for k, v in notes_data.items():
                if hasattr(v, 'value'):
                    data[k] = v.value
            for code, inp in coefs_inputs.items():
                data[f"coef_{code}"] = inp.value
            page.client_storage.set(STORAGE_KEY, data)
        except:
            pass
        page.update()

    def load_data():
        try:
            saved = page.client_storage.get(STORAGE_KEY)
            if not saved:
                return
            for k, v in saved.items():
                if k.startswith("coef_"):
                    code = k.replace("coef_", "")
                    if code in coefs_inputs:
                        coefs_inputs[code].value = str(v)
                elif k in notes_data and hasattr(notes_data[k], 'value'):
                    notes_data[k].value = str(v)
        except:
            pass

    # Header
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("RELEVÉ DE NOTES", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("CPET LE PHENIX • 2025-2026", size=10, color="#64748b"),
                ], spacing=2),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("MOYENNE", size=8, weight=ft.FontWeight.BOLD, color="#60a5fa", text_align=ft.TextAlign.CENTER),
                        txt_moyenne_generale,
                        txt_mention,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    bgcolor="#0f172a", border=ft.border.all(1, "#1e3a5f"),
                    border_radius=12, padding=12, width=120,
                )
            ])
        ]),
        bgcolor="#151a23", border=ft.border.all(1, "#1e293b"), border_radius=14, padding=14,
    )

    # Table
    rows = []
    for idx, (nom, code, coef) in enumerate(MATIERES):
        inp_coef = ft.TextField(value=str(coef), width=45, height=38, text_size=11,
                                bgcolor="#232a36", border_color="#334155", color="white",
                                on_change=lambda e: calc_moyenne())
        coefs_inputs[code] = inp_coef

        inputs = []
        for n in range(1, 5):
            tf = ft.TextField(width=48, height=38, text_size=11, hint_text=f"I{n}",
                              bgcolor="#232a36", border_color="#334155", color="white",
                              on_change=lambda e: calc_moyenne())
            notes_data[f"{code}_i{n}"] = tf
            inputs.append(tf)
        for n in range(1, 4):
            tf = ft.TextField(width=48, height=38, text_size=11, hint_text=f"D{n}",
                              bgcolor="#1a2332", border_color="#1e3a5f", color="white",
                              on_change=lambda e: calc_moyenne())
            notes_data[f"{code}_d{n}"] = tf
            inputs.append(tf)

        lbl_moy_i = ft.Text("—", size=11, weight=ft.FontWeight.BOLD, color="white")
        notes_data[f"{code}_moy_i"] = lbl_moy_i
        cont_moy_i = ft.Container(content=lbl_moy_i, bgcolor="#1e293b", padding=6, border_radius=6, width=55, alignment=ft.alignment.center)

        lbl_moy = ft.Text("—", size=11, weight=ft.FontWeight.BOLD, color="#60a5fa")
        notes_data[f"{code}_moy"] = lbl_moy
        cont_moy = ft.Container(content=lbl_moy, bgcolor="#0f172a", padding=6, border_radius=6, width=55, alignment=ft.alignment.center, border=ft.border.all(1, "#1e3a5f"))

        lbl_mc = ft.Text("—", size=11, weight=ft.FontWeight.BOLD, color="white")
        notes_data[f"{code}_mc"] = lbl_mc

        row = ft.Row([
            inp_coef,
            ft.Container(content=ft.Text(nom, size=11, weight=ft.FontWeight.W_600, color="white"), width=95),
            *inputs,
            cont_moy_i,
            cont_moy,
            ft.Container(content=lbl_mc, width=45, alignment=ft.alignment.center),
        ], spacing=6, scroll=ft.ScrollMode.AUTO)

        rows.append(
            ft.Container(content=row, bgcolor="#1a1f2b" if idx % 2 == 0 else "#151a23", padding=8, border_radius=8)
        )

    table_header = ft.Row([
        ft.Container(width=45, content=ft.Text("Coef", size=9, weight=ft.FontWeight.BOLD, color="#60a5fa")),
        ft.Container(width=95, content=ft.Text("Matière", size=9, weight=ft.FontWeight.BOLD, color="white")),
        ft.Text("Notes Interro + Devoirs", size=9, color="#64748b"),
    ])

    content = ft.Column([
        header,
        ft.Divider(height=10, color="transparent"),
        table_header,
        *rows,
        ft.Divider(height=20, color="transparent"),
        ft.Text("Les notes sont sauvegardées automatiquement", size=10, color="#475569", text_align=ft.TextAlign.CENTER),
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(content)
    load_data()
    calc_moyenne()

ft.app(main)
