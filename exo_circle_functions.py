import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Color tables for plots (picked from xkcd graphic)

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


# Alternative color tables
# Sub Earths
#subearth = (256.0/256.0,0.0/256.0,256.0/256.0)
# Earths
#earth = (78.0/256.0,147/256.0,76/256.0)
# Super Earths
#superearth = (64.0/256.0,22.0/256.0,201.0/256.0)
# Neptunes
#neptunes = (0.0/256.0,87.0/256.0,53.0/256.0)
# Jupiters
#jupiters = (135.0/256.0,40.0/256.0,21.0/256.0)


def begin_and_end_years():
    '''Generates the beginning and end years for producing movies'''
    
    date = datetime.now()
    begin = 2003
    end = date.year
    return begin,end

def gen_random_seed_date():
    '''Uses the date to generate a random number seed'''
    date = datetime.now()
    seed = (date.day*date.year*date.month)
    seed = int(seed)

    np.random.mtrand.RandomState(seed)
    
    return seed


def test_rad(x,y,rad,rmin,rmax):
    '''Tests whether a circle's extent exceeds its prescribed minimum/maximum radii'''
    
    fail = 0
    r = np.sqrt(x*x + y*y)
    if r-rad< rmin and rmin!=0.0: fail=1
    if r+rad>rmax: fail=1
    
    return fail

def test_neighbours(i,xp,yp,radii,placing_spacing):
    '''Tests whether circle i overlaps with any of the other placed circles'''
    
    overlapflag = 0
    # If this is the first planet, everything is fine
    if (i==0):
        overlapflag=0
        return overlapflag
    elif(i>0):        
        # check other planets already placed for intersections
        for j in range(i):    
            
            # Does planet overlap other planet's position?
            sep = (xp[i]-xp[j])**2 + (yp[i]-yp[j])**2
            sep = np.sqrt(sep)
            
            minsep = placing_spacing*(radii[i]+radii[j])
            
            if (sep < minsep and j!=i):
                overlapflag = 1
                #print 'Overlap with ',j
                #print x[i],y[i],x[j],y[j],sep,minsep
                break                    
            
    return overlapflag

def pick_circle_colour(rad):
    '''Selects the plotting colour for the exoplanet depending on its radius'''    

    colors = jupiters
                
    # Sub Earth
    if rad < 0.8:
        colors = subearth        
    elif rad >= 0.8 and rad <1.25:
        colors = earth
    # Super Earths
    elif rad >=1.25 and rad < 2.6:
        colors = superearth
    # Neptunes
    elif rad >=2.6 and rad < 6.0:
        colors = neptunes
    # Jupiters
    elif rad >=6.0:
        colors = jupiters
        
    return colors

def make_circle_legend(axis, textstring,textx,texty):    
    '''Makes circles of each colour to display as a legend to the plot'''
    
    # Find size of x and y axes in pixels
    pointlimits = axis.transData.transform([(0,1),(1,0)])-axis.transData.transform((0,0))
    
    pointscale = np.sum(pointlimits)/2.0
    pointscale = 1.0/pointscale
    #print pointlimits
    #print pointscale
    
    
    line1 = plt.Line2D(range(1), range(1), color="white", marker='o', markersize = 2.0, markerfacecolor=subearth)
    line2 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=2.5*pointscale, markerfacecolor=earth)
    line3 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=3.0*pointscale, markerfacecolor=superearth)
    line4 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=3.5*pointscale, markerfacecolor=neptunes)
    line5 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=5.0*pointscale,markerfacecolor=jupiters)
    
    axis.legend((line1,line2,line3,line4,line5),('Subearth','Earth ', 'Superearth','Neptune', 'Jupiter'),numpoints=1, loc='upper right', bbox_to_anchor= (1.1,1.1))    
    
    axis.text(textx,texty,textstring, style='italic', transform = axis.transAxes,
        bbox={'facecolor':'slategrey', 'alpha':0.01, 'pad':10})

def make_circle_legend_date(axis, textstring,textx,texty):    
    '''Makes circles of each colour to display as a legend to the plot'''
    
    # Find size of x and y axes in pixels
    
    now = datetime.now()
    
    textstring = textstring + str(now.day)+'/'+str(now.month)+'/'+str(now.year)
    
    pointlimits = axis.transData.transform([(0,1),(1,0)])-axis.transData.transform((0,0))
    
    pointscale = np.sum(pointlimits)/2.0
    pointscale = 1.0/pointscale
    #print pointlimits
    #print pointscale
    
    
    line1 = plt.Line2D(range(1), range(1), color="white", marker='o', markersize = 2.0, markerfacecolor=subearth)
    line2 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=2.5*pointscale, markerfacecolor=earth)
    line3 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=3.0*pointscale, markerfacecolor=superearth)
    line4 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=3.5*pointscale, markerfacecolor=neptunes)
    line5 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=5.0*pointscale,markerfacecolor=jupiters)
    
    axis.legend((line1,line2,line3,line4,line5),('Subearth','Earth ', 'Superearth','Neptune', 'Jupiter'),numpoints=1, loc='upper right', bbox_to_anchor= (1.1,1.1))    
    
    axis.text(textx,texty,textstring, style='italic', transform = axis.transAxes,
        bbox={'facecolor':'slategrey', 'alpha':0.01, 'pad':10})


def guess_radii_from_masses_PHL(masses):
    '''Uses input np array of masses to guess radii according to simple mass-radius prescription (phl.pr.edu)'''
    
    radii = np.zeros(len(masses))
    
    for i in range(len(masses)):
        if masses[i] <= 1.0: 
            radii[i] = masses[i]**0.3
        elif masses[i] >1.0 and masses[i] <= 200.0:
            radii[i] = masses[i]**0.5
        elif masses[i] > 200.0:         
            radii[i] = 22.6*masses[i]**(-0.0086)
    
    return radii