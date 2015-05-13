# Simple Installation for Mac Os

## Python & pip

### Check the environment
```bash
which python
```
If it shows noting, run this:
```bash
brew install python
```

### Install pip
```bash
which pip
```
If it shows noting, follow one of the followings:
##### Easy install
```bash
easy_install pip
```
or
##### From source
Download get-pip.py from github (https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py)
```bash
cd /where/the/get-pip.py/is
python get-pip.py
```

### Install Virtual Environment
##### Install virtualenv
```bash
pip install virtualenv

```

### Project folder
##### Make project folder
```bash
cd /where/any/folder/you/want/
mkdir ucsc_project && cd ucsc_project
```
##### Downlaod Git
Download git client from http://git-scm.com/downloads
##### Clone the common repostitory
```bash
cd /where/any/folder/you/want/
cd ucsc_project
git clone https://github.com/SsureyMoon/Ucsc-clustering
```
##### Activate virtual environment
```bash
virtualenv ucsc_virtual_env
source ucsc_virtual_env/bin/activate
```
Now your all python library will be installed in this environment.
If you want get out from this virtual enviroment, run:
```bash
deactivate
```

### Install python libary for this project
If you are out of the virtual environment, activate it by following the step above.
Install `PyWavelets`, 'numpy`, `matplotlib`
```bash
pip install numpy
pip install PyWavelets
pip install matplotlib
```

### Run Demoe
```bash
python demo/main.py
```
You should see some graphs!

### The demo program file 'main.py' is contributed by Josue Kurl.
