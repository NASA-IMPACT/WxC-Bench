import tropycal.tracks as tracks
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 17, "font.weight": "bold"})


def plot_intensity(name='michael', year=2018, start=1, skip=10):
    """
    Plot the intensity of a hurricane over time using maximum sustained wind speed and minimum sea pressure.

    Parameters:
        name (str): The name of the hurricane.
        year (int): The year of the hurricane.
        start (int): The index to start plotting the data.
        skip (int): The number of data points to skip when plotting.

    Returns:
        None
    """
    url = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2022-042723.txt"
    basin = tracks.TrackDataset(basin='north_atlantic', atlantic_url=url)

    storm = basin.get_storm((name, year))

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    color = 'tab:blue'
    ax.plot(storm['date'][start:-skip], storm['vmax'][start:-skip], color=color, marker='d')
    ax.set_ylabel('Maximum Sustained Wind Speed (kt)', color=color)
    ax.set_xlabel('Date (YYYY-MM-DD)', color='k')
    ax.set_yticks(np.arange(0, 150, 30))
    ax.tick_params(axis='y', labelcolor=color)

    ax2 = ax.twinx()
    color = 'tab:red'
    ax2.plot(storm['date'][start:-skip], storm['mslp'][start:-skip], color=color, marker='d')
    ax2.set_ylabel('Minimum Sea Pressure Level (hPa)', color=color)
    ax.tick_params(axis='x', which='major', rotation=30, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    ax.grid()
    ax.set_title(f'{name.upper()} {year}')
    plt.tight_layout()
    plt.savefig(f'figures/Intensity_{name.upper()}_{year}.jpeg', dpi=300)
    plt.close()


if __name__ == "__main__":
    # Call the function to plot intensity for specific hurricanes and years
    plot_intensity(name='alicia', year=1983, start=2)
    plot_intensity(name='harvey', year=2017, start=2)
    plot_intensity(name='laura', year=2020, start=2)
    plot_intensity(name='ike', year=2008, start=2)
    plot_intensity(name='rita', year=2005, start=2)

