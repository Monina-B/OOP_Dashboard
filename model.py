from datetime import date
import json 

class Prüfungsleistung:
    """Repräsentiert eine Prüfungsleistung in einem Modul."""
    def __init__(self, note: float, modul: str, prüfungsform: str):
        #   Initialisiert eine Prüfungsleistung mit Note, Modul und Prüfungsform.
        self.note = note
        self.modul = modul
        self.prüfungsform = prüfungsform

    def set_note(self, note: float):
        #  Setzt die Note der Prüfungsleistung.
        self.note = note


class Modul:
    """Repräsentiert ein Modul im Studiengang."""
    def __init__(self, name: str, ects: int, dozent: str, erwerbbare_kompetenzen: list[str], note: float = None, semester_index: int = 0):
        # Initialisiert ein Modul mit Name, ECTS, Dozent, Kompetenzen, Note und Semesterindex.
        self.name = name
        self.ects = ects
        self.dozent = dozent
        self.erwerbbare_kompetenzen = erwerbbare_kompetenzen
        self.note = note
        self.semester_index = semester_index
    def set_name(self, name: str):
        # Setzt den Namen des Moduls.
        self.name = name
    def set_ects(self, ects: int):
        # Setzt die ECTS-Punkte des Moduls.
        self.ects = ects
    def set_kompetenzen(self, kompetenzen: list[str]):
        # Setzt die Liste der erwerbbaren Kompetenzen für das Modul.
        self.erwerbbare_kompetenzen = kompetenzen


class Semester:
    """Repräsentiert ein Semester im Studiengang."""
    def __init__(self, art: str, beginn: date, dauer_monate: int, module: list[Modul]):
        # Initialisiert ein Semester mit Art, Beginn, Dauer und Modulen.
        self.art = art
        self.beginn = beginn
        self.dauer_monate = dauer_monate
        self.module = module


class Abschluss:
    """Repräsentiert einen Studienabschluss."""
    def __init__(self, form: str, benötigte_ects: int, note: float):
        # Initialisiert einen Abschluss mit Form, benötigten ECTS und Note.
        self.form = form
        self.benötigte_ects = benötigte_ects
        self.note = note

    def get_notenschnitt(self):
        # Gibt die Note des Abschlusses zurück.
        return self.note

    def set_benötigte_ects(self, ects: int):
        # Setzt die benötigten ECTS für den Abschluss.
        self.benötigte_ects = ects


class Studiengang:
    """Repräsentiert einen Studiengang."""
    def __init__(self, name: str, regelabschluss: str, ects: int, modul_liste: list[Modul], regelsemesteranzahl: int):
        # Initialisiert einen Studiengang mit Name, Regelabschluss, ECTS, Modulliste und Regelsemesteranzahl.
        self.name = name
        self.regelabschluss = regelabschluss
        self.ects = ects
        self.modul_liste = modul_liste
        self.regelsemesteranzahl = regelsemesteranzahl

    def get_ects_gesamt(self):
        # Gibt die Gesamtanzahl der ECTS für den Studiengang zurück.
        return self.ects

    def get_ects_aktuell(self):
        # Gibt die Summe der ECTS aller Module zurück
        return sum(modul.ects for modul in self.modul_liste)

    def get_kompetenzen_gesamt(self):
        # Sammelt alle Kompetenzen aus allen Modulen in einer Liste
        return [k for modul in self.modul_liste for k in modul.erwerbbare_kompetenzen]

    def get_kompetenzen_aktuell(self, absolvierte_kompetenzen):
        # Gibt die Liste der aktuell erworbenen Kompetenzen zurück
        return [k for k in self.get_kompetenzen_gesamt() if k in absolvierte_kompetenzen]
    
    def get_notenschnitt(self):
        # Berechnet und gibt den Notenschnitt aller Module mit Note zurück
        noten = [m.note for m in self.modul_liste if m.note is not None]
        return round(sum(noten) / len(noten), 2) if noten else None
 

class Student:
    """Repräsentiert einen Studenten."""
    def __init__(self, nachname: str, vorname: str, matrikelnummer: int, studiengang: Studiengang):
        # Initialisiert einen Studenten mit Nachname, Vorname, Matrikelnummer und Studiengang
        self.nachname = nachname
        self.vorname = vorname
        self.matrikelnummer = matrikelnummer
        self.studiengang = studiengang

    def get_aktueller_fortschritt(self):
        # Gibt die aktuell erworbenen ECTS zurück
        return self.studiengang.get_ects_aktuell()
    

class Datenzugriff:
    """Verwaltet das Laden und Speichern von Moduldaten."""
    def __init__(self, dateiname="data.json"):
        # Initialisiert den Datenzugriff mit dem Dateinamen für die JSON-Datei
        self.dateiname = dateiname

    def load_module_list(self) -> list[Modul]:
        # Lädt die Modulliste aus einer JSON-Datei
        try:
            with open(self.dateiname, "r") as f:
                data = json.load(f)
            return [self.modul_from_dict(entry) for entry in data]
        except FileNotFoundError:
            # Falls die Datei nicht existiert, gib eine leere Modulliste zurück
            return []

    def save_module_list(self, module: list[Modul]):
        # Speichert die Modulliste in einer JSON-Datei
        with open(self.dateiname, "w") as f:
            json.dump([self.modul_to_dict(m) for m in module], f, indent=2)

    def modul_to_dict(self, modul: Modul) -> dict:
        # Konvertiert ein Modul-Objekt in ein Dictionary für die JSON-Speicherung
        return {
            "name": modul.name,
            "ects": modul.ects,
            "dozent": modul.dozent,
            "erwerbbare_kompetenzen": modul.erwerbbare_kompetenzen,
            "note": modul.note,
            "semester_index": modul.semester_index
        }

    def modul_from_dict(self, data: dict) -> Modul:
        # Erstellt ein Modul-Objekt aus einem Dictionary
        return Modul(
            name=data["name"],
            ects=data["ects"],
            dozent=data["dozent"],
            erwerbbare_kompetenzen=data.get("erwerbbare_kompetenzen", []),
            note=data.get("note"),
            semester_index=data.get("semester_index", 0)
        )

class DashboardSteuerung:
    """Steuert die Interaktion zwischen Datenzugriff und Dashboard."""
    def __init__(self, datenzugriff: Datenzugriff):
        # Initialisiert die Steuerung mit einem Datenzugriffsobjekt und lädt die Daten
        self.datenzugriff = datenzugriff
        self.module = self.datenzugriff.load_module_list()
        self.studiengang = Studiengang("Med. Informatik", "Bachelor", 180, self.module, 6)
        self.student = Student("Müller", "Anna", 123456, self.studiengang)

    def getStudent(self) -> Student:
        # Gibt das Student-Objekt zurück
        return self.student

    def getStudiengang(self) -> Studiengang:
        # Gibt das Studiengang-Objekt zurück
        return self.studiengang

    def getModule(self) -> list[Modul]:
        # Gibt die Liste der Module zurück
        return self.module
