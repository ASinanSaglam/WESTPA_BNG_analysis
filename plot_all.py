import IPython, os, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools as itt
import h5py, copy
import numpy.ma as ma
import assignment as ass
import voronoi_plot as vp

def plot_in_between(iiter, fiter, h5file=None):
    if h5file:
        mapper = ass.load_mapper(h5file, 38)
    else:
        h5file = "../west.h5"
        mapper = ass.load_mapper(h5file, 38)
    cur_path = os.getcwd()

    plt.figure(figsize=(20,20))
    f, axarr = plt.subplots(12,12)
    f.suptitle("%i - %i"%(iiter+1, fiter+1))
    f.subplots_adjust(hspace=0.4, wspace=0.4, bottom=0.1, left=0.1)
    names = {0: "STAT", 1: "GBX2", 2: "KLF4", 3: "KLF2",
             4: "SALL", 5: "OCT4", 6: "SOX2", 7: "NANO",
             8: "ESRR", 9: "TFCP", 10:"TCF3", 11:"MEKE"}
    ymin, ymax = None, None
    for ii,jj in itt.product(range(12),range(12)):
        print(ii,jj)
        inv = False
        fi, fj = ii+1, jj+1

        for kw in ['top', 'right']:
            axarr[ii,jj].spines[kw].set_visible(False)
        axarr[ii,jj].tick_params(left=False, bottom=False)
    
        if ii == 11:
            # set x label
            axarr[ii,jj].set_xlabel(names[jj])
        if jj == 0:
            # set y label
            axarr[ii,jj].set_ylabel(names[ii], fontsize=8)
        if fi == fj:
            #print("Diag")
            #print(fi,fj)
            if fi != 12:
                pfile = os.path.join(cur_path, "pdist_%i_%i.h5"%(fi,12))
                #print(pfile)
                datFile = h5py.File(pfile, 'r')
                Hists = datFile['histograms'][iiter:fiter]
                Hists = Hists.mean(axis=0)
                Hists = Hists.mean(axis=1)
            else:
                pfile = 
                os.path.join(cur_path, "/pdist_%i_%i.h5"%(1,12))
                #print(pfile)
                datFile = h5py.File(pfile, 'r')
                Hists = datFile['histograms'][iiter:fiter]
                Hists = Hists.mean(axis=0)
                Hists = Hists.mean(axis=0)
            # Diagonal, plot 1D
            # Done for RMSD 
            Hists = Hists/(Hists.flatten().sum())
            Hists = -np.log(Hists)
            #Hists[np.isinf(Hists)] = np.nan
            #Hists[Hists>30] = np.nan
            #Hists = ma.MaskedArray(Hists, mask=np.isnan(Hists))
            #Hists[np.isnan(Hists)] = np.nanmax(Hists)
            #print(Hists.min(), Hists.max())
            Hists = Hists - Hists.min()
            #print(Hists.min(), Hists.max())
            #Hists = Hists * (5.0/np.nanmax(Hists))
            y_bins = datFile['binbounds_0'][...]
            
            y_mids = np.array([ (y_bins[i]+y_bins[i+1])/2.0 for i in range(len(y_bins)-1)] )
            y_mids = y_mids/y_mids.max()
      
            axarr[ii,jj].plot(y_mids, Hists, label="%i %i"%(fi,fj))
            axarr[ii,jj].set_xlim(0.0, 1.0)
        else:
            #print("Off-diag")
            if fi < fj:
                pfile = os.path.join(cur_path, "pdist_%i_%i.h5"%(fi,fj))
                inv = False
            else:
                pfile = os.path.join(cur_path, "pdist_%i_%i.h5"%(fj,fi))
                inv = True
            #print(pfile)
            datFile = h5py.File(pfile, 'r')
    
            Hists = datFile['histograms'][iiter:fiter]
            #print(Hists.shape)
            Hists = Hists.mean(axis=0)
            Hists = Hists - Hists.min()
            Hists = Hists/(Hists.sum())
            Hists = -np.log(Hists)
            #Hists[np.isinf(Hists)] = np.nan
            #Hists[Hists>30] = np.nan
            #Hists = ma.MaskedArray(Hists, mask=np.isnan(Hists))
            Hists = (Hists - Hists.min()).T
            #print(Hists.min(), Hists.max())
            e_dist = Hists
            x_bins = datFile['binbounds_0'][...]
            x_bins = x_bins/x_bins.max()
            y_bins = datFile['binbounds_1'][...]
            y_bins = y_bins/y_bins.max()
            if inv:
                e_dist = Hists.T
                x_bins, y_bins = y_bins, x_bins
            
            cmap = mpl.cm.magma_r
            cmap.set_bad(color='white')
            cmap.set_over(color='white')
            cmap.set_under(color='white')
            if ymin == None:
                ymin = e_dist[np.isfinite(e_dist)].min()
            if ymax == None:
                ymax = e_dist[np.isfinite(e_dist)].max()
            if e_dist.min() < ymin:
                ymin = e_dist[np.isfinite(e_dist)].min()
            if e_dist.min() < ymax:
                ymax = e_dist[np.isfinite(e_dist)].max()
            pcolormesh = axarr[ii,jj].pcolormesh(x_bins, y_bins,
                           e_dist.T, cmap=cmap, vmin=0.0, vmax=10.0)
            axarr[ii,jj].set_xlim(0.0, 1.0)
            axarr[ii,jj].set_ylim(0.0, 1.0)
            # Plot vornoi bins
            #X = mapper.centers[:,ii]
            #Y = mapper.centers[:,jj]
            #print(X, Y)
            #print(X.shape, Y.shape)
            #if not ((X==0).all() or (Y==0).all()):
            #    axarr[ii,jj].scatter(Y,X, s=0.1)
            #    segments = vp.voronoi(Y,X)
            #    lines = mpl.collections.LineCollection(segments, color='0.75', lw=0.15)
            #    axarr[ii,jj].add_collection(lines)
            #    axarr[ii,jj].ticklabel_format(style='sci')
    
    #for i in range(1,8):
    for i in range(0,12):
        plt.setp([a.get_yticklabels() for a in axarr[:,i]], visible=False)
    #for i in range(0,7):
    for i in range(0,12):
        plt.setp([a.get_xticklabels() for a in axarr[i,:]], visible=False)
    
    plt.savefig("all_%05d_%05d.png"%(iiter,fiter), dpi=600)
    plt.close()
    return ymin, ymax

#ymin, ymax = plot_in_between(1000, 1500)
#print(ymin, ymax)
#for i in range(0,1450):
#    print(i)
#    plot_in_between(i, i+50)
if __main__ == "__name__":
    h5file = sys.argv[1]
    plot_in_between(0, 38, h5file=h5file)
