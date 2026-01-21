import fastf1 as f1
from pandas import DataFrame


class F1Session:
    """Klasse zur Verwaltung von F1-Session-Daten"""
    
    CACHE_DIR: str = "cache"
    
    def __init__(self, season: int, race: str, sessionType: str, drivers: list[str] = None):
        """
        Initialisiert eine F1-Session
        
        Args:
            season: Die Saison (z.B. 2025)
            race: Der Rennname (z.B. "Qatar")
            sessionType: Der Session-Typ (z.B. "R" für Race)
            drivers: Liste der Fahrer-Abkürzungen (z.B. ["VER", "LEC"])
        """

        self.season = season
        self.race = race
        self.sessionType = sessionType
        self.drivers = drivers or []
        self._session = None
        self._laps = None
        self._tyreChanges = None
        
        f1.Cache.enable_cache(self.CACHE_DIR)
    
    def load(self) -> None:
        """Lädt die Session-Daten"""
        
        self._session = f1.get_session(self.season, self.race, self.sessionType)
        self._session.load()
    
    @property
    def session(self) -> f1.core.Session:
        """Gibt die geladene Session zurück"""

        if self._session is None:
            self.load()
        return self._session
    
    def getLaps(self, drivers: list[str] = None) -> DataFrame:
        """Lädt die Lapzeiten für die ausgewählten Fahrer"""

        if self._laps is None or drivers is not None:
            selectedDrivers = drivers or self.drivers
            self._laps = self.session.laps.pick_drivers(selectedDrivers)
        return self._laps

    def getTyreChanges(self, drivers: list[str] = None)  -> DataFrame:
        """Lädt die Reifenwechsel für die ausgewählten Fahrer"""

        if self._tyreChanges is None or drivers is not None:
            if self._laps is None: self.getLaps()

            stints = self._laps[["Driver", "Stint", "Compound", "LapNumber"]]
            stints = stints.groupby(["Driver", "Stint", "Compound"])
            stints = stints.count().reset_index()
            stints = stints.rename(columns={"LapNumber": "StintLength"})

            self._tyreChanges = stints
        return self._tyreChanges

    def getAllDrivers(self) -> DataFrame:
        """Zeigt alle Fahrer mit Nummer, Name, Kürzel und Team an"""
        session = self.session
        results = session.results
        
        driversDf = results[[
            "DriverNumber",
            "Abbreviation", 
            "FullName",
            "TeamName"
        ]].copy()
        
        driversDf = driversDf.rename(columns={
            "DriverNumber": "Nummer",
            "Abbreviation": "Kürzel",
            "FullName": "Name",
            "TeamName": "Team"
        })
        
        driversDf = driversDf.sort_values("Nummer").reset_index(drop=True)
        
        return driversDf
    
    def __str__(self) -> str:
        """String-Repräsentation der Session"""
        return f"{self.race} {self.season} {self.sessionType}"


class F1Analyzer:
    """Klasse zur Analyse von F1-Lap-Daten"""
    
    def __init__(self, laps: DataFrame):
        """Initialisiert den Analyzer mit Lap-Daten"""

        self.laps = laps
    
    def avgLapTimes(self) -> DataFrame:
        """Berechnet den Durchschnitt der Lapzeiten der Fahrer"""

        return (
            self.laps
            .groupby("Driver")["LapTime"]
            .mean()
            .sort_values()
            .reset_index()
        )
    
    def lapTimeConsistency(self) -> DataFrame:
        """Berechnet die Konstanz der Lapzeiten der Fahrer"""

        return (
            self.laps
            .groupby("Driver")["LapTime"]
            .std()
            .reset_index()
            .rename(columns={"LapTime": "LapTimeStd"})
        )
    
    def analyzeTyreStrategy(self, tyreChanges: DataFrame) -> DataFrame:
        """Analysiert die Reifenstrategie der Fahrer"""
        
        strategy = (
            tyreChanges
            .groupby("Driver")
            .agg({
                "Stint": "count",
                "StintLength": "mean",
                "Compound": lambda x: ", ".join(x.unique())
            })
            .reset_index()
            .rename(columns={
                "Stint": "NumberOfStints",
                "StintLength": "AvgStintLength",
                "Compound": "CompoundsUsed"
            })
        )
        
        # Anzahl der Stopps = Anzahl der Stints - 1
        strategy["NumberOfPitStops"] = strategy["NumberOfStints"] - 1
        
        return strategy
    
    def compareWithWinner(self, session: f1.core.Session, tyreChanges: DataFrame, selectedDrivers: list[str]) -> DataFrame:
        """
        Vergleicht die ausgewählten Fahrer mit dem Renngewinner
        
        Args:
            session: Die F1-Session
            tyreChanges: DataFrame mit Reifenwechsel-Daten
            selectedDrivers: Liste der zu vergleichenden Fahrer
        
        Returns:
            DataFrame mit Vergleichsdaten
        
        Methode teils mithilfe von Claude geschrieben.
        """
        # Gewinner identifizieren (Position 1)
        results = session.results
        winner = results.loc[results["Position"] == 1, "Abbreviation"].iloc[0]
        
        # Gewinner-Daten laden
        winnerLaps = session.laps.pick_drivers(winner)
        
        # Gewinner TyreChanges berechnen falls nicht vorhanden
        if winner in tyreChanges["Driver"].values:
            winnerTyreChanges = tyreChanges[tyreChanges["Driver"] == winner]
        else:
            # Gewinner TyreChanges separat berechnen
            winnerLapsData = winnerLaps[["Driver", "Stint", "Compound", "LapNumber"]]
            winnerStints = winnerLapsData.groupby(["Driver", "Stint", "Compound"])
            winnerStints = winnerStints.count().reset_index()
            winnerStints = winnerStints.rename(columns={"LapNumber": "StintLength"})
            winnerTyreChanges = winnerStints
        
        # Vergleichsdaten für ausgewählte Fahrer sammeln
        comparisonData = []
        
        # Gewinner-Daten hinzufügen
        if len(winnerLaps) > 0 and len(winnerTyreChanges) > 0:
            winnerAvgPace = winnerLaps["LapTime"].mean().total_seconds()
            winnerAvgStintLength = winnerTyreChanges["StintLength"].mean()
            winnerCompounds = ", ".join(winnerTyreChanges["Compound"].unique())
            winnerPitStops = len(winnerTyreChanges) - 1
            
            comparisonData.append({
                "Driver": winner,
                "IsWinner": True,
                "AvgPaceSeconds": winnerAvgPace,
                "AvgStintLength": winnerAvgStintLength,
                "CompoundsUsed": winnerCompounds,
                "NumberOfPitStops": winnerPitStops
            })
        
        # Ausgewählte Fahrer-Daten hinzufügen
        for driver in selectedDrivers:
            if driver == winner:
                continue  # Gewinner bereits hinzugefügt
            
            driverLaps = self.laps[self.laps["Driver"] == driver]
            driverTyreChanges = tyreChanges[tyreChanges["Driver"] == driver]
            
            if len(driverLaps) > 0 and len(driverTyreChanges) > 0:
                driverAvgPace = driverLaps["LapTime"].mean().total_seconds()
                driverAvgStintLength = driverTyreChanges["StintLength"].mean()
                driverCompounds = ", ".join(driverTyreChanges["Compound"].unique())
                driverPitStops = len(driverTyreChanges) - 1
                
                # Unterschiede zum Gewinner berechnen
                winnerAvgPace = winnerLaps["LapTime"].mean().total_seconds() if len(winnerLaps) > 0 else None
                winnerAvgStintLength = winnerTyreChanges["StintLength"].mean() if len(winnerTyreChanges) > 0 else None
                
                paceDiff = driverAvgPace - winnerAvgPace if winnerAvgPace is not None else None
                stintDiff = driverAvgStintLength - winnerAvgStintLength if winnerAvgStintLength is not None else None
                
                comparisonData.append({
                    "Driver": driver,
                    "IsWinner": False,
                    "AvgPaceSeconds": driverAvgPace,
                    "AvgStintLength": driverAvgStintLength,
                    "CompoundsUsed": driverCompounds,
                    "NumberOfPitStops": driverPitStops,
                    "PaceDiffToWinner": paceDiff,
                    "StintLengthDiffToWinner": stintDiff
                })
        
        comparisonDf = DataFrame(comparisonData)
        
        # Sortieren: Gewinner zuerst, dann nach Pace
        if len(comparisonDf) > 0:
            comparisonDf = comparisonDf.sort_values(
                by=["IsWinner", "AvgPaceSeconds"],
                ascending=[False, True]
            ).reset_index(drop=True)
        
        return comparisonDf
