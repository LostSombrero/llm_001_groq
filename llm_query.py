import os
import requests
import re
from webscrape_imprint import run_scraper
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

def get_data_for_csv(target_url):
    print(f"🚀 Starte Verarbeitung für: {target_url}")

    try:
        print("🔍 Starte Scraper...")
        llm_text_input, html_url = run_scraper(target_url)

        if not llm_text_input:
            print("⚠️ Kein Impressumstext gefunden.")
            return "Kein Impressum gefunden"

        print("✅ Impressumstext gefunden – Länge:", len(llm_text_input), "Zeichen")
        print("📄 Textvorschau:\n", llm_text_input[:500], "...\n")

        extracted_data = """
        Unternehmensname:
        Geschäftsführer:
        E-Mail-Adresse:
        Telefonnummer:
        Straße und Hausnummer:
        PLZ:
        Ort:
        Land:
        HRB-Nummer:
        UStID-Nummer:
        Website:
        """

        prompt_template = (
            "Du bist ein hochqualifizierter Experte für Datenextraktion und Textanalyse. "
            "Deine Aufgabe ist es, aus Impressums-Texten strukturierte, geschäftsrelevante Kontaktdaten zu extrahieren.\n\n"
            "Bitte extrahiere die folgenden Informationen:\n"
            "{extracted_data}\n\n"
            "Der folgende Text wurde von einer Impressumsseite extrahiert:\n\n"
            "{llm_text_input}\n\n"
            "Ignoriere Postanschriften, Niederlassungen oder Versandadressen."
            "Gib nur die Hauptanschrift/zentrale Anschrift an."
            "Achte besonders auf Geschäftsführer, physische Adresse und Kontaktinformationen. "
            "Gib Straße und Hausnummer, Postleitzahl, Ort und Land jeweils separat an. "
            "Gib keine E-Mail-Adresse oder Telefonnummer bei diesen Feldern an. "
            "Wenn etwas nicht vorhanden ist, gib 'N/A' zurück.\n\n"
            "Gib die Daten ausschließlich im folgenden Format zurück:\n{extracted_data}\n"
            "Keine Erklärungen oder Kommentare."
        )

        prompt = prompt_template.format(
            llm_text_input=llm_text_input,
            extracted_data=extracted_data
        )

        print("💬 Sende Prompt an Groq...")
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()

        result = response.json()["choices"][0]["message"]["content"]
        clean_output = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)

        print("✅ Antwort erhalten von Groq")
        print("📦 Extraktion abgeschlossen.\n")
        return clean_output.strip()

    except Exception as e:
        print(f"❌ Fehler bei {target_url}")
        print("🛠️ Fehlerdetails:", e)
        return "Fehler bei Verarbeitung"