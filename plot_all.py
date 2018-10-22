import IPython, os, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools as itt
import h5py, copy
import numpy.ma as ma
import assignment as asgn
import voronoi_plot as vp

# TODO: Turn this into a tool that handles the pdist'ing 
def plot_in_between(iiter, fiter, h5file=None, mapper_iter=None, outext=None, voronoi=False):
    if not h5file:
        h5file = "../west.h5"
    if not mapper_iter:
        h5 = h5py.File(h5file, 'r')
        mapper_iter = h5.attrs['west_current_iteration'] - 1 

    print("Loading file {}, mapper from iteration {}".format(h5file, mapper_iter))
    mapper = asgn.load_mapper(h5file, mapper_iter)
    cur_path = os.getcwd()

    plt.figure(figsize=(20,20))
    f, axarr = plt.subplots(12,12)
    f.suptitle("%i - %i"%(iiter+1, fiter+1))
    f.subplots_adjust(hspace=0.4, wspace=0.4, bottom=0.1, left=0.1)
    names = {0: "STAT", 1: "GBX2", 2: "KLF4", 3: "KLF2",
             4: "SALL", 5: "OCT4", 6: "SOX2", 7: "NANO",
             8: "ESRR", 9: "TFCP", 10:"TCF3", 11:"MEKE"}
    ymin, ymax = None, None
    print("Plotting")
    if voronoi: 
        print("Plotting voronoi centers")
    for ii,jj in itt.product(range(12),range(12)):
        #print("Plotting dimensions {} vs {}".format(ii,jj))
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
            # plotting the diagonal, 1D plots
            if fi != 12:
                # First pull a file that contains the dimension
                pfile = os.path.join(cur_path, "pdist_{}_{}.h5".format(fi,12))
                datFile = h5py.File(pfile, 'r')
                Hists = datFile['histograms'][iiter:fiter]
                # Get average and average the other dimension
                Hists = Hists.mean(axis=0)
                Hists = Hists.mean(axis=1)
            else:
                # We just need one that contains the last dimension
                pfile = os.path.join(cur_path, "pdist_{}_{}.h5".format(1,12))
                datFile = h5py.File(pfile, 'r')
                Hists = datFile['histograms'][iiter:fiter]
                # Average the correct dimension here
                Hists = Hists.mean(axis=0)
                Hists = Hists.mean(axis=0)

            # Normalize the distribution, take -ln, zero out minimum point
            Hists = Hists/(Hists.flatten().sum())
            Hists = -np.log(Hists)
            Hists = Hists - Hists.min()

            # Calculate the x values, normalize s.t. it spans 0-1
            x_bins = datFile['binbounds_0'][...]
            x_mids = np.array([ (x_bins[i]+x_bins[i+1])/2.0 for i in range(len(x_bins)-1)] )
            x_mids = x_mids/x_mids.max()
      
            # Plot on the correct ax, set x limit
            axarr[ii,jj].plot(x_mids, Hists, label="{} {}".format(fi,fj))
            axarr[ii,jj].set_xlim(0.0, 1.0)
        else:
            # Plotting off-diagonal, plotting 2D heatmaps
            if fi < fj:
                pfile = os.path.join(cur_path, "pdist_{}_{}.h5".format(fi,fj))
                inv = False
            else:
                pfile = os.path.join(cur_path, "pdist_{}_{}.h5".format(fj,fi))
                inv = True
            datFile = h5py.File(pfile, 'r')
    
            # Get average histograms over iterations, 
            # take -ln of the histogram after normalizing 
            # and set minimum to 0 
            Hists = datFile['histograms'][iiter:fiter]
            Hists = Hists.mean(axis=0)
            Hists = Hists/(Hists.sum())
            Hists = -np.log(Hists)
            Hists = Hists - Hists.min()
            # pcolormesh takes in transposed matrices to get 
            # the expected orientation
            e_dist = Hists.T

            # Get x/y bins, normalize them to 1 max
            x_bins = datFile['binbounds_0'][...]
            x_max = x_bins.max()
            x_bins = x_bins/x_max
            y_bins = datFile['binbounds_1'][...]
            y_max = y_bins.max()
            y_bins = y_bins/y_max

            # If we are at the other side of the diagonal line
            if not inv:
                e_dist = e_dist.T
                x_bins, y_bins = y_bins, x_bins
            
            # Set certain values to white to avoid distractions
            cmap = mpl.cm.magma_r
            cmap.set_bad(color='white')
            cmap.set_over(color='white')
            cmap.set_under(color='white')
            # Find min/max of histogram to return eventually
            if ymin == None:
                ymin = e_dist[np.isfinite(e_dist)].min()
            if ymax == None:
                ymax = e_dist[np.isfinite(e_dist)].max()
            if e_dist.min() < ymin:
                ymin = e_dist[np.isfinite(e_dist)].min()
            if e_dist.min() < ymax:
                ymax = e_dist[np.isfinite(e_dist)].max()
            
            # Plot the heatmap
            pcolormesh = axarr[ii,jj].pcolormesh(x_bins, y_bins,
                           e_dist, cmap=cmap, vmin=0.0, vmax=10.0)

            # Set x/y limits
            axarr[ii,jj].set_xlim(0.0, 1.0)
            axarr[ii,jj].set_ylim(0.0, 1.0)

            # Plot vornoi bins if asked
            if voronoi:
                # Get centers from mapper
                X = mapper.centers[:,ii]
                Y = mapper.centers[:,jj]

                # Normalize to 1
                X = X/x_max
                Y = Y/y_max

                # Ensure not all X/Y values are 0
                if not ((X==0).all() or (Y==0).all()):
                    # First plot the centers
                    axarr[ii,jj].scatter(Y,X, s=0.1)

                    # Now get line segments
                    segments = vp.voronoi(Y,X)
                    lines = mpl.collections.LineCollection(segments, color='0.75', lw=0.15)
                    
                    # Plot line segments
                    axarr[ii,jj].add_collection(lines)
                    axarr[ii,jj].ticklabel_format(style='sci')
    
    for i in range(0,12):
        plt.setp([a.get_yticklabels() for a in axarr[:,i]], visible=False)
    for i in range(0,12):
        plt.setp([a.get_xticklabels() for a in axarr[i,:]], visible=False)
    
    if outext:
        outname = "all_{:05d}_{:05d}_{}.png".format(iiter, fiter, outext)
    else:
        outname = "all_{:05d}_{:05d}.png".format(iiter, fiter)
    plt.savefig(outname, dpi=600)
    plt.close()
    return ymin, ymax

if __name__ == "__main__":
    # Command line options
    h5file = sys.argv[1]
    start_iter = int(sys.argv[2])
    end_iter = int(sys.argv[3])
    # Get the regular plot
    plot_in_between(start_iter, end_iter, h5file=h5file)
    # Add voronoi centers
    plot_in_between(start_iter, end_iter, h5file=h5file, outext="vor", voronoi=True)
