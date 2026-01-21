from analysis import F1Session, F1Analyzer
from plot import PlotTyreStrategy, plotRacePace
from summary import *

#--------------------------------------------------------------------
# KONFIGURATION                                                     #
SEASON: int = 2025                                                  #
RACE: str = "Abu Dhabi"  # Rennname                                 #
SESSION_TYPE: str = "Race"  # "Race", "Qualifying", "FP1", etc.     #
DRIVERS: list[str] = ["NOR", "VER", "LEC"]  # Fahrer-Abkürzungen    #
AI_MODEL: str = "dolphin3:latest"  # Ollama-Modell                  #
#--------------------------------------------------------------------


def main():
    # Session erstellen und laden
    session = F1Session(SEASON, RACE, SESSION_TYPE, DRIVERS)
    session.load()
    
    # Lap-Daten laden
    laps = session.getLaps()
    
    # Tyre-Daten laden
    tyres = session.getTyreChanges()
    
    # Analyse durchführen
    analyzer = F1Analyzer(laps)
    avgPace = analyzer.avgLapTimes()
    consistency = analyzer.lapTimeConsistency()
    tyreStrategy = analyzer.analyzeTyreStrategy(tyres)
    comparison = analyzer.compareWithWinner(session.session, tyres, DRIVERS)
    allDrivers = session.getAllDrivers()


    # KI Prompt erstellen
    summarizer = AISummary(AI_MODEL, avgPace, consistency, tyreStrategy, comparison, allDrivers)
    summarizer.generatePrompt()

    # Ergebnisse ausgeben
    print("Durchschnittliche Lapzeiten:")
    print(avgPace)
    
    print("\nKonstanz der Lapzeiten:")
    print(consistency)

    print("\nReifenstrategie:")
    print(tyreStrategy)
    
    print("\nVergleich mit Gewinner:")
    print(comparison)

    # Plot erstellen
    plotRacePace(session)
    PlotTyreStrategy(session)

    # Summary erstellen
    summary = summarizer.summarizeStrategy()
    print("\nKI Erklärung:")
    print(summary)


if __name__ == "__main__":
    main()
