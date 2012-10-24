# Code to produce an xkcd style plot using the latest exoplanet data
# Code pulls data via SQL-type query, and delivers all objects with confirmed radii (Earth Radii)
# Confirmed exoplanets are plotted in a circle, and candidates are plotted in an enclosing annulus 

import numpy as np
import exoplanet_data as exo
import exo_circle_functions as fun
import matplotlib.pyplot as plt

pi = 3.141592654
rearth = 6.371e7/7.1492e8 # Earth Radius in Jupiter Radii
rjup = 1.0/rearth # Jupiter Radius in Earth Radii

area_spacing_factor = 2.0 # Increases the area of the circle to allow gaps
placing_spacing = 1.1 # Tolerance for distance between planets. 1=planets can touch
graphic_border = 1.4 # How big is the graphic relative to the area of the annulus/circle?

# 1. Pull exoplanet data using NASA API

# First confirmed exoplanets

print 'Retrieving confirmed planets'

planetfile = 'planetradii.dat'
table = 'table=exoplanets'
entries = '&select=pl_rade'
conditions = '&where=pl_rade+is+not+null'
order = '&order=pl_rade'
form = '&format=ascii'

exo.pull_exoplanet_data(table,entries,order,conditions,form,planetfile)

# Now candidate exoplanets (Kepler)

print 'Retrieving Kepler Candidates'

# Repeat this exercise for the Kepler candidates

table = 'table=keplercandidates'
entries = '&select=prad'
conditions = '&where=prad+is+not+null'
order = '&order=prad'
candidatefile = 'candidateradii.dat'

exo.pull_exoplanet_data(table,entries,order,conditions,form,candidatefile)

# 3. Read files into numpy arrays

radii = np.genfromtxt(planetfile, skiprows=11)
nplanet = len(radii)

radii_c = np.genfromtxt(candidatefile,skiprows=11)

ncandidate = len(radii_c)

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
print 'This gives an annulus of radius ',annulus_rad

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

# Second while loop to place candidates

i=0
overlapflag = 0
sep =0.0

while i<ncandidate:
    # Randomly select x and y inside the annulus
        
    rc = np.random.mtrand.uniform(low=circle_rad,high=annulus_rad-radii_c[i])
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
 
    
textstring = str(nplanet)+' exoplanets with confirmed physical radii as of '
    
fun.make_circle_legend(ax,textstring,0.0,0.0)
plt.savefig('confirmed.png', format='png',dpi=300)

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

textstring = str(nplanet)+' exoplanets with confirmed physical radii \n'+str(ncandidate)+' candidate exoplanets as of '
    
fun.make_circle_legend(ax,textstring,0.0,0.0)

plt.savefig('combined.png', format='png', dpi=300)

print 'Done'
