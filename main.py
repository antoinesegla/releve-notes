
import flet as ft
import json
from pathlib import Path

MATIERES = [
    ("Français", "fr", 3),
    ("Anglais", "an", 2),
    ("Mathématiques", "ma", 4),
    ("EST", "es", 5),
    ("PCT", "pc", 4),
    ("Dessin", "de", 4),
    ("Technologie", "te", 2),
    ("Législation", "le", 1),
    ("Philosophie", "ph", 1),
    ("TP", "tp", 6),
    ("MEL", "me", 5),
    ("Électrotechnique", "el", 2),
    ("EPS", "ep", 1),
]

STORAGE_KEY = "releve_flet_v4"
THEME_KEY = "theme_mode_v4"
try:
    DATA_FILE = Path(__file__).parent / "releve_data.json"
except:
    DATA_FILE = Path.home() / "releve_data.json"
DATA_FILE_BACKUP = Path.home() / ".releve_notes_flet.json"

THEMES = {
    "dark": {
        "page_bg": "#0b0d10",
        "card_bg": "#151a23",
        "card_bg_alt": "#141a23",
        "card_border": "#1e293b",
        "input_bg": "#232a36",
        "input_border": "#334155",
        "table_bg": "#151a23",
        "table_header": "#1e293b",
        "table_border": "#1e293b",
        "row_even": "#1a1f2b",
        "row_odd": "#151a23",
        "text_primary": "white",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "pill_bg": "#0f172a",
        "pill_bg_int": "#1e293b",
        "pill_border": "#1e3a5f",
        "pill_text": "white",
        "divider": "#1e293b",
        "badge_bg": "#1a1e24",
    },
    "light": {
        "page_bg": "#f1f5f9",
        "card_bg": "white",
        "card_bg_alt": "#ffffff",
        "card_border": "#e2e8f0",
        "input_bg": "#f8fafc",
        "input_border": "#cbd5e1",
        "table_bg": "white",
        "table_header": "#f1f5f9",
        "table_border": "#e2e8f0",
        "row_even": "#f8fafc",
        "row_odd": "white",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_muted": "#94a3b8",
        "pill_bg": "#dbeafe",
        "pill_bg_int": "#e0f2fe",
        "pill_border": "#93c5fd",
        "pill_text": "#1e3a8a",
        "divider": "#e2e8f0",
        "badge_bg": "#f1f5f9",
    }
}

def main(page: ft.Page):
    page.title = "Relevé de Notes - Mobile"
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO
    try:
        page.window.width = 860
        page.window.height = 940
        page.window.resizable = True
        page.window.center()
    except:
        pass

    # Thème sauvegardé
    is_dark = True
    try:
        saved_theme = page.client_storage.get(THEME_KEY)
        if saved_theme == "light":
            is_dark = False
    except:
        pass

    is_dark_ref = [is_dark]
    colors = THEMES["dark" if is_dark else "light"]
    colors_ref = [colors]
    page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
    page.bgcolor = colors["page_bg"]

    notes_data = {}
    coefs_inputs = {}
    coefs = {code: c for _, code, c in MATIERES}
    eleve_inputs = {}
    
    # Pour pouvoir mettre à jour les pills en mode clair/sombre
    moy_int_containers = []
    moy_containers = []
    moy_int_texts = []
    moy_texts = []
    moy_coef_texts = []

    txt_titre_app = ft.Text("RELEVÉ DE NOTES", size=20, weight=ft.FontWeight.BOLD, color=colors["text_primary"])
    txt_sous_titre = ft.Text("Suivi académique • CPET LE PHENIX", size=10, color=colors["text_muted"])
    txt_nom_ecole_badge = ft.Text("CPET LE PHENIX", size=11, weight=ft.FontWeight.W_600, color=colors["text_secondary"])
    txt_moyenne_generale = ft.Text("—", size=26, weight=ft.FontWeight.BOLD, color=colors["text_primary"])
    txt_mention = ft.Text("Aucune note", size=10, weight=ft.FontWeight.W_500, color=colors["text_secondary"])

    def fermer_dialogue(dlg):
        dlg.open = False
        page.update()

    def ouvrir_a_propos(e):
        dlg = ft.AlertDialog(
            title=ft.Text("À propos"),
            content=ft.Column([
                ft.Markdown(
                    "**Application Relevé de Notes**\n\n"
                    "Version 1.0\n\n"
                    "**Développé par :** Antoine Epiphane Segla\n\n"
                    "© 2026"
                ),
            ], tight=True, spacing=10),
            actions=[ft.TextButton("OK", on_click=lambda _: fermer_dialogue(dlg))]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    btn_apropos = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, size=12, color="white"),
            ft.Text("À propos", size=11, weight=ft.FontWeight.BOLD, color="white"),
        ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.Padding(left=14, right=14, top=8, bottom=8),
        bgcolor="#1e293b",
        border_radius=20,
        ink=True,
        on_click=ouvrir_a_propos
    )

    btn_theme = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE_ROUNDED if is_dark else ft.Icons.DARK_MODE_ROUNDED,
        icon_color=colors["text_secondary"],
        tooltip="Clair/Sombre",
        icon_size=20,
        style=ft.ButtonStyle(bgcolor=colors["badge_bg"]),
    )

    moyenne_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ANALYTICS_ROUNDED, size=10, color="blue400"),
                ft.Text("MOYENNE", size=8, weight=ft.FontWeight.BOLD, color="blue400"),
            ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
            txt_moyenne_generale,
            ft.Container(
                content=txt_mention,
                bgcolor=colors["pill_bg"],
                padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                border_radius=10,
                border=ft.Border.all(1, colors["pill_border"]),
            )
        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=10,
        bgcolor=colors["pill_bg"],
        border=ft.Border.all(1, colors["pill_border"]),
        border_radius=12,
        width=135,
    )

    badge_annee = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=10, color=colors["text_secondary"]),
            ft.Text("2025-2026", size=9, color=colors["text_secondary"]),
        ], spacing=3),
        bgcolor=colors["badge_bg"],
        padding=ft.Padding(left=8, right=8, top=4, bottom=4),
        border_radius=12,
        border=ft.Border.all(1, colors["card_border"]),
    )

    entete = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=14, color="white"),
                    bgcolor="blue700",
                    padding=6,
                    border_radius=8,
                ),
                txt_nom_ecole_badge,
                ft.Container(expand=True),
                badge_annee,
                btn_theme,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            ft.Divider(height=12, color=colors["divider"], thickness=1),
            ft.Row([
                ft.Column([
                    txt_titre_app,
                    txt_sous_titre,
                    ft.Container(height=4),
                    ft.Row([
                        ft.Container(width=24, height=3, bgcolor="blue500", border_radius=2),
                        ft.Container(width=12, height=3, bgcolor=colors["pill_border"], border_radius=2),
                    ], spacing=4)
                ], spacing=2, expand=True),
                moyenne_card
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], spacing=0),
        padding=14,
        bgcolor=colors["card_bg_alt"],
        border=ft.Border.all(1, colors["card_border"]),
        border_radius=16,
    )

    style_input_discret = {
        "text_size": 12,
        "height": 36,
        "content_padding": ft.Padding(left=4, right=4, top=0, bottom=6),
        "border": ft.UnderlineInputBorder(),
        "text_align": ft.TextAlign.CENTER,
        "bgcolor": "transparent",
        "focused_border_color": "blue400",
        "keyboard_type": ft.KeyboardType.NUMBER,
    }

    style_coef = {
        "text_size": 12,
        "height": 36,
        "content_padding": ft.Padding(left=4, right=4, top=0, bottom=6),
        "border": ft.UnderlineInputBorder(),
        "text_align": ft.TextAlign.CENTER,
        "bgcolor": colors["input_bg"],
        "focused_border_color": "blue400",
        "keyboard_type": ft.KeyboardType.NUMBER,
    }

    style_eleve = {
        "text_size": 13,
        "height": 50,
        "border_radius": 10,
        "content_padding": ft.Padding(left=14, right=14, top=14, bottom=14),
        "bgcolor": colors["input_bg"],
        "border_color": colors["input_border"],
        "focused_border_color": "blue400",
        "label_style": ft.TextStyle(size=10, color=colors["text_secondary"]),
        "hint_style": ft.TextStyle(size=11, color=colors["text_muted"]),
        "text_style": ft.TextStyle(size=13, color=colors["text_primary"]),
    }

    def save_data():
        try:
            data = {
                "eleve": {k: v.value or "" for k, v in eleve_inputs.items()},
                "coefs": {k: v.value or "" for k, v in coefs_inputs.items()},
                "notes": {k: v.value or "" for k, v in notes_data.items() if isinstance(v, ft.TextField)},
                "_theme": "dark" if is_dark_ref[0] else "light",
            }
            json_str = json.dumps(data, ensure_ascii=False)
            try:
                page.client_storage.set(STORAGE_KEY, json_str)
                page.client_storage.set(THEME_KEY, "dark" if is_dark_ref[0] else "light")
            except:
                pass
            try:
                DATA_FILE.write_text(json_str, encoding="utf-8")
            except:
                pass
            try:
                DATA_FILE_BACKUP.write_text(json_str, encoding="utf-8")
            except:
                pass
        except Exception as e:
            print(f"Save error: {e}")

    def recalculer_et_mettre_a_jour():
        total_points = 0.0
        total_coefs = 0.0
        for nom, code, coef_actuel in MATIERES:
            c_val = coefs.get(code, coef_actuel)
            i_vals = []
            for n in range(1, 5):
                ref = notes_data.get(f"{code}_i{n}")
                if ref and ref.value:
                    try:
                        i_vals.append(float(ref.value.replace(",", ".")))
                    except:
                        pass
            moy_interro = sum(i_vals) / len(i_vals) if i_vals else None
            d_vals = []
            for n in range(1, 4):
                ref = notes_data.get(f"{code}_d{n}")
                if ref and ref.value:
                    try:
                        d_vals.append(float(ref.value.replace(",", ".")))
                    except:
                        pass
            valeurs = list(d_vals)
            if moy_interro is not None:
                valeurs.insert(0, moy_interro)
            moyenne = sum(valeurs) / len(valeurs) if valeurs else None
            
            if f"{code}_moy_i" in notes_data:
                notes_data[f"{code}_moy_i"].value = f"{moy_interro:.2f}" if moy_interro is not None else "—"
            if f"{code}_moy" in notes_data:
                notes_data[f"{code}_moy"].value = f"{moyenne:.2f}" if moyenne is not None else "—"
            if f"{code}_mc" in notes_data:
                if moyenne is not None:
                    mc = moyenne * c_val
                    notes_data[f"{code}_mc"].value = f"{mc:.2f}"
                    total_points += mc
                    total_coefs += c_val
                else:
                    notes_data[f"{code}_mc"].value = "—"

        if total_coefs > 0:
            mg = total_points / total_coefs
            txt_moyenne_generale.value = f"{mg:.2f}"
            if mg >= 16:
                txt_mention.value = "Très bien"
            elif mg >= 14:
                txt_mention.value = "Bien"
            elif mg >= 12:
                txt_mention.value = "Assez bien"
            elif mg >= 10:
                txt_mention.value = "Passable"
            else:
                txt_mention.value = "Insuffisant"
        else:
            txt_moyenne_generale.value = "—"
            txt_mention.value = "Aucune note"
        save_data()
        page.update()

    def apply_theme():
        c = THEMES["dark" if is_dark_ref[0] else "light"]
        colors_ref[0] = c
        page.theme_mode = ft.ThemeMode.DARK if is_dark_ref[0] else ft.ThemeMode.LIGHT
        page.bgcolor = c["page_bg"]
        entete.bgcolor = c["card_bg_alt"]
        entete.border = ft.Border.all(1, c["card_border"])
        txt_titre_app.color = c["text_primary"]
        txt_sous_titre.color = c["text_muted"]
        txt_nom_ecole_badge.color = c["text_secondary"]
        txt_moyenne_generale.color = c["text_primary"]
        badge_annee.bgcolor = c["badge_bg"]
        badge_annee.border = ft.Border.all(1, c["card_border"])
        moyenne_card.bgcolor = c["pill_bg"]
        moyenne_card.border = ft.Border.all(1, c["pill_border"])
        eleve_card.bgcolor = c["card_bg"]
        eleve_card.border = ft.Border.all(1, c["card_border"])
        lbl_eleve.color = c["text_secondary"]
        tableau_container.bgcolor = c["table_bg"]
        tableau_container.border = ft.Border.all(1, c["card_border"])
        data_table.heading_row_color = c["table_header"]
        data_table.border = ft.Border.all(1, c["table_border"])
        lbl_table.color = c["text_secondary"]

        for idx, row in enumerate(data_table.rows):
            row.color = c["row_even"] if idx % 2 == 0 else c["row_odd"]

        # FIX PRINCIPAL: pills moyenne
        for cont in moy_int_containers:
            cont.bgcolor = c["pill_bg_int"]
            cont.border = ft.Border.all(1, c["pill_border"])
        for cont in moy_containers:
            cont.bgcolor = c["pill_bg"]
            cont.border = ft.Border.all(1, c["pill_border"])
        for txt in moy_int_texts:
            txt.color = c["pill_text"] if not is_dark_ref[0] else "white"
        for txt in moy_texts:
            txt.color = "#2563eb" if not is_dark_ref[0] else "white"
        for txt in moy_coef_texts:
            txt.color = c["text_primary"]

        for k, inp in eleve_inputs.items():
            inp.bgcolor = c["input_bg"]
            inp.border_color = c["input_border"]
            inp.text_style = ft.TextStyle(size=13, color=c["text_primary"])
            inp.label_style = ft.TextStyle(size=10, color=c["text_secondary"])

        for k, inp in coefs_inputs.items():
            inp.bgcolor = c["input_bg"]

        btn_theme.icon = ft.Icons.LIGHT_MODE_ROUNDED if is_dark_ref[0] else ft.Icons.DARK_MODE_ROUNDED
        btn_theme.icon_color = c["text_secondary"]
        btn_theme.style = ft.ButtonStyle(bgcolor=c["badge_bg"])
        page.update()

    def toggle_theme(e):
        is_dark_ref[0] = not is_dark_ref[0]
        apply_theme()
        save_data()

    btn_theme.on_click = toggle_theme
    colors_ref = [colors]

    def load_data():
        data = None
        try:
            raw = page.client_storage.get(STORAGE_KEY)
            if raw:
                data = json.loads(raw)
        except:
            pass
        if data is None:
            try:
                if DATA_FILE.exists():
                    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                elif DATA_FILE_BACKUP.exists():
                    data = json.loads(DATA_FILE_BACKUP.read_text(encoding="utf-8"))
            except:
                pass
        if not data:
            return
        try:
            if data.get("_theme") == "light":
                is_dark_ref[0] = False
                apply_theme()
            elif data.get("_theme") == "dark":
                is_dark_ref[0] = True
                apply_theme()
            for k, v in data.get("eleve", {}).items():
                if k in eleve_inputs:
                    eleve_inputs[k].value = v
            for k, v in data.get("coefs", {}).items():
                if k in coefs_inputs:
                    coefs_inputs[k].value = str(v)
                    try:
                        coefs[k] = float(str(v).replace(",", "."))
                    except:
                        pass
            for k, v in data.get("notes", {}).items():
                if k in notes_data and isinstance(notes_data[k], ft.TextField):
                    notes_data[k].value = str(v)
            # recalcul
            total_points = 0.0
            total_coefs = 0.0
            for nom, code, coef_actuel in MATIERES:
                c_val = coefs.get(code, coef_actuel)
                i_vals = []
                for n in range(1, 5):
                    ref = notes_data.get(f"{code}_i{n}")
                    if ref and ref.value:
                        try:
                            i_vals.append(float(ref.value.replace(",", ".")))
                        except:
                            pass
                moy_interro = sum(i_vals) / len(i_vals) if i_vals else None
                d_vals = []
                for n in range(1, 4):
                    ref = notes_data.get(f"{code}_d{n}")
                    if ref and ref.value:
                        try:
                            d_vals.append(float(ref.value.replace(",", ".")))
                        except:
                            pass
                valeurs = list(d_vals)
                if moy_interro is not None:
                    valeurs.insert(0, moy_interro)
                moyenne = sum(valeurs) / len(valeurs) if valeurs else None
                if f"{code}_moy_i" in notes_data:
                    notes_data[f"{code}_moy_i"].value = f"{moy_interro:.2f}" if moy_interro is not None else "—"
                if f"{code}_moy" in notes_data:
                    notes_data[f"{code}_moy"].value = f"{moyenne:.2f}" if moyenne is not None else "—"
                if f"{code}_mc" in notes_data:
                    if moyenne is not None:
                        mc = moyenne * c_val
                        notes_data[f"{code}_mc"].value = f"{mc:.2f}"
                        total_points += mc
                        total_coefs += c_val
                    else:
                        notes_data[f"{code}_mc"].value = "—"
            if total_coefs > 0:
                mg = total_points / total_coefs
                txt_moyenne_generale.value = f"{mg:.2f}"
                if mg >= 16:
                    txt_mention.value = "Très bien"
                elif mg >= 14:
                    txt_mention.value = "Bien"
                elif mg >= 12:
                    txt_mention.value = "Assez bien"
                elif mg >= 10:
                    txt_mention.value = "Passable"
                else:
                    txt_mention.value = "Insuffisant"
            page.update()
        except Exception as e:
            print(f"Load error: {e}")

    def make_eleve_field(label, key, hint=""):
        tf = ft.TextField(
            label=label,
            hint_text=hint,
            **style_eleve,
            expand=True,
            on_change=lambda e: save_data(),
        )
        eleve_inputs[key] = tf
        return tf

    tf_nom = make_eleve_field("Nom", "nom")
    tf_prenom = make_eleve_field("Prénom", "prenom")
    tf_matricule = make_eleve_field("Matricule", "matricule")
    tf_classe = make_eleve_field("Classe", "classe", "Ex: Tle F3")
    tf_filiere = make_eleve_field("Filière", "filiere", "Ex: Electrotech")
    tf_annee = make_eleve_field("Année", "annee", "2025-2026")

    lbl_eleve = ft.Text("INFORMATIONS DE L'ÉLÈVE", size=10, weight=ft.FontWeight.BOLD, color=colors["text_secondary"])

    eleve_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PERSON_ROUNDED, size=14, color="blue400"),
                lbl_eleve,
            ], spacing=6),
            ft.Container(height=2),
            ft.Row([tf_nom, tf_prenom], spacing=10),
            ft.Row([tf_matricule, tf_classe], spacing=10),
            ft.Row([tf_filiere, tf_annee], spacing=10),
        ], spacing=10),
        padding=14,
        bgcolor=colors["card_bg"],
        border=ft.Border.all(1, colors["card_border"]),
        border_radius=14,
    )

    rows = []
    for idx, (nom, code, coef) in enumerate(MATIERES):
        inp_coef = ft.TextField(
            value=str(coef), width=44,
            on_change=lambda e, c=code: (
                coefs.update({c: float(e.control.value.replace(",", ".")) if e.control.value else 0}), 
                recalculer_et_mettre_a_jour()
            ),
            **style_coef
        )
        coefs_inputs[code] = inp_coef
        
        inputs_i = []
        for n in range(1, 5):
            inp = ft.TextField(
                width=42,
                on_change=lambda e: recalculer_et_mettre_a_jour(),
                **style_input_discret
            )
            notes_data[f"{code}_i{n}"] = inp
            inputs_i.append(inp)

        lbl_moy_i = ft.Text("—", size=12, weight=ft.FontWeight.BOLD, color=colors["pill_text"] if not is_dark else "white")
        notes_data[f"{code}_moy_i"] = lbl_moy_i
        moy_int_texts.append(lbl_moy_i)
        cont_moy_i = ft.Container(content=lbl_moy_i, bgcolor=colors["pill_bg_int"], padding=ft.Padding(left=8, right=8, top=5, bottom=5), border_radius=8, border=ft.Border.all(1, colors["pill_border"]))
        moy_int_containers.append(cont_moy_i)

        inputs_d = []
        for n in range(1, 4):
            inp = ft.TextField(
                width=42,
                on_change=lambda e: recalculer_et_mettre_a_jour(),
                **style_input_discret
            )
            notes_data[f"{code}_d{n}"] = inp
            inputs_d.append(inp)

        lbl_moy = ft.Text("—", size=13, weight=ft.FontWeight.BOLD, color="#2563eb" if not is_dark else "white")
        notes_data[f"{code}_moy"] = lbl_moy
        moy_texts.append(lbl_moy)
        cont_moy = ft.Container(content=lbl_moy, bgcolor=colors["pill_bg"], padding=ft.Padding(left=10, right=10, top=5, bottom=5), border_radius=8, border=ft.Border.all(1, colors["pill_border"]))
        moy_containers.append(cont_moy)

        lbl_mc = ft.Text("—", size=12, weight=ft.FontWeight.BOLD, color=colors["text_primary"])
        notes_data[f"{code}_mc"] = lbl_mc
        moy_coef_texts.append(lbl_mc)

        row_color = colors["row_even"] if idx % 2 == 0 else colors["row_odd"]

        cells = [
            ft.DataCell(inp_coef),
            ft.DataCell(ft.Text(nom, size=12, weight=ft.FontWeight.W_600, color=colors["text_primary"])),
            ft.DataCell(inputs_i[0]), ft.DataCell(inputs_i[1]), ft.DataCell(inputs_i[2]), ft.DataCell(inputs_i[3]),
            ft.DataCell(cont_moy_i),
            ft.DataCell(inputs_d[0]), ft.DataCell(inputs_d[1]), ft.DataCell(inputs_d[2]),
            ft.DataCell(cont_moy),
            ft.DataCell(lbl_mc),
        ]
        rows.append(ft.DataRow(cells=cells, color=row_color))

    lbl_table = ft.Text("RÉSULTATS PAR MATIÈRE", size=10, weight=ft.FontWeight.BOLD, color=colors["text_secondary"])

    data_table = ft.DataTable(
        heading_row_color=colors["table_header"],
        heading_row_height=46,
        data_row_min_height=52,
        data_row_max_height=58,
        divider_thickness=0.6,
        horizontal_margin=10,
        column_spacing=14,
        border=ft.Border.all(1, colors["table_border"]),
        border_radius=12,
        columns=[
            ft.DataColumn(ft.Text("Coef", size=10, weight=ft.FontWeight.BOLD, color="blue400")),
            ft.DataColumn(ft.Text("Matière", size=11, weight=ft.FontWeight.BOLD, color=colors["text_primary"])),
            ft.DataColumn(ft.Text("I1", size=10, weight=ft.FontWeight.BOLD, color=colors["text_muted"])),
            ft.DataColumn(ft.Text("I2", size=10, weight=ft.FontWeight.BOLD, color=colors["text_muted"])),
            ft.DataColumn(ft.Text("I3", size=10, weight=ft.FontWeight.BOLD, color=colors["text_muted"])),
            ft.DataColumn(ft.Text("I4", size=10, weight=ft.FontWeight.BOLD, color=colors["text_muted"])),
            ft.DataColumn(ft.Text("Moy Int", size=10, weight=ft.FontWeight.BOLD, color=colors["text_muted"])),
            ft.DataColumn(ft.Text("D1", size=10, weight=ft.FontWeight.BOLD, color=colors["text_secondary"])),
            ft.DataColumn(ft.Text("D2", size=10, weight=ft.FontWeight.BOLD, color=colors["text_secondary"])),
            ft.DataColumn(ft.Text("D3", size=10, weight=ft.FontWeight.BOLD, color=colors["text_secondary"])),
            ft.DataColumn(ft.Text("Moyenne", size=10, weight=ft.FontWeight.BOLD, color="blue400")),
            ft.DataColumn(ft.Text("Moy Coef", size=10, weight=ft.FontWeight.BOLD, color=colors["text_primary"])),
        ],
        rows=rows,
    )

    tableau_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.TABLE_CHART_ROUNDED, size=14, color="blue400"),
                lbl_table,
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text("Glissez ⇄", size=8, color=colors["text_muted"]),
                    bgcolor=colors["table_header"],
                    padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                    border_radius=10,
                )
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(height=1, color=colors["divider"]),
            ft.Row([data_table], scroll=ft.ScrollMode.AUTO),
        ], spacing=10),
        bgcolor=colors["table_bg"],
        border=ft.Border.all(1, colors["card_border"]),
        border_radius=14,
        padding=12,
    )

    page.add(
        ft.SafeArea(
            ft.Column([
                entete,
                ft.Divider(height=12, color="transparent"),
                eleve_card,
                ft.Divider(height=12, color="transparent"),
                tableau_container,
                ft.Divider(height=16, color="transparent"),
                ft.Row([btn_apropos], alignment=ft.MainAxisAlignment.CENTER)
            ], scroll=ft.ScrollMode.AUTO)
        )
    )

    load_data()
    apply_theme()

ft.app(main)
