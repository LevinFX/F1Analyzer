import fastf1 as f1
import pandas as pd
from pandas import DataFrame

#KONFIGURATION
SEASON: int = 2025
RACE: str = "Qatar"
SESSION_TYPE: str = "R"
DRIVERS: list[str] = ["VER", "LEC"]#, "LEC", "NOR", "HUL"]

CACHE_DIR: str = "cache"
f1.Cache.enable_cache(CACHE_DIR)

def loadLapData() -> DataFrame:
    """Lädt die Lapzeiten für die ausgewählten Fahrer"""
    race = f1.get_session(SEASON, RACE, SESSION_TYPE)
    race.load()
    return race.laps.pick_drivers(DRIVERS)

def avgLapTimes(laps: DataFrame) -> DataFrame:
    """Berechnet den Durchschnitt der Lapzeiten der Fahrer"""
    return(
        laps
        .groupby("Driver")["LapTime"]
        .mean()
        .sort_values()
        .reset_index()
    )

def lapTimeConsistency(laps: DataFrame) -> DataFrame:
    """Berechnet die Konstanz der Lapzeiten der Fahrer"""
    return(
        laps
        .groupby("Driver")["LapTime"]
        .std()
        .reset_index()
        .rename(columns={"LapTime": "LapTimeStd"})
    )