import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

def rest_decay_to_massless(parrent_mass, num_decays):
    '''
    Simulating the decay(s) of a particle at rest to two photons
    '''
    dim = 3# We model decays in the 3 dimentional space
    momentum_mag = parrent_mass/2 # when a particle at rest of mass M decays to two photons each photon has momentum of magnitude P=M/2
    p1_vectors = RandomSampleSphere(dim, momentum_mag, num_decays) #momentum vector of the first photons
    p2_vectors = -p1_vectors  #momentum vector of the second photons. Conservation of momentum yields that the momentum of  the second photon needs to be opposite from the first one. 
    p_vectors = np.hstack((p1_vectors, p2_vectors)) #the
    return (p1_vectors, p2_vectors)

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

if __name__=="__main__" :
    import ROOT
    parrent_mass = 10 #Gev
    test = rest_decay_to_massless(parrent_mass, 5)
    events = []
    for particle in test:
        vec = ROOT.TLorentzVector(np.append(particle, parrent_mass/2))
        vec = to_pep(vec)
        events.append(vec)
    #
    events = np.array(events)
    print(events)
    exit()


    '''
    dim, radius, num_points= (3, 4, 5000)
    points = RandomSampleSphere(dim, radius, num_points)
    x_, y_, z_ = ([], [], [])
    for p in points:
    xi, yi, zi = p
    x_.append(xi)
    y_.append(yi)
    z_.append(zi)
    #
    print('sampled {} points from the surfase of a {} dimentional sphere of radius {}'
    .format(len(x_), dim, radius))
    fig=plt.figure()
    ax=Axes3D(fig)
    ax.scatter(x_, y_, z_, s=7)
    plt.show()
'''
