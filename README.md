## Anaconda Environment Setup (python 2.7)

* Go to anaconda web site 
[https://www.continuum.io/downloads](https://www.continuum.io/downloads)
and download the latest anaconda installer for your operating system. The following
instructions use *Python 2.7* so you need to install appropriate version 
of Anaconda. 

* Install anaconda into suitable place on your local machine following
instruction from 
[https://docs.continuum.io/anaconda/install](https://docs.continuum.io/anaconda/install)

## Create cnviewer anaconda environment from scratch

* After installing Anacond you need to create an environment to use with the viewer:

    ```
    conda create -n aviewer
    source activate aviewer
    conda install numpy scipy matplotlib pillow pandas
    ```

## Activate the viewer environment

* To activate the anaconda environment `cnviewer` you need to use the appropriate
anconda instructions to 
[activate an environment](http://conda.pydata.org/docs/using/envs.html#change-environments-activate-deactivate). 
For `Linux` and `OS X` you should
use:

    ```bash
    source activate aviewer
    ```
On `Windows` you need to use:
    ```bash
    activate aviewer
    ```

* Full instructions on how ot use and manage anaconda environments can be found
here: [http://conda.pydata.org/docs/using/envs.html](http://conda.pydata.org/docs/using/envs.html)


## Start the Viewer
* Before starting the viewer you need to activate viewer Anaconda environment
    ```
    source activate aviewer
    ```

* To start the viewer go to `cnviewer` directory and start `tkmain.py`

    ```bash
    cd cnviewer/cnviewer
    python tkmain.py
    ```

## Select Dataset

* Use `OA` (open archive) and `OD` (open directory) buttons to open a data set 
for visualization

* `OD` button allows you to select a directory where a dataset is located.
One directory may contain only one dataset.

* Files in the dataset should conform to the following naming convention. Each filename
should end with two dot separated words. The last word is the usual file extension
and second to last is the file type. For example:

    ```
    GL9.2smear1bpPinMat.pinmat.txt
    ```
is a `txt` file, that contains `pinmat` used by the viewer. Example full dataset
should be named in following way:

    ```
    .
    ├── GL9.2smear1bpFisherPcloneTracks.clone.txt
    ├── GL9.2smear1bpFisherTreePyP.tree.txt
    ├── GL9.2smear1bpPinMat.pinmat.txt
    ├── GL9.2smear1bpPins.pins.txt
    ├── joan02.guide06172016.guide.txt
    ├── uber.hg19.GL9.2.20k.lowratio.quantal.R.ratio.txt
    └── uber.hg19.GL9.2.20k.seg.quantal.R.seg.txt
    ```

* `OA` button allow you to select dataset stored as a `ZIP` archive. Files from the
dataset should follow the same naming convention as for dataset directories.
For example the dataset archive from the previous example should contain following 
files:

    ```
    unzip -t GL9.2.zip 
    Archive:  GL9.2.zip
        testing: GL9.2smear1bpFisherPcloneTracks.clone.txt   OK
        testing: GL9.2smear1bpFisherTreePyP.tree.txt   OK
        testing: GL9.2smear1bpPinMat.pinmat.txt   OK
        testing: GL9.2smear1bpPins.pins.txt   OK
        testing: joan02.guide06172016.guide.txt   OK
        testing: uber.hg19.GL9.2.20k.lowratio.quantal.R.ratio.txt   OK
        testing: uber.hg19.GL9.2.20k.seg.quantal.R.seg.txt   OK
    No errors detected in compressed data of GL9.2.zip.
    ```
    
