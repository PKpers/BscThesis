
# Table of Contents

1.  [Directories and names](#org6793c52)
    1.  [Tutorial material and scripts](#orgf0b7de0)
    2.  [Thesis](#org20cd2b6)
        1.  [File structure](#orgfb6b89e)

This is the place where I will be developing my thesis.


<a id="org6793c52"></a>

# Directories and names

-   Rfiles stands for root files. Most probably I will not be using directories solely for storing root files anymore.


<a id="orgf0b7de0"></a>

## Tutorial material and scripts

-   tutorial<sub>material</sub> contains any kind of material which I found or I believe I will find useful.
-   tutorial<sub>scripts</sub> contains all the code I wrote while I was learning how to use the basic tools such as xgb boost and root.


<a id="org20cd2b6"></a>

## Thesis

The directory where my thesis is being developed.


<a id="orgfb6b89e"></a>

### File structure

The two main directories are the "Sim/" which contains the code for the Monte Carlo and "Bdt/" which contains the code for analyzing the Monte Carlo samples.  The two directories communicate via the "Share/" directory.  

1.  Sim/

    -   config/ directory contains the configuration file(s) used to configure the parameters of the simulation, such as sample size, coordinates system etc.
    -   src/ contains the source code for Creating the simulation and for visualizing the results. One can run the code from this directory.
    -   out/ The output from the source code goes to out/. This can be either root files containing the Monte Carlo sample or plots. The simulated sample goes to Sim/Data/ directory.
    
    1.  Simulation names
    
        The generated data output files are named in a way that by reading them, one should know the Signal and Background mass the sample size, whether the file contains Signal data or background data and finally whether is the file going to be used for testing or training.
        
        -   SXB: S stands for signal and B for background, thus SXB means that the file under question contains data where the signal mass is x and the background mass is y. in case of decimal points, those can be specified with the lowercase p. eg 4.5 = 4p5
        -   rest/moving/mixZ: rest/moving/mix denoted whether the parent particles were moving, or at rest. Mix denotes that the simulation contains a mix of particles at rest and moving. Z denoted the sample size. xK is x\*10<sup>3</sup> xM is 10<sup>6</sup> and so on. The default sample value is 100K. If the sample size is not in the name this means that the sample size is the default
        -   Coordinate system: XYZ denotes the Cartesian system. The default coordinates the Petaohm coordinates. In case the coordinate system is not present in the file name, it means that the coordinates in use are the default ones.
        -   SIG/BKG<sub>Test</sub>/Train: Denotes whether the file contains signal or background data and if it is going to be used for training or testing.

2.  Bdt/

    -   config/ directory contains the Training hyper parameter configurations files. One begins with an "initial guess" of the configuration. This initial file is numbered with a number starting from 10 and increasing. After a grid search(or any other method) one converge to the optimal configuration which is labeled with a number starting from 0. eg. training<sub>conf10</sub> -> training<sub>conf0</sub>
    -   src/ directory contains the source code used in the analysis. The concept is that the main tools, developed for the analysis are steered by the executable bash scripts located in src/exc/ directory.
    -   out/ The output of the src code is stored in the out directory. This is either models stored in root files, predilections made using the models, stored in root files or plots.
    
    All the output files are named based on the simulation they came from. 

