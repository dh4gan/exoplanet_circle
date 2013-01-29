import numpy as np
from os import system


def pull_exoplanet_radii(extraconditions=''):
    '''Uses wget to pull exoplanet radii (in Earth Radii) from Exoplanet Archive (Caltech) using its API
    (See http://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html for documentation)'''
    
    # Pull data and write to file
    
    weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'
     
    filename = 'planetradii.dat'
    table = 'table=exoplanets'
    entries = '&select=pl_rade'
    conditions = '&where=pl_rade+is+not+null'+extraconditions
    order = '&order=pl_rade'
    form = '&format=ascii'

    #command = 'wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    command = '/usr/local/bin/wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    system(command)
    
    # Read data from file into array and return it
    radii = np.genfromtxt(filename,skiprows=11)
    
    # Delete file
    command = 'rm '+filename
    system(command)
    
    return radii
    
def pull_exoplanet_masses(extraconditions=''):
    '''Uses wget to pull exoplanet mass (in Earth masses) from Exoplanet Archive (Caltech) using its API
    (See http://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html for documentation)'''
     # Pull data and write to file
    
    weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'
     
    filename = 'planetmasses.dat'
    table = 'table=exoplanets'
    entries = '&select=pl_msinie'
    conditions = '&where=pl_msinie+is+not+null'
    order = '&order=pl_msinie'
    form = '&format=ascii'

    #command = 'wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    command = '/usr/local/bin/wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    system(command)
    
    # Read data from file into array and return it
    masses = np.genfromtxt(filename,skiprows=11)
    
    # Delete file
    command = 'rm '+filename
    system(command)
    
    return masses
    
    
def pull_candidate_exoplanet_radii(extraconditions=''):
    '''Uses wget to pull candidate exoplanet radii (in Earth Radii) from Exoplanet Archive (Caltech) using its API
    (See http://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html for documentation)'''
    
    # Pull data and write to file
    
    weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'
     
    filename = 'candidateradii.dat'
    table = 'table=q1_q6_kepler_candidates'
    entries = '&select=koi_prad'
    conditions = '&where=koi_prad+is+not+null'
    order = '&order=koi_prad'
    form = '&format=ascii'

    #command = 'wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    command = '/usr/local/bin/wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    system(command)
    
    # Read data from file into array and return it
    radii = np.genfromtxt(filename,skiprows=11)
    
    # Delete file
    command = 'rm '+filename
    system(command)
    
    return radii