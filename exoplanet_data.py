import os


def pull_exoplanet_data(table,entries,order,conditions,form,filename):
    '''Uses wget to pull exoplanet data from Exoplanet Archive (Caltech) using its API
    (See http://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html for documentation)'''
    
    # 1. Pull exoplanet data using NASA API

    weblink = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'
    command = 'wget "'+weblink+table+entries+order+conditions+form+'" -O "'+filename+'"'
    os.system(command)
    