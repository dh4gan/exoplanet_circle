Python dependencies:

Written for Python 2.x (untested on 3.0); uses numpy and matplotlib (plus other standard Python modules)

These Python scripts will:

i) Make a wget call to the Exoplanet Archive hosted by IPAC to obtain exoplanets and Kepler candidates where their physical radius is known, and write this data to file;
ii) it then generates two xkcd-style plots of exoplanets plotted inside a circle(the candidates are plotted in an annulus around the confirmed exoplanets)

iii) These images are stored as .png files

exoplanet_circle.py is the main script, which uses functions stored in exoplanet_data.py (which handles the calls to the Archive) and in exo_circle_functions (which handles the placing algorithm and plot legends, etc)
