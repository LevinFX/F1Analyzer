from analysis import loadLapData, avgLapTimes, lapTimeConsistency
from plot import plotRacePace


def main():
    laps = loadLapData()

    avgPace = avgLapTimes(laps)
    consistency = lapTimeConsistency(laps)

    print("Durchschnittliche Lapzeiten:")
    print(avgPace)

    print("Konstanz der Lapzeiten:")
    print(consistency)

    plotRacePace(laps)


if __name__ == "__main__":
    main()