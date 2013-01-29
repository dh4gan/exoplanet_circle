# Code to produce multiple xkcd style plots using the latest exoplanet data
# Code pulls data via SQL-type query, and delivers all objects with confirmed radii (Earth Radii)

import numpy as np
import exoplanet_data as exo
import exo_circle_functions as fun
import matplotlib.pyplot as plt
from time import sleep
import os

pi = 3.141592654
rearth = 6.371e7/7.1492e8 # Earth Radius in Jupiter Radii
rjup = 1.0/rearth # Jupiter Radius in Earth Radii

area_spacing_factor = 2.0 # Increases the area of the circle to allow gaps
placing_spacing = 1.05 # Tolerance for distance between planets. 1=planets can touch
graphic_border = 1.4 # How big is the graphic relative to the area of the annulus/circle?

guess_radius_from_mass = True # Set this to true to estimate planet radius from mass

# Retrieve candidate exoplanets (Kepler)

#os.system('tcsh')

seed = fun.gen_random_seed_date()
print "Today's seed is ",seed

# Loop over confirmed exoplanet data by discovery date

beginyear,endyear = fun.begin_and_end_years()

print "Generating graphics for years ",beginyear, " to ",endyear

weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'

for j in range(beginyear,endyear):

    # 1. Pull exoplanet data using NASA API

    print 'Retrieving planets detected before ',str(j)

    disc = '+AND+pl_disc<'+str(j+1)
    
    radii = exo.pull_exoplanet_radii(extraconditions=disc)

    # If requested, pull planets with masses and calculate radii

    if guess_radius_from_mass:
        print 'Retrieving other planets with masses'
        disc = disc+'+AND+pl_rade+is+null'
        masses = exo.pull_exoplanet_masses(extraconditions=disc)
        guessradii = fun.guess_radii_from_masses_PHL(masses)
    
        # Add to confirmed candidate list
    
        if(len(radii) > 0):
            radii = np.concatenate((radii,guessradii),axis=0)
        else:
            radii = guessradii
            
    nplanet = len(radii)

    if guess_radius_from_mass:
        print 'There are ',nplanet, ' planets with confirmed and calculated radii'
    else:
        print 'There are ',nplanet, ' planets with confirmed radii'

    # Sort data into descending order

    radii = np.sort(radii)
    radarg = np.argsort(radii, axis=0)[::-1]
    radii = radii[radarg]

    # Set up arrays to store x and y positions

    xp = np.zeros(nplanet)
    yp = np.zeros(nplanet)

    # Calculate maximum area of circle for confirmed planets

    circlearea = 0.0

    for i in range(nplanet):
        circlearea = circlearea + pi*radii[i]*radii[i]

    circlearea = circlearea*area_spacing_factor
    circle_rad2 = circlearea/pi
    circle_rad = np.sqrt(circle_rad2) 

    print 'Total area of exoplanet circles is ',circlearea
    print 'This gives a circle of radius ',circle_rad
   
    sleep(2)

    # Now begin accept reject to build planet circle
    
    sep = 0.0
    i = 0
    overlapflag = 0

    while i < nplanet:    
        # Randomly select x and y inside the circle
    
        rad = np.random.mtrand.uniform(low=0.0,high = circle_rad)
        phi = np.random.mtrand.uniform(low=0.0,high=2.0*pi)
    
        xp[i] = rad*np.cos(phi)
        yp[i] = rad*np.sin(phi)    
     
        overlapflag = 0
    
        # Check - does planet's extent exceed circle radius?    
        #overlapflag = fun.test_rad(xp[i], yp[i], radii[i], 0.0, circle_rad)
        #if overlapflag==1: continue      
    
        # Now check to see if there is overlap among neighbours
        overlapflag = fun.test_neighbours(i, xp, yp, radii, placing_spacing)    
        
        # Check to see if overlap flagged - if not, increase i by 1
        if overlapflag==0:
            i +=1
            print 'Planet ', i, 'placed'
                
    # End while loop

    print 'Planets placed: plotting'
    sleep(2)

    
    # Now plot data 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.set_xlim(-graphic_border*circle_rad,graphic_border*circle_rad)
    #ax.set_ylim(-graphic_border*circle_rad,graphic_border*circle_rad)
    ax.set_xlim(-graphic_border*560.0,graphic_border*560.0)
    ax.set_ylim(-graphic_border*560.0,graphic_border*560.0)
    ax.set_axis_off()

    print 'Plotting'

    if guess_radius_from_mass:
        textstring = str(nplanet)+' exoplanets with confirmed and calculated physical radii as of '+str(j)
    else:   
        textstring = str(nplanet)+' exoplanets with confirmed physical radii as of '+str(j)
    
    fun.make_circle_legend(ax,textstring,0.0,0.0)


    for i in range(nplanet):    
    
        numstring = '0'+str(j)
        colors = fun.pick_circle_colour(radii[i])
        
        circle1=plt.Circle((xp[i],yp[i]),radius=radii[i],edgecolor='none',facecolor=colors)    
        ax.add_patch(circle1)
 
    plt.savefig('confirmed'+numstring+'.png', format='png')
    print 'Year ',str(j), ' Done'
