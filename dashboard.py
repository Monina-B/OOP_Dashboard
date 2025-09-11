import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
from model import Datenzugriff, DashboardSteuerung

# --- Streamlit User Interface ---

st.set_page_config(layout="wide")
# Seitenlayout 

benutzer = {
    # Benutzerverwaltung
    "anna": {"passwort": "1234", "name": "Anna", "nachname": "Müller", "matrikelnummer": 123456},
    "max": {"passwort": "abcd", "name": "Max", "nachname": "Schmidt", "matrikelnummer": 654321}
}

if "eingeloggt" not in st.session_state:
    # speichert den Login-Status
    st.session_state["eingeloggt"] = False

if not st.session_state["eingeloggt"]:
    # Login-Formular anzeigen
    st.sidebar.header("Login")
    nutzername = st.sidebar.text_input("Benutzername")
    passwort = st.sidebar.text_input("Passwort", type="password")
    if st.sidebar.button("Einloggen"):
        # Überprüfen der Anmeldedaten
        if nutzername in benutzer and benutzer[nutzername]["passwort"] == passwort:
            # Erfolgreicher Login
            st.session_state["eingeloggt"] = True
            st.session_state["nutzer"] = benutzer[nutzername]
            st.experimental_rerun()  # Seite neu laden
        else:
            # Login fehlgeschlagen
            st.error("Login fehlgeschlagen.")
    st.stop()


if st.sidebar.button("Ausloggen"):
    # Logout
    st.session_state.clear()
    st.experimental_rerun()  # sofort zurück zum Login
    st.stop()


st.sidebar.markdown(f"Eingeloggt als: {st.session_state['nutzer']['name']}")
# Anzeigen des eingeloggten Nutzers

datenzugriff = Datenzugriff("data.json")
steuerung = DashboardSteuerung(datenzugriff)

student = steuerung.getStudent()
studiengang = steuerung.getStudiengang()
module = steuerung.getModule()

# Nutzerinformationen aus dem Login speichern 
student.vorname = st.session_state["nutzer"]["name"]
student.nachname = st.session_state["nutzer"]["nachname"]
student.matrikelnummer = st.session_state["nutzer"]["matrikelnummer"]

# Beispielhafte absolvierte Kompetenzen (aktuell statisch)
absolvierte_kompetenzen = ["Kompetenz 1", "Kompetenz 2", "Kompetenz 5"]

# Header mit Icon und Titel
col_icon, col_title = st.columns([1, 9])


with col_icon:
    # kleines Nutzer-Icon (externes Bild)
    st.markdown("""
        <div style="margin-top: 12px;">
            <img src="https://img.icons8.com/ios-filled/50/user.png" width="30"/>
        </div>
    """, unsafe_allow_html=True)

with col_title:
     # Titelzeile: Name des Studierenden + Studiengang
    st.markdown(
        f'<p style="font-size:28px; font-weight:600; margin-top:5px;">Dashboard von <i>{student.vorname} {student.nachname}</i> für <i>{studiengang.name}</i></p>',
        unsafe_allow_html=True
    )

col1, spacer, col2 = st.columns([3.5, 2.5, 4.5])
# Layout: linke Spalte mit Fortschritt und Seminaren

with col1:
    # Linke Spalte mit Fortschritt und Seminaren
    st.markdown("<h3 style='margin-bottom:0;'>Fortschritt <i>Semester</i></h3>", unsafe_allow_html=True)
    
    #Donut-Diagramm
    fig, ax = plt.subplots(figsize=(5, 5)) 
    size = 0.13 #Ringbreite

    # Aktuelles Semester ermitteln (aktuell fix auf 1. Semester gesetzt)
    semester_index = 0
    # Module des aktuellen Semesters filtern
    semester_module = [m for m in module if m.semester_index == semester_index]
    
    # Äußerer Ring: "Platzhalter" – jedes Modul bekommt 1 Segment
    outer_values = [1] * len(semester_module) 

    # Innere Segmente: 1 für absolviertes Modul, sonst 0
    inner_values = [1] * len(semester_module) # if m.note is not None else 0 for m in semester_module]

    # Farben für den äußeren Ring (blaue)
    outer_colors = plt.cm.Blues(np.linspace(0.5, 0.9, len(outer_values)))

    # Farben für den inneren Ring (blau für absolviert, grau für offen)
    inner_colors = [
            plt.cm.Blues(0.4) if m.note is not None else "#e0e0e0"  # (r,g,b,alpha)
            for m in semester_module
    ]

    # Innerer Ring (zuerst zeichnen)
    ax.pie(outer_values, radius=1 - size, colors=outer_colors,
           wedgeprops=dict(width=size, edgecolor='w')) 
    

    # Äußerer Ring (drauflegen)
    ax.pie(inner_values, radius=1, colors=inner_colors,
           wedgeprops=dict(width=size, edgecolor='w'))


    ax.set(aspect="equal")
    st.pyplot(fig)

    
    # ---- Legende als Zeile unter dem Diagramm ----
    with st.container():
        # Anlage der Spalten: 2 Spalten für Legende (Hälfte 1, Hälfte 2), 1 Spacer rechts
        spacer1, leg_col1, leg_col2, spacer2 = st.columns([2, 2, 2, 1])

        gruppe1 = semester_module[:3]
        gruppe2 = semester_module[3:]

        with leg_col1:
            # Hälfte 1 der Module
            for modul in gruppe1:
                color = matplotlib.colors.to_hex(outer_colors[semester_module.index(modul)])
                st.markdown(
                    f"<div style='color:{color}; font-weight:bold; font-size:0.9em; padding:2px 0;'>{modul.name}</div>",
                    unsafe_allow_html=True
                )

        with leg_col2:
            # Hälfte 2 der Module
            for modul in gruppe2:
                color = matplotlib.colors.to_hex(outer_colors[semester_module.index(modul)])
                st.markdown(
                    f"<div style='color:{color}; font-weight:bold; font-size:0.9em; padding:2px 0;'>{modul.name}</div>",
                    unsafe_allow_html=True
                )

with col2:
    # Rechte Spalte mit Kompetenzen (Checkboxen)
    st.markdown(
        "<h3 style='margin-bottom: 90px;'>Kompetenzen <i>Semester</i></h3>",
        unsafe_allow_html=True
    )

# 7 Kompetenzen aktuell hart kodiert und gegen Liste geprüft
    for i in range(1, 8):
        key = f"Kompetenz {i}"
        checked = key in absolvierte_kompetenzen
        symbol = "✅" if checked else "⬜️"
        st.markdown(
            f"<div style='font-size:1.7em; padding:4px 0;'>{symbol} <strong>{key}</strong></div>",
            unsafe_allow_html=True
        )


# Untere Abschnitt mit Balkendiagramm und Notenschnitt
st.markdown("---")
st.markdown("#### *Studienfortschritt*")

col3, col4 = st.columns([4, 1])

# Balkendiagramm und Notenschnitt
with col3:
    schnitt = studiengang.get_notenschnitt()
    schnitt_text = f"Aktueller Notenschnitt: {schnitt:.2f}" if schnitt else "Notenschnitt: –"
    st.markdown(f"""
        <div style='display:inline-block;padding:6px 18px;background-color:#457b9d;border-radius:25px;margin-right:10px;color:white;font-weight:bold;'>
            {schnitt_text}
        </div>
    """, unsafe_allow_html=True)
    st.progress(student.get_aktueller_fortschritt() / studiengang.get_ects_gesamt())
    # Balkendiagramm mit ECTS-Fortschritt (ECTS erreicht / gesamt)

with col4:
    # Icon für Abschluss
    st.markdown("""
        <div style='text-align:center; font-size:38px; line-height:1.2'>
            🎓<br><span style='font-size:18px;'><strong>Abschluss</strong></span>
        </div>
    """, unsafe_allow_html=True)
