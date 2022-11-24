#  Prerequired
>1. VMWare 15
>2. Ubuntu 18
>3. USB with Data
>4. register nvidia developer account
***
# Part Jetson OS
### install Nvidia SDK Manger for install New Jetpack OS with CUDA
1. install `Ubuntu 18 only` (ubuntu-18.04.6-desktop-amd64.iso) (storage 80 GB or more) on `VMWare 15 only`
2. Login & Download SDK Manager from https://developer.nvidia.com/embedded/downloads
3. select Flash `Jetpack 4.6.2` OS
<!-- 4. select check box Jetson OS
5. do not select check box Jetson SDK Components before build `Opencv 4.5.3` (Part Build OpenCV) -->
4. select automatic setup + runtime option on 3rd step in SDK Manager<br>
### test connection
>`$ ssh jetson@<jetson-ip>`<br>
password for jetson: yahboom
***
# Part PIP 3
### install pip3 for python 3.6.9
>`$ wget https://bootstrap.pypa.io/pip/3.6/get-pip.py`<br>
`$ sudo python3 get-pip.py`
***
## (Optional) Part Monitoring
### install monitoring tool
>`$ sudo apt -y update`<br>
`$ sudo -H pip3 install -U jetson-stats`<br>
`$ sudo systemctl restart jetson_stats.service`<br>
`$ sudo jtop`
***
# Part Build OpenCV
### Before Build OpenCV, jetson nano has 38% disk usage (case do not install Jetson SDK Components)
### Delete OpenCV 4.1.1 that comes with Jetpack 4.6.2
>`$ sudo apt-get purge *libopencv*` <br>
### build opencv
>`$ git clone https://github.com/wanarut-bda/buildOpenCV.git` <br>
`$ cd buildOpenCV` <br>
`$ sudo ./buildOpenCV.sh |& tee openCV_build.log`
## take time about 5 hours

### check build Information
`$ python3` <br>
>`import cv2` <br>
`print(cv2.getBuildInformation())`
### Version control:      4.5.3-dirty
### GStreamer:            YES (1.14.5)
### After Build OpenCV, jetson nano has 51% disk usage
### delete opencv folder (1.9 GB)
>`$ sudo rm -rf opencv*`

### After Delete opencv folder, jetson nano has 39% disk usage
***
# Part Clear Space
### After install All SDK, jetson nano has 84% disk usage (case install Jetson SDK Components)

### clear for free space
>`$ sudo apt remove -y libreoffice* thunderbird*` <br>
`$ sudo apt-get -y autoremove` <br>
`$ sudo apt-get clean`

### reduce disk usage to 80%
<!-- # Part Jetson SDK Components
1. do not check Jetson OS
2. check Jetson SDK Components after build Opencv 4.5.3 (Part Build OpenCV)
3. select automatic setup + runtime option on 3rd step in SDK Manager
### After install Jetson SDK Components, jetson nano has 90% disk usage -->
### check cuda version
>`$ nvcc -V`
***
# Part Install OCR Module
## NOTE** if use `easyocr` do not install `paddleocr`

## easyocr installation
### install pytorch (native style)
### ref: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
>`$ wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl` <br>
`$ sudo apt-get install python3-pip libopenblas-base libopenmpi-dev libomp-dev` <br>
`$ sudo -H pip3 install Cython` <br>
`$ sudo -H pip3 install numpy torch-1.10.0-cp36-cp36m-linux_aarch64.whl`
## take time about 10 minutes
>`$ sudo -H pip3 install torchvision` <br>
`$ sudo -H pip3 install easyocr` <br>
`$ sudo -H pip3 uninstall opencv-python-headless`
## take time about 2 hours

## test project modules
`$ OPENBLAS_CORETYPE=ARMV8 python3` <br>
>`import easyocr` <br>
`import cv2` <br>
`cv2.__version__` <br>
`tracker = cv2.TrackerCSRT_create()` <br>
***
## or install pytorch via docker
>- JetPack 4.6.1 (L4T R32.7.1) <br>
>- l4t-pytorch:r32.7.1-pth1.9-py3 <br>
>- PyTorch v1.9.0 <br>
>- torchvision v0.10.0 <br>
>- torchaudio v0.9.0 <br>
### ref https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch
>`$ sudo docker pull nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3` <br>
`$ sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3` <br>

### You should then be able to start a Python3 interpreter and import torch and import torchvision.
***

## (Optional) install paddleocr
### install dependencies
>`$ sudo apt-get install cmake wget` <br>
`$ sudo apt-get install libatlas-base-dev libopenblas-dev libblas-dev` <br>
`$ sudo apt-get install liblapack-dev patchelf gfortran` <br>
>`$ sudo -H pip3 install Cython` <br>
`$ sudo -H pip3 install -U python3-setuptools` <br>
`$ sudo -H pip3 install six requests wheel pyyaml` <br>
### upgrade version 3.0.0 -> 3.13.0
>`$ sudo -H pip3 install -U protobuf` <br>
### download the wheel
>`$ wget https://paddle-wheel.bj.bcebos.com/kunlun/paddlepaddle-2.0.2-cp37-cp37m-linux_aarch64.whl` <br>
### install Paddle
>`$ sudo -H pip3 install paddlepaddle-2.0.0-cp37-cp37m-linux_aarch64.whl`
### clean up
>`$ rm paddlepaddle-2.0.0-cp37-cp37m-linux_aarch64.whl`
***
## (Optional) Part Install VNC
>`$ sudo apt update` <br>
`$ sudo apt install vino` <br>
`$ mkdir -p ~/.config/autostart` <br>
`$ cp /usr/share/applications/vino-server.desktop ~/.config/autostart` <br>
`$ gsettings set org.gnome.Vino prompt-enabled false` <br>
`$ gsettings set org.gnome.Vino require-encryption false` <br>
`$ gsettings set org.gnome.Vino authentication-methods "['vnc']"` <br>
`$ gsettings set org.gnome.Vino vnc-password $(echo -n 'aabbccddee'|base64)` <br>
`$ sudo reboot`
***
## (Optional) Part Python 3.9 ------------------
### Upgrade to python 3.9
>`$ sudo add-apt-repository ppa:deadsnakes/ppa` <br>
`$ sudo apt-get update` <br>
`$ sudo apt-get install python3.9` <br>
`$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1` <br>
`$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2` <br>
`$ sudo update-alternatives --config python3`
## select number 2
>`$ python3 -V`
***