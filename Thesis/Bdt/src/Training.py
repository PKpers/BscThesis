#!/usr/bin/python
import ROOT
import numpy as np
import pickle
from copy import copy
from matplotlib import pyplot as plt 

def pair_permute(__list__):
    '''
    combine the items of a list
    in pairs of two.
    order doesn't matter
    repetition allowed
    '''
    permutations = []
    for i, xi in enumerate(__list__):
        if type(xi) is str:
            p = [xi+xj for xj in __list__[i:]]
        #
        permutations += p
    #
    return permutations

def make_variable_names(signal_filename, background_filename):
    variables = []
    names=()
    if "Pxyz" in signal_filename and "Pxyz" in background_filename:
        names=("Px", "Py", "Pz") 
    else:
        names=("Pt", "Eta", "Phi") 
    #
    for j in range(1, 3):
        for name in names:
            variables.append(name+str(j))
        #
    #
    if 'Perm' in signal_filename and 'Perm' in background_filename:
        variables = pair_permute(variables)
    elif 'Deltas' in signal_filename and 'Deltas' in background_filename:
        variables = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta"]
    #
    print(variables)
    return variables
#


def make_bar_graph(variables, feat_imp):
    plt.bar(variables, feat_imp)
    plt.ylabel('Featrue importance')
    plt.savefig("/home/kpapad/UG_thesis/Thesis/Bdt/out/Plots/feature_importance.pdf")
    return

def load_data(signal_filename, background_filename):
    # Read data from ROOT files
    data_sig = ROOT.RDataFrame("tree", signal_filename).AsNumpy()
    data_bkg = ROOT.RDataFrame("tree", background_filename).AsNumpy()

    # create the variable names(instead of typing them one by one)
    variables = make_variable_names(signal_filename, signal_filename) 
    
    # Convert inputs to format readable by machine learning tools
    x_sig = np.vstack([data_sig[var] for var in variables]).T
    x_bkg = np.vstack([data_bkg[var] for var in variables]).T
    
    x = np.vstack([x_sig, x_bkg]).astype(np.float32)
    # Create labels
    #number of events. After transposing , we have an object of that form [ [], [], ..., [] ]
    # each sub array corresponds to the number of event: [ [1st event contents ], [2nd, ] ... ]
    #spape method, returns the lentgh of each dimention of the array.
    #In our case the array is 2 dimentional. To describe the position of an element in the array,
    #we need one index to specify the number of the event the the element is in
    #and another one to specify its position inside the event(eg the jth element of the ith event)
    #so x_sig.shape is a tuple whose elements is number of events and number of elements in each event
    #from that tuple we take the 0th element which is the number of events 
    num_sig = x_sig.shape[0]#same as len(np.array) returns error
    num_bkg = x_bkg.shape[0]
    y = np.hstack([np.ones(num_sig), np.zeros(num_bkg)]).astype(np.float32)

   # ones(n): return an array of shape n filled with 1
   #zeros(n): return an array of shape n filled with 0
   #[np.array(), np.array()] -hstack-> np.array[contents of the two arrays merged]
   
    # Compute weights balancing both classes
    num_all = num_sig + num_bkg
    w = np.hstack([np.ones(num_sig) * num_all / num_sig, np.ones(num_bkg) * num_all / num_bkg])\
          .astype(np.float32)
    #asign the same weight in all sig events and the same in all bkg events. wsig != wbkg.
    #np.ones it is used to create an array of diemntion = num_bkg
    return x, y, w, num_all
 # ======================================================================= #
 # ========================== MAIN FUNCTION ================================= #
 # ======================================================================= #
if __name__ == "__main__":
    import sys
    import xgboost as xgb
    from xgboost import XGBClassifier
    from asdict import read_as_dict
    from sklearn.model_selection import train_test_split

    if len(sys.argv) != 3:
        print("Usage: {} {} {}".format(sys.argv[0], "training_dataset", "training_config"))
        exit(-1)
    #
    dataset = sys.argv[1]
    
    ## Load data
    # Load the training data 
    inpath = '/home/kpapad/UG_thesis/Thesis/share/SimuData/'
    sig_filename = inpath+ "{}_SIG_Train.root".format(dataset)
    bkg_filename = inpath+ "{}_BKG_Train.root".format(dataset)
    x, y, w, num_all= load_data(sig_filename, bkg_filename)
    
    # Load training config
    config_dir="/home/kpapad/UG_thesis/Thesis/Bdt/config/"
    training_config = config_dir + sys.argv[2]
    print("loading training configuration: {}".format(training_config))
    training_config = read_as_dict(training_config)
    
    ## Fit xgboost model
    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.20, random_state=0)
    
    # Create the list for validation set
    dval = [(X_val, y_val)]
    print('Training started with data from {} and {}'.format(sig_filename, bkg_filename)) 
    bdt = XGBClassifier(**training_config)
    bdt.fit(X_train, y_train, eval_set=dval, verbose=True)
    
    ## Calculate feature importance
    # create again the variable names 
    variables = make_variable_names(dataset, dataset) 
    feat_imp=bdt.feature_importances_
    make_bar_graph(variables, feat_imp)
    
    # Save model in TMVA format
    outpath = '/home/kpapad/UG_thesis/Thesis/Bdt/out/Models/'
    modelname = sys.argv[2][13:-5]
    modelFile = outpath +"myModel{}_conf{}.root".format(dataset, modelname)
    #
    print('Training, done')
    print('Saving model at {}'.format(modelFile))
    #
    ROOT.TMVA.Experimental.SaveXGBoost(bdt,"myBDT", modelFile ,  num_inputs=num_all)
    print('done')
    
    
