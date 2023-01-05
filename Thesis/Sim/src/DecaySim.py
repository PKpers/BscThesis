def RandomSampleSphere(dim, radius, num_points):
    '''
    draws numPoints random samples uniformly distributed
    at the surface of a sphere
    # At first n pairs of gaussian distributed numbers are generated.
        n = num_points and the length of the pairs is defined by the dimention dim of the sphere
    # Then the norm of those pairs is calculated.
       If the norm is 0 in any of the pairs those pairs are removed
    # After that an intermediate sptep needs to be taken so that the list
       which contains the norms of each pair, to have a form suitable
       for the division of each number inside a given pair with the norm
    # Finally, each point in a given pair is divided by the norm of the said pair
       and is multiplied by the radius of the sphere in questons
    # in this form, each pair represents, a vector whose start is at 0
       and its end in the surface of the sphere. Those vectors are know uniformly distributed
       at the surface of our sphere.
    '''
    import numpy as np
    x = np.random.normal(0,1,(num_points,dim))#generate the random(gaussian) pairs
    z = np.linalg.norm(x, axis=1) #calculate the norm of the random pairs
    if (z==0).any(): #kick out any pair whose norm = 0 also remove the respectable norms
        i = np.where(z==0)
        x = np.delete(x,i)
        z = np.delete(z, i)
    #
    z = z.reshape(-1,1).repeat(x.shape[1], axis=1)# z has the following form [ [norm_0, norm_0, ..., norm_0], ... ] 

    Points = x/z * radius 
    return Points

def to_pep(vec):
    '''
    Helper function 
    conver a vector from whatever coordinates
    to the PtEtaPhi system

    The imput vecot must be a 4vector
    '''
    from ROOT import TLorentzVector
    import numpy as np
    vec = TLorentzVector(vec)
    Pt = vec.Perp()
    Eta = vec.Eta()
    Phi = vec.Phi()
    vec_in_pep = np.array([Pt, Eta, Phi])
    return vec_in_pep

def to_cart(vec):
    '''
    Helper function
    convert a vector from whatever coordinates
    to the cartesian coordinate system

    the imput vetor must be a 4 vector
    '''
    from ROOT import TLorentzVector
    import numpy as np
    vec = TLorentzVector(vec)
    Px = vec.Px()
    Py = vec.Py()
    Pz = vec.Pz()
    vec_in_cart = np.array([Px, Py, Pz])
    return vec_in_cart

def rest_decay_to_massless(parrent_mass, num_decays, coord):
    '''
    Simulating the decay(s) of a particle at rest to two photons
    # We model decays in the 3 dimentional space
    # when a particle at rest of mass M decays to two photons
       each photon has momentum of magnitude P=M/2
    # coord: the coordinate system to use for output
    # pi_vectors, i = 1, 2: momenta of the photons
    '''
    import numpy as np
    import ROOT
    dim = 3
    momentum_mag = parrent_mass/2 
    p1_vectors = RandomSampleSphere(dim, momentum_mag, num_decays)
    p2_vectors = -p1_vectors  #momentum vector of the second photons.  
    p_vectors = np.hstack((p1_vectors, p2_vectors)) #the
    # Convert to the coorect coordinates
    if 'PxPyPz' not in coord:
        l = p1_vectors.shape[0]
        p1_events, p2_events = ([], [])
        for i in range(l):
            photon1 = ROOT.TLorentzVector(np.append(p1_vectors[i], parrent_mass/2))
            photon2 = ROOT.TLorentzVector(np.append(p2_vectors[i], parrent_mass/2))
            photon1 = to_pep(photon1)
            photon2 = to_pep(photon2)
            p1_events.append(photon1)
            p2_events.append(photon2)
        #
        p1_events = np.array(p1_events)
        p2_events = np.array(p2_events)
        p_vectors = np.hstack((p1_events, p2_events))
        return p_vectors
    else:
        l = p1_vectors.shape[0]
        p1_events, p2_events = ([], [])
        for i in range(l):
            photon1 = ROOT.TLorentzVector(np.append(p1_vectors[i], parrent_mass/2))
            photon2 = ROOT.TLorentzVector(np.append(p2_vectors[i], parrent_mass/2))
            photon1 = to_cart(photon1)
            photon2 = to_cart(photon2)
            p1_events.append(photon1)
            p2_events.append(photon2)
        #
        p1_events = np.array(p1_events)
        p2_events = np.array(p2_events)
        p_vectors = np.hstack((p1_events, p2_events))
        return p_vectors
    #

def define_columns(num_columns, var_names, var):
    '''
    defince the variables of data frame
    '''
    import numpy as np
    vars_ = {}
    for i in range(num_columns):
        vars_[var_names[i]] = np.array(var[i])
    #
    return vars_
#
def create_fnames(create_type, settings):
    '''
    create the output file names
    '''
    purpose = ('Test', 'Train')
    if create_type == 'defult':
        outpath = "/home/kpapad/UG_thesis/Thesis/Sim/out/Data"
        fileName = settings["Type"]
    else:
        output_settings = [settings[key] for key in settings.keys() if 'output' in key or 'Output' in key][0]
        outpath, fileName =  output_settings
    #
    outfiles = [
        ('{}{}{}.root'.format(outpath, fileName+str('_SIG_'), p),
         '{}{}{}.root'.format(outpath, fileName+str('_BKG_'), p))
        for p in purpose
    ]
    return outpath, outfiles
#--------------------------------------------------------------------------------------------------------------------------
## Main fucntion ##
#--------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    from asdict import read_as_dict
    import ROOT
    ## Load settings
    settings_file = "/home/kpapad/UG_thesis/Thesis/Sim/config/config.dict"
    settings = read_as_dict(settings_file)
    if not ("Output" or 'output') in settings:
        _type = 'default'
    else:
        _type = 'custom'
    #
    outpath, outfiles = create_fnames(_type, settings)
    Files = []
    for f in outfiles:
        Files.append(f[0])
        Files.append(f[1])
    #
    #print(outfiles)
    ## Inintial configuration
    sig_pmass, bkg_pmass = settings["decay_params"] #Load the parent masses for sig and bkg
    num_events, coordinates= settings['general']#number of events to generate and coordinate system
    ## Generate the events  
    sig_events_test = rest_decay_to_massless(sig_pmass, num_events, coordinates)
    bkg_events_test = rest_decay_to_massless(bkg_pmass, num_events, coordinates)
    sig_events_train = rest_decay_to_massless(sig_pmass, num_events, coordinates)
    bkg_events_train = rest_decay_to_massless(bkg_pmass, num_events, coordinates)
    events = (
        sig_events_test,
        bkg_events_test,
        sig_events_train,
        bkg_events_train
    )
    #
    # write the output
    treeName = 'myTree'
    if coordinates == 'PtEtaPhi':
        b_n = [
            ['Pt{}'.format(i+1), 'Eta{}'.format(i+1), 'Phi{}'.format(i+1)]
            for i in range(2)
        ]
        branch_names = b_n[0] + b_n[1]
        #print(branch_names)
    elif coordinates == 'PxPyPz':
        b_n = [
            ['Px{}'.format(i+1), 'Py{}'.format(i+1), 'Pz{}'.format(i+1)]
            for i in range(2)
        ]
        branch_names = b_n[0] + b_n[1]
    #
    for i in range(len(events)):
        photons = events[i].T
        print('Writting {} in {}'.format(treeName, Files[i]))
        vars_dict = define_columns(6, branch_names, photons)
        df = ROOT.RDF.MakeNumpyDataFrame(vars_dict).Snapshot(treeName, Files[i])
