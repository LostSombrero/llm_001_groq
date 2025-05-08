# 🕸️ Domain-Impressum Extractor (Groq API Version)

Dieses Projekt dient der automatisierten Extraktion von Impressumsdaten aus einer Liste von Webseiten.  
Die Analyse erfolgt über ein Language Model, das in dieser Version über die **Groq API** angebunden ist.

---

## 📦 Projektübersicht

Das Projekt besteht aus drei Hauptkomponenten:

1. **`run_batch_domains.py`** – Batch-Controller zum Einlesen und Starten der Verarbeitung
2. **`main_script.py`** – Einzelverarbeitung einer URL inkl. Ergebnis-Speicherung
3. **`llm_query.py`** – Kommunikation mit dem LLM zur strukturierten Datenausgabe

---

## 📁 Projektstruktur

```
llm_001/
├── input/
│ └── urls.csv		        # CSV-Datei mit den Ziel-URLs
├── output/
│ └── impressum_analyse.csv	# Ergebnisdatei der Datenextraktion
├── main_script.py		# Einzelverarbeitung
├── run_batch_domains.py	# Batch-Verarbeitung
├── llm_query.py		# LLM-Logik für Datenanalyse (Groq API)
├── webscrape_imprint.py	# Web-Scraping Modul
├── .env			# API-Key und Modellkonfiguration
└── README.md			# Diese Datei
```

---

## 🧰 Voraussetzungen

- Python 3.6 oder höher
- Terminal mit UTF-8-Unterstützung
- API-Key und Modellname für [Groq Playground](https://console.groq.com/)

---

## 🔧 Konfiguration (.env)

Beispiel:

GROQ_API_KEY=sk-abc123deinrichtigerkey456
GROQ_MODEL=deepseek-r1-distill-llama-70b

---

## ⚙️ Setup und Ausführung (Guide)

### 1. Ursprünglichen Guide folgen (außer Ollama).
### 2. `pip install python-dotenv`
### 3. [Groq Playground](https://console.groq.com/home) öffnen
### 4. Einloggen oder Account erstellen
### 5. API-Key erstellen ([groq.com/keys](https://console.groq.com/keys))
### 6. `.env` mit Key und Modell befüllen
### 7. Ausführung:

```bash
python run_batch_domains.py
```

oder für eine einzelne URL:
```
python main_script.py https://example.com
```

---

## 🔁 Ablaufbeschreibung

### 1. 🔁 run_batch_domains.py

Startet die Batch-Verarbeitung für mehrere URLs aus input/urls.csv.

### 2. 🧠 main_script.py

Verarbeitet eine einzelne Domain, analysiert die LLM-Antwort und schreibt das Ergebnis in output/impressum_analyse.csv.

### 3. 🤖 llm_query.py

Kommuniziert mit Groq API, generiert den Prompt und erwartet die Antwort in folgender Struktur:

```
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
```

**Hinweis:** Fehlt eine Information, wird "N/A" zurückgegeben.

---

## 📥 Eingabeformat

Die Datei input/urls.csv muss wie folgt aufgebaut sein:

```csv
Target URL
https://example.com
https://another-example.org
```

---

## 🧪 Ausgabeformat

Beispielausgabe in output/impressum_analyse_debug.csv:

```csv
Unternehmensname,Geschäftsführer,E-Mail-Adresse,Telefonnummer,Straße und Hausnummer,PLZ,Ort,Land,HRB-Nummer,UStID-Nummer,Website
Example GmbH,Max Mustermann,info@example.com,+49 123 4567,Musterstraße 1,12345,Musterstadt,Deutschland,HRB 12345,DE123456789,https://example.com
```

---

## 💡 Hinweise

- Die Nutzung von Groq Playground ist zum Stand 2025-05-05 kostenlos.
- Modell-Limits: z. B. deepseek-r1-distill-llama-70b = 30/min, 1000/Tag
	→ realistisch: 1000 Impressen pro Tag.
- .env-Datei muss existieren mit gültigem API-Key und Modell.

---

## 🐞 Fehlerbehandlung

- Fehlende URL → Hinweis in der Konsole
- Kein Impressum gefunden → "Kein Impressum gefunden"
- Fehlermeldung (z. B. Encoding) → Logging mit URL

---

## 🧾 Changelog

[0.2] – 2025-05-05

- Migration von lokalem LLM zu Groq Playground
- .env hinzugefügt (API Key + Modell)
- llm_query.py überarbeitet
- Bugfix: „Adresse“ wurde oft mit E-Mail-Adressen verwechselt → jetzt unterteilt:
	- Straße und Hausnummer
	- PLZ
	- Ort
	- Land
- Prompt verändert
- requirements.txt: ollama entfernt
- Neue Impressumspfade ergänzt:
	/impressum/
	/index.php/impressum/
- run_batch_domains.py: Fix für UTF-8-Fehler mit encoding='utf-8'

---

## 📅 Geplant (Planned)

[0.3 – 1.0]

- Einträge wie /index.php/impressum/ verschlechtern die Extraktion auf bestimmten Seiten

Beispiel:
	- negativ: https://www.pro-energy-solutions.de/
	- positiv: https://probatum-sun.de/

---

## 📜 Lizenz

Dieses Projekt steht unter der MIT License.
Du darfst den Code frei verwenden, verändern und weiterverbreiten – mit Angabe des Urhebers.
