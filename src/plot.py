import matplotlib.pyplot as plt
import fastf1.plotting as plotting
import fastf1 as f1
from analysis import F1Session

OUTPUT_DIR: str = "output"

def plotRacePace(f1_session: F1Session) -> None:
    """
    Plottet die Rennzeiten der Fahrer
    """

    f1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

    session = f1_session.session
    drivers = f1_session.drivers
    
    fig, ax = plt.subplots(figsize=(8, 5))

    for driver in drivers:
        laps = session.laps.pick_drivers(driver).pick_quicklaps().reset_index()
        style = plotting.get_driver_style(identifier=driver,
                                        style=['color', 'linestyle'],
                                        session=session)
        ax.plot(laps['LapTime'], **style, label=driver)

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    plotting.add_sorted_driver_legend(ax, session)

    plt.title(f"{f1_session.race} {f1_session.season} {f1_session.sessionType}")
    plt.grid(True)

    plt.savefig(f"{OUTPUT_DIR}/race_pace.png")
    plt.close()
    print(f"Pace-Plot gespeichert in {OUTPUT_DIR}/race_pace.png")

def PlotTyreStrategy(f1_session: F1Session) -> None:
    """Plottet die Reifenwechselstrategie der Fahrer"""

    fig, ax = plt.subplots(figsize=(5, 10))

    session = f1_session.session
    drivers = f1_session.drivers
    stints = f1_session._tyreChanges

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]

        previous_stint_end = 0
        for idx, row in driver_stints.iterrows():
            compound_color = f1.plotting.get_compound_color(row["Compound"],
                                                                session=session)
            plt.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=compound_color,
                edgecolor="black",
                fill=True
            )

            previous_stint_end += row["StintLength"]

    plt.title(f"{f1_session.race} {f1_session.season} {f1_session.sessionType}")
    plt.xlabel("Lap Number")
    plt.grid(False)
    ax.invert_yaxis()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/tyre_strategy.png")
    plt.close()
    print(f"Tyre-Plot gespeichert in {OUTPUT_DIR}/tyre_strategy.png")