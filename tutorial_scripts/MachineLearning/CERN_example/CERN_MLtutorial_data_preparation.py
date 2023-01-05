import ROOT
 
 
def filter_events(df):
    """
    Reduce initial dataset to only events which shall be used for training
    """
    return df.Filter("nElectron>=2 && nMuon>=2")
 
 
def define_variables(df):
    """
    Define the variables which shall be used for training
    """
    return df.Define("Muon_pt_1", "Muon_pt[0]")\
             .Define("Muon_pt_2", "Muon_pt[1]")\
             .Define("Electron_pt_1", "Electron_pt[0]")\
             .Define("Electron_pt_2", "Electron_pt[1]")
 
 
variables = ["Muon_pt_1", "Muon_pt_2", "Electron_pt_1", "Electron_pt_2"]
 
 
if __name__ == "__main__":
    for filename, label in [["SMHiggsToZZTo4L.root", "signal"], ["ZZTo2e2mu.root", "background"]]:
        print(">>> Extract the training and testing events for {} from the {} dataset.".format(
            label, filename))
 
        # Load dataset, filter the required events and define the training variables
        filepath = "/home/kpapad/UG_thesis/Rfiles/" + filename
        df = ROOT.RDataFrame("Events", filepath)
        df = filter_events(df)
        df = define_variables(df)
        # Book cutflow report
        report = df.Report()
        # Split dataset by event number for training and testing
        columns = ROOT.std.vector["string"](variables)

        df.Filter("event % 2 == 0", "Select events with even event number for training")\
          .Snapshot("Events", "train_" + label + ".root", columns)
        df.Filter("event % 2 == 1", "Select events with odd event number for testing")\
          .Snapshot("Events", "test_" + label + ".root", columns)
 
        # Print cutflow report
        report.Print()
