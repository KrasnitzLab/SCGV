# Anaconda Environment Setup

* Go to anaconda web site 
[https://www.continuum.io/downloads](https://www.continuum.io/downloads)
and download the latest anaconda installer for your operating system. Please
note that at the moment `cnviewer` uses *Python 2.7*, so you need to install
the appropriate version of Anconda for *Python 2.7*. 

* Install anaconda into suitable place on your local machine following
instruction from 
[https://docs.continuum.io/anaconda/install](https://docs.continuum.io/anaconda/install)

* Recreate an anaconda environment suitable for work with 
`cnviewer` codebase. To this end you need to create a `cnviewer` anaconda 
environment using following command:

    ```
    cd cnviewer/deploy_tools
    conda env create -f environment.yml
    ```
This command will create an anaconda environment named `cnviewer`.

* If you already have an anaconda environment named `cnviewer` and need only to
update this environment, the appropriate commands are:

    ```
    cd cnviewer/deploy_tools
    conda env update -f environment.yml
    ```

* To activate the anaconda environment `cnviewer` you need to use the appropriate
anconda instructions to 
[activate an environment](http://conda.pydata.org/docs/using/envs.html#change-environments-activate-deactivate). 
For `Linux` and `OS X` you should
use:

    ```bash
    source activate cnviewer
    ```
On `Windows` you need to use:
    ```bash
    activate cnviewer
    ```

* Full instructions on how ot use and manage anaconda environments can be found
here: [http://conda.pydata.org/docs/using/envs.html](http://conda.pydata.org/docs/using/envs.html)
