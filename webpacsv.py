import pandas as pd
import glob, os

#def calcsvscore(filename='score.csv'):
def calcsvscore(folder, aiclass):
    list_of_files = glob.glob(os.path.join(folder, "*.csv"))  # * means all if need specific format then *.csv
    if (aiclass['csv'] == None):
        lfile = max(list_of_files, key=os.path.getctime)
    else:
        lfile=os.path.join(folder, aiclass['csv'])

    sf = pd.read_csv(lfile)
    lstname = sf['name']
    names = sf.columns.values[1:]

    tscorebyname = {}
    cscorebyname={}
    cnt=0
    for i in range(len(lstname)):
        pf = sf.loc[sf['name'] == lstname[i]]
        cscorebyname[lstname[i]]= list(sf[lstname[i]])
        tscore =0
        ccnt=1
        for name in names:
            tscore= tscore+ int(pf[name])
            if (int(pf[name])!=0):
                ccnt=ccnt*0
    #        pp = (names[j], pf[j])
        cnt=cnt+ccnt
        tscorebyname[lstname[i]]=tscore

    fudge=len(names)/(len(names)-cnt)

    pscorebyname={}
    for n in names:
        nscore=0.0
        for i in range(len(names)):
            ##print("{}:{}~{}~".format(n, cscorebyname[n][i], tscorebyname[names[i]]))
            if (tscorebyname[names[i]]!=0):
                nscore = nscore + round(cscorebyname[n][i]*fudge/tscorebyname[names[i]],2)
        pscorebyname[n]=round(nscore,2)
    return pscorebyname
