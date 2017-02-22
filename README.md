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

* Use `Open Archive` and `Open Directory` buttons to open a data set 
for visualization

* `Open Directory` button allows you to select a directory where a dataset is located.
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
    ├── uber.hg19.GL9.2.20k.seg.quantal.R.seg.txt
    └── pathology
        ├── 9727420.color.map.060414.png
        ├── COR003.GS9.2.Area1.Benign.jpg
        ├── COR003.GS9.2.Area1.Benign.txt
        ├── COR003.GS9.2.Area2.PIN.with.Benign.jpg
        ├── COR003.GS9.2.Area2.PIN.with.Benign.txt
        ├── COR003.GS9.2.Area3.GS9.invading.SV.jpg
        ├── COR003.GS9.2.Area3.GS9.invading.SV.txt
        ├── COR003.GS9.2.Area4.GS9.near.Urethra.jpg
        ├── COR003.GS9.2.Area4.GS9.near.Urethra.txt
        ├── COR003.GS9.2.Area5.GS9.at.Capsule.jpg
        ├── COR003.GS9.2.Area5.GS9.at.Capsule.txt
        └── description.csv

    ```
Optionally the dataset directory can contain a `pathology` subdirectory that
contains pathology images and notes. This subdirectory should contain 
`description.csv` with following structure:

    ```
    sector,pathology,image,notes
    1,Benign prostatic tissue,COR003.GS9.2.Area1.Benign.jpg,COR003.GS9.2.Area1.Benign.txt
    2,Pin and benign prostate,COR003.GS9.2.Area2.PIN.with.Benign.jpg,COR003.GS9.2.Area2.PIN.with.Benign.txt
    3,Gleason 9 and invading seminal vesicle,COR003.GS9.2.Area3.GS9.invading.SV.jpg,COR003.GS9.2.Area3.GS9.invading.SV.txt
    4,Gleason 9 near urethra,COR003.GS9.2.Area4.GS9.near.Urethra.jpg,COR003.GS9.2.Area4.GS9.near.Urethra.txt
    5,Gleason 9 at capsule,COR003.GS9.2.Area5.GS9.at.Capsule.jpg,COR003.GS9.2.Area5.GS9.at.Capsule.txt
    ```
First column in `description.txt` contains the name/id of the sector as in `guide` file, 
the second column is a description of the sector and the last two columns contain
file names of pathology image and notes.

* `Open Archive` button allow you to select dataset stored as a `ZIP` archive. Files from the
dataset should follow the same naming convention as for dataset directories.
For example the dataset archive from the previous example should contain following 
files:

    ```
    unzip -t GL9.2.zip 
    Archive:  GL9.2.zip
        testing: pathology/               OK
        testing: pathology/description.csv   OK
        testing: pathology/COR003.GS9.2.Area4.GS9.near.Urethra.jpg   OK
        testing: pathology/COR003.GS9.2.Area3.GS9.invading.SV.jpg   OK
        testing: pathology/COR003.GS9.2.Area2.PIN.with.Benign.jpg   OK
        testing: pathology/COR003.GS9.2.Area1.Benign.txt   OK
        testing: pathology/COR003.GS9.2.Area5.GS9.at.Capsule.txt   OK
        testing: pathology/COR003.GS9.2.Area4.GS9.near.Urethra.txt   OK
        testing: pathology/COR003.GS9.2.Area3.GS9.invading.SV.txt   OK
        testing: pathology/COR003.GS9.2.Area2.PIN.with.Benign.txt   OK
        testing: pathology/COR003.GS9.2.Area5.GS9.at.Capsule.jpg   OK
        testing: pathology/COR003.GS9.2.Area1.Benign.jpg   OK
        testing: pathology/9727420.color.map.060414.png   OK
        testing: GL9.2smear1bpFisherPcloneTracks.clone.txt   OK
        testing: GL9.2smear1bpFisherTreePyP.tree.txt   OK
        testing: GL9.2smear1bpPinMat.pinmat.txt   OK
        testing: GL9.2smear1bpPins.pins.txt   OK
        testing: joan02.guide06172016.guide.txt   OK
        testing: uber.hg19.GL9.2.20k.lowratio.quantal.R.ratio.csv   OK
        testing: uber.hg19.GL9.2.20k.seg.quantal.R.seg.txt   OK
    No errors detected in compressed data of GL9.2.zip.
    ```
    
