import IPython, os, sys, h5py
import subprocess as sbpc
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools as itt
import assignment as asgn
import voronoi_plot as vp

# Hacky way to disable warnings so we can focus on important stuff
import warnings 
warnings.filterwarnings("ignore")

class HighDimPlotter:
    def __init__(self, h5file="../west.h5", mapper_iter=None, outext=None, names=None):
        # TODO Work on getting argparse in here

        # Absolutely needed
        self.h5file_path = h5file
        # open the file itself
        self.h5file = h5py.File(self.h5file_path, 'r')

        # We can determine an iteration to pull the mapper from
        # ourselves
        if not mapper_iter:
            mapper_iter = self.h5file.attrs['west_current_iteration'] - 1
        self.mapper_iter = mapper_iter

        # Load in mapper from the iteration given/found
        print("Loading file {}, mapper from iteration {}".format(h5file, mapper_iter))
        self.mapper = asgn.load_mapper(self.h5file_path, self.mapper_iter)

        # Let's set the default behavior to work on the current path for now
        self.work_path = os.getcwd()

        # Let's setup names for ourselves, we don't know dim rn so we can't setup a default
        self.names = names

        # Do we need an extension?
        self.outext = outext

    def set_dims(self, dims=None):
        if not dims:
            dims = self.h5file['iterations/iter_{:08d}'.format(1)]['pcoord'].shape[2]
        self.dims = dims
        
        # We now know the dimensionality, can assume a 
        # naming scheme if we don't have one
        if not self.names:
            self.names = dict( (i, str(i)) for i in range(dims) )

        # return the dimensionality if we need to 
        return self.dims

    def setup_figure(self, dims=None):
        self.set_dims(dims)
        # Setup the figure and names for each dimension
        plt.figure(figsize=(20,20))
        f, axarr = plt.subplots(self.dims,self.dims)
        return f, axarr

    def save_fig(self, ext=None, iiter=None, fiter=None):
        # passed extension overwrites default
        if ext:
            outext = ext
        elif self.outext:
            outext = self.outext
        else:
            outext = None

        # setup our output filename
        if outext:
            outname = "all_{:05d}_{:05d}_{}.png".format(iiter, fiter, outext)
        else:
            outname = "all_{:05d}_{:05d}.png".format(iiter, fiter)

        # save the figure
        plt.savefig(outname, dpi=600)
        plt.close()
        return 

    def open_pdist_file(self, fdim, sdim):
        # TODO: Rewrite so that it uses w_pdist directly and we can avoid using
        # --construct-dataset and remove the dependency on assignment.py here
        pfile = os.path.join(self.work_path, "pdist_{}_{}.h5".format(fdim, sdim))
        # for now let's just get it working
        try:
            open_file = h5py.File(pfile, 'r')
            return open_file
        except IOError:
            print("Cannot open pdist file for {} vs {}, calling w_pdist".format(fdim, sdim))
            # We are assuming we don't have the file now
            # TODO: Expose # of bins somewhere, this is REALLY hacky,
            # I need to fiddle with w_pdist to fix it up
            f = open("data_to_pull.txt", "w")
            f.write("{} {}".format(fdim, sdim))
            f.close()
            proc = sbpc.Popen(["w_pdist", "-W", "{}".format(self.h5file_path), 
                       "-o", "{}".format(pfile), "-b", "100", 
                       "--construct-dataset", "assignment.pull_data"])
            proc.wait()
            assert proc.returncode == 0, "w_pdist call failed, exiting"
            open_file = h5py.File(pfile, 'r')
            return open_file
            
    def plot(self, iiter=None, fiter=None, voronoi=False, ext=None):
        if not iiter:
            iiter = 0
        if not fiter:
            fiter = self.h5file.attrs['west_current_iteration'] - 1

        f, axarr = self.setup_figure()
        f.suptitle("%i - %i"%(iiter+1, fiter+1))
        f.subplots_adjust(hspace=0.4, wspace=0.4, bottom=0.1, left=0.1)
        # Loop over every dimension vs every other dimension
        # TODO: We could just not plot the lower triangle and 
        # save time and simplify code
        for ii,jj in itt.product(range(self.dims),range(self.dims)):
            inv = False
            fi, fj = ii+1, jj+1

            # It's too messy to plot the spines and ticks for large dimensions
            for kw in ['top', 'right']:
                axarr[ii,jj].spines[kw].set_visible(False)
            axarr[ii,jj].tick_params(left=False, bottom=False)
        
            # Set the names if we are there
            if ii == 11:
                # set x label
                axarr[ii,jj].set_xlabel(self.names[jj])
            if jj == 0:
                # set y label
                axarr[ii,jj].set_ylabel(self.names[ii], fontsize=8)

            # Check what type of plot we want
            if fi == fj:
                # plotting the diagonal, 1D plots
                if fi != 12:
                    # First pull a file that contains the dimension
                    pfile = os.path.join(self.work_path, "pdist_{}_{}.h5".format(fi,self.dims))
                    datFile = self.open_pdist_file(fi, self.dims)
                    Hists = datFile['histograms'][iiter:fiter]
                    # Get average and average the other dimension
                    Hists = Hists.mean(axis=0)
                    Hists = Hists.mean(axis=1)
                else:
                    # We just need one that contains the last dimension
                    pfile = os.path.join(self.work_path, "pdist_{}_{}.h5".format(1,self.dims))
                    datFile = self.open_pdist_file(1, self.dims)
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
                x_mids = x_mids/x_bins.max()
          
                # Plot on the correct ax, set x limit
                axarr[ii,jj].set_xlim(0.0, 1.0)
                axarr[ii,jj].plot(x_mids, Hists, label="{} {}".format(fi,fj))
            else:
                # Plotting off-diagonal, plotting 2D heatmaps
                if fi < fj:
                    datFile = self.open_pdist_file(fi, fj)
                    inv = False
                else:
                    datFile = self.open_pdist_file(fj, fi)
                    inv = True
        
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

                # Set x/y limits
                axarr[ii,jj].set_xlim(0.0, 1.0)
                axarr[ii,jj].set_ylim(0.0, 1.0)
                
                # Plot the heatmap
                pcolormesh = axarr[ii,jj].pcolormesh(x_bins, y_bins,
                               e_dist, cmap=cmap, vmin=0.0, vmax=10.0)

                # Plot vornoi bins if asked
                if voronoi:
                    # Get centers from mapper
                    X = self.mapper.centers[:,ii]
                    Y = self.mapper.centers[:,jj]

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

        self.save_fig(ext=ext, iiter=iiter, fiter=fiter)
        return

if __name__ == "__main__":
    names = {0: "STAT", 1: "GBX2", 2: "KLF4", 3: "KLF2",
             4: "SALL", 5: "OCT4", 6: "SOX2", 7: "NANO",
             8: "ESRR", 9: "TFCP", 10:"TCF3", 11:"MEKE"}
    # Get the regular plot
    hdp = HighDimPlotter(h5file="west.h5", names=names)
    hdp.plot()
    # Add voronoi centers
    hdp.plot(ext="vor", voronoi=True)
