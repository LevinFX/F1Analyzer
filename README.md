# F1 AI Race Analysis

Ein Python-basiertes Analyse-Tool für Formel-1-Renndaten, das Rennverläufe analysiert, visualisiert und mithilfe von KI automatisch interpretiert.

## 🏎️ Features

- **Datenanalyse**
  - Durchschnittliche Rennpace pro Fahrer
  - Konstanz der Lapzeiten (Standardabweichung)
  - Reifenstrategie-Analyse (Stints, Compounds, Boxenstopps)
  - Vergleich ausgewählter Fahrer mit dem Renngewinner

- **Visualisierung**
  - Race Pace Plots (Lap-Zeiten über Runden)
  - Reifenstrategie-Diagramme (Stint-Verlauf pro Fahrer)

- **KI-gestützte Zusammenfassung**
  - Automatische Interpretation der Analyseergebnisse
  - Technische Erklärungen im Stil eines F1-Renningenieurs
  - Markdown-Formatierte Ausgabe

## 🛠️ Technologien

- **Python** - Programmiersprache
- **fastf1** - F1-Daten-API
- **pandas** - Datenanalyse und -manipulation
- **matplotlib** - Visualisierung
- **ollama** - Lokale KI-Modelle für Zusammenfassungen

## 📦 Installation

1. Repository klonen:
```bash
git clone https://github.com/LevinFX/F1Analyzer.git
cd F1Analyzer
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Ollama installieren und Modell herunterladen:
```bash
# Ollama installieren von https://ollama.com
ollama pull dolphin3:latest  # oder ein anderes Modell
```

## 🚀 Verwendung

### Konfiguration

Öffne `src/main.py` und passe die Konfiguration an:

```python
# KONFIGURATION
SEASON: int = 2025
RACE: str = "Abu Dhabi"  # Rennname
SESSION_TYPE: str = "Race"  # "Race", "Qualifying", "FP1", etc.
DRIVERS: list[str] = ["NOR", "VER", "LEC"]  # Fahrer-Abkürzungen
AI_MODEL: str = "dolphin3:latest"  # Ollama-Modell
```

### Ausführung

```bash
python src/main.py
```

Das Skript:
1. Lädt die F1-Session-Daten
2. Führt Analysen durch
3. Erstellt Visualisierungen (gespeichert in `output/`)
4. Generiert eine KI-Zusammenfassung (gespeichert in `output/summary.md`)

## 📁 Projektstruktur

```
F1Analysis/
├── src/
│   ├── main.py          # Hauptprogramm
│   ├── analysis.py      # F1Session & F1Analyzer Klassen
│   ├── plot.py          # Visualisierungsfunktionen
│   └── summary.py       # KI-Zusammenfassung
├── output/              # Generierte Plots und Zusammenfassungen
├── cache/               # FastF1 Cache
├── requirements.txt     # Python-Abhängigkeiten
└── README.md
```

## 📊 Klassen-Übersicht

### F1Session
Verwaltet F1-Session-Daten:
- `load()` - Lädt Session-Daten
- `getLaps()` - Lädt Lap-Zeiten
- `getTyreChanges()` - Lädt Reifenwechsel-Daten
- `getAllDrivers()` - Liste aller Fahrer

### F1Analyzer
Führt Analysen auf Lap-Daten durch:
- `avgLapTimes()` - Durchschnittliche Lap-Zeiten
- `lapTimeConsistency()` - Konstanz der Lap-Zeiten
- `analyzeTyreStrategy()` - Reifenstrategie-Analyse
- `compareWithWinner()` - Vergleich mit Renngewinner

### AISummary
Generiert KI-gestützte Zusammenfassungen:
- `generatePrompt()` - Erstellt Prompt aus Analysedaten
- `summarizeStrategy()` - Generiert Zusammenfassung

## 📈 Beispiel-Ausgabe

Das Tool generiert:
- **Konsolen-Output**: Tabellarische Analysen
- **Plots**: `output/race_pace.png`, `output/tyre_strategy.png`
- **Zusammenfassung**: `output/summary.md`

## 🎯 Lernziele

- Arbeiten mit realen F1-Daten
- Datenanalyse & Visualisierung
- Objektorientierte Programmierung
- Einsatz von KI zur Ergebnisinterpretation
- API-Integration (FastF1)

## ⛏️ Verbesserungsmöglichkeiten
- Anderes LLM-Modell benutzten
- Prompt genauer abstimmen
- Mehr Datenpunkte der API anknüpfen

## 📝 Hinweise

- Beim ersten Lauf werden Daten von der FastF1-API geladen und gecacht
- Stelle sicher, dass Ollama läuft und das konfigurierte Modell verfügbar ist
- Session-Typen: "Race", "Qualifying", "FP1", "FP2", "FP3", "Sprint", "Sprint Shootout"

## 📄 Lizenz

MIT
