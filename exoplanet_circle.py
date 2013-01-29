# Code to produce an xkcd style plot using the latest exoplanet data
# Code pulls data via SQL-type query to the IPAC Exoplanet Archive
# Confirmed exoplanets are plotted in a circle, and candidates are plotted in an enclosing annulus 

import numpy as np
import exoplanet_data as exo
import exo_circle_functions as fun
import matplotlib.pyplot as plt
from time import sleep

pi = 3.141592654
rearth = 6.371e7/7.1492e8 # Earth Radius in Jupiter Radii
rjup = 1.0/rearth # Jupiter Radius in Earth Radii

area_spacing_factor = 2.0 # Increases the area of the circle to allow gaps
placing_spacing = 1.1 # Tolerance for distance between planets. 1=planets can touch
graphic_border = 1.4 # How big is the graphic relative to the area of the annulus/circle?

guess_radius_from_mass = True # Set this to true to estimate planet radius from mass

# 1. Pull exoplanet data using NASA API

weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'
    
# First confirmed exoplanets

print 'Retrieving confirmed planets'

radii = exo.pull_exoplanet_radii()

# Now candidate exoplanets (Kepler)

print 'Retrieving Kepler Candidates'

radii_c = exo.pull_candidate_exoplanet_radii()

# If requested, pull planets with masses and calculate radii

if guess_radius_from_mass:
    print 'Retrieving other planets with masses'
    
    masses = exo.pull_exoplanet_masses(extraconditions='+AND+pl_rade+is+null')
    
    guessradii = fun.guess_radii_from_masses_PHL(masses)
    
    # Add to confirmed exoplanet list
    
    radii = np.concatenate((radii,guessradii),axis=0)

nplanet = len(radii)
ncandidate = len(radii_c)

if guess_radius_from_mass:
    print 'There are ',nplanet, ' planets with confirmed and calculated radii'
else:
    print 'There are ',nplanet, ' planets with confirmed radii'
    
print 'There are ',ncandidate, ' candidates'



# Sort data into descending order

radii = np.sort(radii)
radarg = np.argsort(radii, axis=0)[::-1]
radii = radii[radarg]

radii_c = np.sort(radii_c)
radarg = np.argsort(radii_c, axis=0)[::-1]
radii_c = radii_c[radarg]

# Set up arrays to store x and y positions

xp = np.zeros(nplanet)
yp = np.zeros(nplanet)

xc = np.zeros(ncandidate)
yc = np.zeros(ncandidate)

# 4. Generate random number seed from today's date

seed = fun.gen_random_seed_date()
print "Today's seed is ",seed

# 5. Calculate maximum area of circle for confirmed planets

circlearea = 0.0

for i in range(nplanet):
    circlearea = circlearea + pi*radii[i]*radii[i]

circlearea = circlearea*area_spacing_factor
circle_rad2 = circlearea/pi
circle_rad = np.sqrt(circle_rad2) 


print 'Total area of exoplanet circles is ',circlearea
print 'This gives a circle of radius ',circle_rad

# 5a. Now calculate maximum area of annulus for candidates

annulusarea= 0.0

for i in range(ncandidate):
    annulusarea = annulusarea + pi*radii_c[i]*radii_c[i]

annulusarea = annulusarea*area_spacing_factor

annulus_rad2 = annulusarea/pi +circle_rad2
annulus_rad = np.sqrt(annulus_rad2)

print 'Total area of candidate circles is ',annulusarea
print 'This gives an annulus of outer radius ',annulus_rad,2.0*radii_c[0]

# Check: Is annulus too thin for largest candidate?

if 2.0*radii_c[0]>(annulus_rad-circle_rad):
    print 'The maximum diameter of an exoplanet candidate is ',radii_c[0]
    annulus_rad = 1.1*2.0*radii_c[0] + circle_rad
    print 'The annulus has been enlarged to fit this exoplanet: new outer radius ',annulus_rad

sleep(3)

# 6. Now begin accept reject to build planet circle
sep = 0.0
i = 0
overlapflag = 0

while i < nplanet:    
    # Randomly select x and y inside the circle
    
    rad = np.random.mtrand.uniform(low=0.0,high = circle_rad-radii[i])
    phi = np.random.mtrand.uniform(low=0.0,high=2.0*pi)
    
    xp[i] = rad*np.cos(phi)
    yp[i] = rad*np.sin(phi)    
     
    overlapflag = 0
    
    # Check - does planet's extent exceed circle radius?    
    overlapflag = fun.test_rad(xp[i], yp[i], radii[i], 0.0, circle_rad)
    if overlapflag==1: continue      
    
    # Now check to see if there is overlap among neighbours
    overlapflag = fun.test_neighbours(i, xp, yp, radii, placing_spacing)    
        
    # Check to see if overlap flagged - if not, increase i by 1
    if overlapflag==0:
        i +=1
        print 'Planet ', i, 'placed'
                
# End while loop

print 'Planets placed: now candidates'
sleep(2)
# Second while loop to place candidates

i=0
overlapflag = 0
sep =0.0

while i<ncandidate:
    # Randomly select x and y inside the annulus
        
    rc = np.random.mtrand.uniform(low=circle_rad+radii_c[i],high=annulus_rad-radii_c[i])
    phic = np.random.mtrand.uniform(low=0.0,high = 2.0*pi)
        
    xc[i] = rc*np.cos(phic)    
    yc[i] = rc*np.sin(phic)
        
    overlapflag = 0
        
    # Check - does planet's extent exceed circle radius?    
    overlapflag = fun.test_rad(xc[i], yc[i], radii_c[i], circle_rad, annulus_rad)    
    if overlapflag==1: continue      
    
    # Now check to see if there is overlap among neighbours
    overlapflag = fun.test_neighbours(i, xc, yc, radii_c, placing_spacing)    
        
    # Check to see if overlap flagged - if not, increase i by 1
    if overlapflag==0:        
        print 'Candidate ', i, 'placed '
        i +=1
    

# End of placing stage
    
# Now plot data: just exoplanets first
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-graphic_border*circle_rad,graphic_border*circle_rad)
ax.set_ylim(-graphic_border*circle_rad,graphic_border*circle_rad)
ax.set_axis_off()
print 'Plotting'


for i in range(nplanet):    
    
    colors = fun.pick_circle_colour(radii[i])
        
    circle1=plt.Circle((xp[i],yp[i]),radius=radii[i],edgecolor='none',facecolor=colors)    
    ax.add_patch(circle1)

if guess_radius_from_mass:
    textstring = str(nplanet)+' exoplanets with confirmed and calculated physical radii as of '
else:   
    textstring = str(nplanet)+' exoplanets with confirmed physical radii as of '
    
fun.make_circle_legend_date(ax,textstring,0.0,0.0)
plt.savefig('confirmed.png', format='png')

# Now plot candidates and planets together

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-graphic_border*annulus_rad,graphic_border*annulus_rad)
ax.set_ylim(-graphic_border*annulus_rad,graphic_border*annulus_rad)
ax.set_axis_off()

# First, add a transparent circle outlining the confirmed exoplanets

circle1 = plt.Circle((0.0,0.0),radius=circle_rad,edgecolor='none',facecolor='slategrey',alpha=0.5)
ax.add_patch(circle1)

# Now add planets
for i in range(nplanet):    
    
    colors = fun.pick_circle_colour(radii[i])    
    circle1=plt.Circle((xp[i],yp[i]),radius=radii[i],edgecolor='none',facecolor=colors)    
    ax.add_patch(circle1)

# Then add candidates
for i in range(ncandidate):    
        
    colors = fun.pick_circle_colour(radii_c[i])    
    circle1=plt.Circle((xc[i],yc[i]),radius=radii_c[i],edgecolor='none',facecolor=colors)    
    ax.add_patch(circle1)

if guess_radius_from_mass:
    textstring = str(nplanet)+' exoplanets with confirmed and calculated physical radii \n'+str(ncandidate)+' candidate exoplanets as of '
else:    
    textstring = str(nplanet)+' exoplanets with confirmed physical radii \n'+str(ncandidate)+' candidate exoplanets as of '
    
fun.make_circle_legend_date(ax,textstring,0.0,0.0)

plt.savefig('combined.png', format='png')

print 'Done'
