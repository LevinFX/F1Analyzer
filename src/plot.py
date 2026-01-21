import matplotlib.pyplot as plt
from analysis import DRIVERS, RACE, SEASON, SESSION_TYPE
from pandas import DataFrame

output_DIR: str = "output"

def plotRacePace(laps: DataFrame) -> None:
    """Plottet die Rennzeiten der Fahrer"""
    plt.figure(figsize=(10, 6))

    for driver in DRIVERS:
        driver_laps = laps[laps["Driver"] == driver]
        lap_times_seconds = driver_laps["LapTime"].dt.total_seconds()
        plt.plot(
            driver_laps["LapNumber"],
            lap_times_seconds,
            label=driver
        )

    plt.xlabel("Runde")
    plt.ylabel("Rundenzeit (s)")
    plt.title(f"{RACE} {SEASON} {SESSION_TYPE}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_DIR}/lap_times.png")
    plt.close()

    print(f"Plot gespeichert in {output_DIR}/lap_times.png")
    return