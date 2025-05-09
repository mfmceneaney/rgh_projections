import uproot
import pandas as pd
import os

def convert_root_to_csv(inpath, outpath, treename="tree"):
    """
    Convert a ROOT file to a CSV file.

    Parameters
    ----------
    inpath : str
        Path to the ROOT file.
    outpath : str
        Path to the CSV file.
    treename : str
        Name of the TTree in the ROOT file.
    """

    # Open the ROOT file and TTree
    file = uproot.open(inpath)
    tree = file[treename]

    # Convert to pandas DataFrame
    df = tree.arrays(library="pd")

    # Write to CSV
    df.to_csv(outpath, index=False)

# Grab environment variables
RGH_PROJECTIONS_HOME = os.environ['RGH_PROJECTIONS_HOME']

# Set input and output paths
channels = ["pi", "pim", "k", "km"]
treename = "t"
infile = "out_dataset.root"
outfile = infile.replace(".root", ".csv")
inpaths = [os.path.abspath(f"{RGH_PROJECTIONS_HOME}/jobs/saga/test_getKinBinnedAsym__mc_rgh_22GeV__{ch}/{infile}") for ch in channels]
outpaths = [os.path.abspath(f"{RGH_PROJECTIONS_HOME}/jobs/saga/test_getKinBinnedAsym__mc_rgh_22GeV__{ch}/{outfile}") for ch in channels]

# Loop over input and output paths
for inpath, outpath in zip(inpaths, outpaths):
    convert_root_to_csv(inpath, outpath, treename=treename)
