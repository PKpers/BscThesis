#!/usr/bin/python
def rand_data(s, n):
    '''
    returns n numbers, n1, n2, ... such that n1+n2+...=s
    '''
    import random as rand
    nums = [rand.randint(-100, 100) for i in range(n-1)]
    nums.append(s - sum(nums))
    return nums
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
        outpath = "/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/RFiles/"
        fileName = settings["Type"]
    else:
        output_settings = [settings[key] for key in settings.keys() if 'output' in key or 'Output' in key][0]
        outpath, fileName =  output_settings
    #
    outfiles = [
        ('{}{}{}.root'.format(outpath, fileName+str(1), p),
         '{}{}{}.root'.format(outpath, fileName+str(2), p))
        for p in purpose
    ]
    return outpath, outfiles
#
def generate_input(_type, settings, num_data):
    '''
    initiates the variables needed to generate training and testing data
    '''
    if _type == "fixed":
        sum_a, sum_b = settings["Args"]
        return sum_a, sum_b
    elif _type == "rand":
        sum_a, sum_b = [ rand.randint(0, 10) for i in range(num_data) ]
        return sum_a, sum_b
    elif _type == "dist":
        mu_a, mu_b, sigma = settings["Args"]
        return mu_a, mu_b, sigma
    #
def generate_data(_type, settings, num_sets, num_data, n):
    '''
    generates training and testing data
    '''
    data= []
    if _type == "fixed" or _type == "rand":
        # in fixed and rand scenarios the sum of each element in a group are the same 
        sum_a, sum_b = generate_input(_type, settings, num_data)
        for i in range(num_data):
            # rand_data() creates one set. The number of sets we create is num_sets
            # We create num_sets for each group.
            # We do it twice. Once to create testing data and once to create training data
            #
            a = np.array(
                [rand_data(sum_a, n) for i in range(num_sets)],
                dtype="float32").T
            #
            b = np.array(
                [rand_data(sum_b, n) for i in range(num_sets)],
                dtype="float32").T
            #
            data.append( (a,b) )
        #
        return data
#        
    elif _type == "dist":
        mu_a, mu_b, sigma = generate_input(_type, settings, num_data)
        for i in range(num_data):
            a = np.array(
                [rand_data(rand.gauss(mu_a, sigma), n) for i in range(num_sets)],
                dtype="float32").T
            #
            b = np.array(
                [rand_data(rand.gauss(mu_b, sigma), n) for i in range(num_sets)],
                dtype="float32").T
            #
            data.append( (a,b) )
        return data
# 
if __name__== "__main__" :
    import numpy as np
    import ROOT
    import random as rand
    from asdict import read_as_dict
    # Load settings
    settings_file = "/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/config/GenData.dict"
    settings = read_as_dict(settings_file)
    if 'Output' or 'output' not in settings:
        _type = 'default'
    else:
        _type = 'custom'
    #
    outpath, outfiles = create_fnames(_type, settings)
    #    
    # n: number of elements in each event
    # num_data: testing and training data
    # num_sets: number of events in each groop
    n, num_data, num_events = settings['General']
    #
    _type = settings["Type"]
    # Generate data
    data = generate_data(_type, settings, num_events, num_data, n)
    #store the tuples of group a and b in to different root  files 
    treeName ='myTree'
    branch_names = ['var_{}'.format(num) for num in range(n)]
    #
    for j, File in enumerate(outfiles):
        nums = data[j]
        for i in range(num_data):
            print('Writting {} in {}'.format(treeName,File[i]))
            #
            vars_dict=define_columns(n, branch_names, nums[i])
            df = ROOT.RDF.MakeNumpyDataFrame(vars_dict)
            df.Define(
                "sum",
                "var_0\
                +var_1\
                +var_2\
                +var_3"
            ).Snapshot(treeName, File[i])
            print('done')
            #
        #
    #
#
