
import re
import io
from datetime import datetime
from icalendar import Calendar

def auto_refactor(ical_object):
    results = {}
    current_summarys = distinct_summaries(ical_object)
    for summary in current_summarys:
        parts = sorted(filter(lambda part: bool(part), map(refactor, summary.split(","))), key=auditorium_last)
        results.update({summary: refactor(", ".join(parts).strip())})

    for key, value in results.items():
        for component in ical_object.walk(name="VEVENT"):
            if key == str(component["summary"]):
                component["summary"] = value

    return results

def refactor_file(ics_file):
    data = ics_file.read()
    ics_file.seek(0)
    ical_obj = Calendar.from_ical(data)
    results = auto_refactor(ical_obj)
    file_io = io.BytesIO(ical_obj.to_ical())
    file_io.seek(0)
    return file_io, results



def distinct_summaries(ical_object):
    summaries = set()
    for component in ical_object.walk(name="VEVENT"):
        summaries.add(str(component["summary"]))
    return summaries

def refactor(part):
    replacements = {
        # Targers cource code " / 28C00500 - "
        r" / .*? - ": " ",
        r"Otakaari 1": "",
        r"Kurssitentti/Course examination/Kurssitentti": "TENTTI",
        "Välikoe/Midterm exam/Mellanförhör": 'Välikoe',
        r"  ": r" ",
        r"[HML]\d{2}": r"",
        r"[^\sA-Öa-ö]*\.+\)": r"",
        r"\(\d[A-Z0-9]+": r"",
        r"^\([A-Z0-9-]+\)?": r"",
        "Pienryhmäopetus": "",
        "Small group teaching": "",
        "Pienryhmäopetus": "",
        "Monimuoto-opetus": "",
        "Multiform teaching": "",
        "Monimuoto-opetus": "",
        "Luento": "",
        "Lecture": "",
        "Föreläsning": "",
        "Harjoitukset": "",
        "Harjoitus": "",
        "Exercises": "",
        "Övningar": "",
        # Dates separated by [/.-]
        r"[0-9]{2}[/.-][0-9]{2}[/.-][0-9]{4}": "",
    }
    for find, replace in replacements.items():
        part = re.sub(find, replace, part)

    chars = ", -/"
    for _ in range(len(chars)*2):
        part = part.strip(chars)
    return part

def auditorium_last(part):
    auditorium_patterns = [
        r"^[A-Z]-Sali",
        r"^[UYA][0-9]",
    ]
    for pattern in auditorium_patterns:
        if re.findall(pattern, part):
            return 1
    return -1

    