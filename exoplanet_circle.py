# Code to produce an xkcd style plot using the latest exoplanet data
# Code pulls data via SQL-type query, and delivers all objects with confirmed radii (Earth Radii)
# Confirmed exoplanets are plotted in a circle, and candidates are plotted in an enclosing annulus
# TODO - add legend with: exoplanet numbers, key to different 
# TODO - create functions for placing, accept-reject, etc
# TODO - optimise algorithm: try small modifications to placing to prevent rejection
import numpy as np
import os
import sys
from datetime import datetime
import time
import matplotlib.pyplot as plt

pi = 3.141592654
rearth = 6.371e7/7.1492e8 # Earth Radius in Jupiter Radii
rjup = 1.0/rearth # Jupiter Radius in Earth Radii

area_spacing_factor = 2.0 # Increases the area of the circle to allow gaps
placing_spacing = 1.1 # Tolerance for distance between planets. 1=planets can touch
graphic_border = 1.1

# 1. Pull exoplanet data using NASA API

planetfile = 'planetradii.dat'

#print 'Retrieving confirmed exoplanets'

#weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'
#table = 'table=exoplanets'
#entries = '&select=pl_rade'
#conditions = '&where=pl_rade+is+not+null'
#order = '&order=pl_rade'
#form = '&format=ascii'

#command = 'wget "'+weblink+table+entries+order+conditions+form+'" -O "'+planetfile+'"'
#os.system(command)

#print 'Now retrieving candidates'

#time.sleep(2)
# Repeat this exercise for the Kepler candidates

#table = 'table=keplercandidates'
#entries = '&select=prad'
#conditions = '&where=prad+is+not+null'
#order = '&order=prad'
candidatefile = 'candidateradii.dat'

#command = 'wget "'+weblink+table+entries+order+conditions+form+'" -O "'+candidatefile+'"'
#os.system(command)

# 3. Read files into numpy arrays

radii = np.genfromtxt(planetfile, skiprows=11)
nplanet = len(radii)

radii_c = np.genfromtxt(candidatefile,skiprows=11)

ncandidate = len(radii_c)

print 'There are ',nplanet, ' planets'
print 'There are ',ncandidate, ' candidates'

# Sort data into descending order

radii = np.sort(radii)
radarg = np.argsort(radii, axis=0)[::-1]
radii = radii[radarg]

radii_c = np.sort(radii_c)
radarg = np.argsort(radii_c, axis=0)[::-1]
candidateradii = radii_c[radarg]

xp = np.zeros(nplanet)
yp = np.zeros(nplanet)

xc = np.zeros(ncandidate)
yc = np.zeros(ncandidate)

# 4. Generate random number seed from today's date

date = datetime.now()
seed = (date.day*date.year*date.month)
seed = int(seed)

np.random.mtrand.RandomState(seed)

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

annulus_rad2 = annulusarea/pi +circle_rad*circle_rad
annulus_rad = np.sqrt(annulus_rad2)


print 'Total area of candidate circles is ',annulusarea
print 'This gives a circle of radius ',annulus_rad

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
    rad2 = xp[i]*xp[i] + yp[i]*yp[i]
    
    if(rad2 > circle_rad2): continue
    
    # If this is not the first planet
    if(i>0):
        # check other planets already placed for intersections
        for j in range(i):    
            #print i, j
            # Does planet overlap other planet's position?
            sep = (xp[i]-xp[j])**2 + (yp[i]-yp[j])**2
            sep = np.sqrt(sep)
            
            minsep = placing_spacing*(radii[i]+radii[j])
            
            if (sep < minsep and j!=i):
                overlapflag = 1
                #print 'Overlap with ',j
                #print x[i],y[i],x[j],y[j],sep,minsep
                break
        
    # Check to see if overlap flagged - if not, increase i by 1
    if overlapflag==0:
        i +=1
        print 'Planet ', i, 'placed'
                
# End while loop

# Second while loop to place candidates

while i<ncandidate:
    # Randomly select x and y inside the annulus
        
    rc = np.random.mtrand.uniform(low=circle_rad,high=annulus_rad-radii_c[i])
    phic = np.random.mtrand.uniform(low=0.0,high = 2.0*pi)
        
    xc[i] = rc*np.cos(phic)    
    yc[i] = rc*np.sin(phic)
        
    overlapflag = 0
    
    # Check - does planet's extent exceed annulus radius?
    rad2 = (rc+ radii_c[i])**2
    
    # Outer condition
    if(rad2 > annulus_rad2): continue
    
    # inner condition    
    minsep = radii_c[i]+circle_rad
    
    if(rc<minsep): continue
    
    # If this is not the first planet
    if(i>0):
        # check other planets already placed for intersections
        for j in range(i):    
            #print i, j
            # Does planet overlap other planet's position?
            sep = (xc[i]-xc[j])**2 + (yc[i]-yc[j])**2
            sep = np.sqrt(sep)
            
            minsep = placing_spacing*(radii_c[i]+radii_c[j])
            
            if (sep < minsep and j!=i):
                overlapflag = 1
                #print 'Overlap with ',j
                #print x[i],y[i],x[j],y[j],sep,minsep
                break
        
    # Check to see if overlap flagged - if not, increase i by 1
    if overlapflag==0:
        i +=1
        print 'Candidate ', i, 'placed'
    
# Now plot data: just exoplanets first
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-graphic_border*circle_rad,graphic_border*circle_rad)
ax.set_ylim(-graphic_border*circle_rad,graphic_border*circle_rad)
ax.set_axis_off()
print 'Plotting'


for i in range(nplanet):    
    
    # Change colors according to categories:    
    # Sub Earths (lightblue)
    subearth = (29.0/256.0,166.0/256.0,97.0/256.0)
    # Earths
    earth = (20.0/256.0,107.0/256.0,135.0/256.0)
    # Super Earths
    superearth = (135.0/256.0,99/256.0,21/256.0)
    # Neptunes
    neptunes = (84.0/256.0,53.0/256.0,16.0/256.0)
    # Jupiters
    jupiters = (135.0/256.0,40.0/256.0,21.0/256.0)
    
    colors = jupiters
    
    # Sub Earth
    if radii[i] < 0.8:
        colors = subearth        
    elif radii[i] >= 0.8 and radii[i] <1.25:
        colors = earth
    # Super Earths
    elif radii[i] >=1.25 and radii[i] < 2.6:
        colors = superearth
    # Neptunes
    elif radii[i] >=2.6 and radii[i] < 6.0:
        colors = neptunes
    # Jupiters
    elif radii[i] >=6.0:
        colors = jupiters
        
    circle1=plt.Circle((xp[i],yp[i]),radius=radii[i],edgecolor='none',facecolor=colors)    
    ax.add_patch(circle1)
    #plt.draw()    
    #time.sleep(2)
    
plt.savefig('confirmed.png', format='png')
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-graphic_border*annulus_rad,graphic_border*annulus_rad)
ax.set_ylim(-graphic_border*annulus_rad,graphic_border*annulus_rad)
ax.set_axis_off()

# Now add candidates and planets together

for i in range(nplanet):    
    
    # Change colors according to categories:    
    # Sub Earths (lightblue)
    subearth = (29.0/256.0,166.0/256.0,97.0/256.0)
    # Earths
    earth = (20.0/256.0,107.0/256.0,135.0/256.0)
    # Super Earths
    superearth = (135.0/256.0,99/256.0,21/256.0)
    # Neptunes
    neptunes = (84.0/256.0,53.0/256.0,16.0/256.0)
    # Jupiters
    jupiters = (135.0/256.0,40.0/256.0,21.0/256.0)
    
    colors = jupiters
    
    # Sub Earth
    if radii[i] < 0.8:
        colors = subearth        
    elif radii[i] >= 0.8 and radii[i] <1.25:
        colors = earth
    # Super Earths
    elif radii[i] >=1.25 and radii[i] < 2.6:
        colors = superearth
    # Neptunes
    elif radii[i] >=2.6 and radii[i] < 6.0:
        colors = neptunes
    # Jupiters
    elif radii[i] >=6.0:
        colors = jupiters
        
    circle1=plt.Circle((xp[i],yp[i]),radius=radii[i],edgecolor='none',facecolor=colors)    
    ax.add_patch(circle1)

for i in range(ncandidate):    
        
    colors = jupiters
    
    # Sub Earth
    if radii_c[i] < 0.8:
        colors = subearth        
    elif radii_c[i] >= 0.8 and radii_c[i] <1.25:
        colors = earth
    # Super Earths
    elif radii_c[i] >=1.25 and radii_c[i] < 2.6:
        colors = superearth
    # Neptunes
    elif radii_c[i] >=2.6 and radii_c[i] < 6.0:
        colors = neptunes
    # Jupiters
    elif radii_c[i] >=6.0:
        colors = jupiters
        
    circle1=plt.Circle((xc[i],yc[i]),radius=radii_c[i],edgecolor='none',facecolor=colors)    
    ax.add_patch(circle1)

plt.savefig('combined.png', format='png')
#plt.show()

print 'Done'
