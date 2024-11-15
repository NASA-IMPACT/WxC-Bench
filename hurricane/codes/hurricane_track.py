import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tropycal.tracks as tracks
import tropycal
from src_utils.coast import plot_domain

def plot_hurdat_track_from_xarray(hurdat, ax):
    """
    Plot the hurricane track and intensity from xarray data on the given axis.

    Parameters:
        hurdat (xarray.Dataset): Hurricane data in xarray format containing "lon", "lat", and "vmax" variables.
        ax (matplotlib.axes.Axes): The axis on which to plot the hurricane track.

    Returns:
        ax (matplotlib.axes.Axes): The updated axis after plotting the hurricane track and scatter points.
        scatter (matplotlib.collections.PathCollection): The scatter points representing wind speed intensity.
        bounds (numpy.ndarray): Array of boundaries for the intensity categories.
    """
    # Define colormap and bounds for the intensity categories
    cmap = plt.cm.jet
    bounds = np.array([0, 32, 64, 83, 96, 113, 137, 150])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
    # Plot hurricane track
    ax.plot(hurdat["lon"], hurdat["lat"], "k")
    
    # Plot scatter points with color representing wind speed
    scatter = ax.scatter(hurdat["lon"], hurdat["lat"], c=hurdat["vmax"], cmap=cmap, norm=norm)
    return ax, scatter, bounds

def main():
    """
    Main function to visualize hurricane tracks and intensities.

    This function retrieves hurricane data for the year 2017 from the North Atlantic basin,
    plots the hurricane tracks on a geographic domain, and adds a color bar for intensity visualization.
    """
    # Set matplotlib parameters
    plt.rcParams.update({"font.size": 14, "font.weight": "bold", "savefig.dpi": 300})

    # Define the URL for the hurricane dataset
    url = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2022-042723.txt"
    
    # Load the North Atlantic basin hurricane data from the specified URL
    basin = tracks.TrackDataset(basin="north_atlantic", atlantic_url=url)

    # Get hurricane data for the year 2017
    hurdat = [
        basin.get_storm((storm_name, 2017))
        for storm_name in basin.get_season(2017).to_dataframe()["name"].values
    ]

    # Define the bounding box for the domain plot
    domain_bb = [-110, -20, 5, 55]
    
    # Plot the domain with a margin of 0
    ax = plot_domain((domain_bb, domain_bb), margin=0)

    if type(hurdat) == tropycal.tracks.storm.Storm:
        # If there's only one hurricane in the dataset, plot its track
        ax, scatter, bounds = plot_hurdat_track_from_xarray(hurdat, ax)
        ax.set_title(f'{hurdat.attrs["name"]} ({hurdat.attrs["year"]})'.upper())
    else:
        # If there are multiple hurricanes in the dataset, plot tracks for each
        for hurdat_tracks in hurdat:
            ax, scatter, bounds = plot_hurdat_track_from_xarray(hurdat_tracks, ax)
            ax.set_title(f'{hurdat[0].attrs["year"]} Atlantic Hurricane Season'.upper())

    # Add a color bar with intensity category labels
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.7)
    cbar.set_ticks((bounds[:-1] + bounds[1:]) / 2)
    cbar.set_ticklabels(["TD", "TS", "Cat 1", "Cat 2", "Cat 3", "Cat 4", "Cat 5"])

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()



