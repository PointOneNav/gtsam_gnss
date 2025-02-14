# gtsam_gnss
This repository is a small set of custom factors and MATLAB wrappers that use [GTSAM](https://github.com/borglab/gtsam) for GNSS processing.

<u>This repository is currently under development</u>, so we will gradually add content.

## Updates
### February 13, 2025
[The preprint of the paper](https://arxiv.org/abs/2502.08158) has been uploaded. Examples in the paper are now available. Also, examples of the use of `CarrierPhaseFactor_XB` to estimate carrier phase integer ambiguity have been added.

# Test environments
- Ubuntu 22.04 / Windows 11 /macOS
- MATLAB 2024a

# Build on Ubuntu 22.04
## GTSAM
- [GTSAM](https://github.com/borglab/gtsam):
Factor graph optimization library. Due to a problem with the MATLAB wrapper, please clone [GTSAM from my repository](https://github.com/taroz/gtsam-4.3a) instead of the original GTSAM and build it using the following procedure.
```shell
sudo apt-get install -y git build-essential cmake libboost-all-dev libtbb-dev python3-pip
pip install pyparsing
git clone https://github.com/taroz/gtsam-4.3a.git
cd gtsam-4.3a
mkdir build && cd build
cmake .. -DGTSAM_BUILD_UNSTABLE=OFF -DGTSAM_BUILD_EXAMPLES_ALWAYS=OFF -DGTSAM_BUILD_TESTS=OFF -DGTSAM_INSTALL_MATLAB_TOOLBOX=ON
make -j$(nproc)
sudo make install
```
`gtsam_toolbox` is installed in `/usr/local/`

### Enabling Python Support

To use `gtsam_gnss` with Python, you must enable GTSAM Python support by adding the following `cmake` arguments:
```
-DGTSAM_BUILD_PYTHON=ON -DGTSAM_PYTHON_VERSION=3.10
```
replacing 3.10 with the Python version you intend to use. If you wish to use GTSAM within a Python virtual
environment, activate the virtual environment before building GTSAM.

## gtsam_gnss
```shell
git clone https://github.com/taroz/gtsam_gnss.git
cd gtsam_gnss
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```
By default, `gtsam_gnss` is installed in `user/local/gtsam_toolbox`.
Add `user/local/gtsam_toolbox` to your MATLAB search path.

### Enabling Python Support

By default, the `gtsam_gnss` build will generate MATLAB wrappers. To generate Python wrappers, make sure GTSAM is built
with Python support above, and then specify the following `cmake` argument when building `gtsam_gnss`:
```
-DGTSAM_GNSS_BUILD_PYTHON=ON
```

After `make` completes, you can install the Python bindings with:
```
make python-install
```

As with building GTSAM, if you wish to use `gtsam_gnss` within a Python  virtual environment, activate the virtual
environment before building GTSAM.

Once installed, you can import `gtsam_gnss` in Python as follows:
```python
import gtsam
import gtsam_gnss
import numpy as np
factor = gtsam_gnss.DopplerFactor_V(
    keyV=1,
    losvec=gtsam.Point3(1, 0, 0),
    prr=3,
    iniv=gtsam.Point3(0, 2, 0),
    model=gtsam.noiseModel.Diagonal.Sigmas(np.array((5,))))
```

### Disabling MATLAB Support

If you are building only for Python and wish to disable the MATLAB wrapper compilation, set the following `cmake`
argument:
```
-DGTSAM_GNSS_BUILD_MATLAB=OFF
```

# Build on Windows 11
Building GTSAM and gtsam_gnss on Windows is a little complicated. The procedure is shown [here](./BUILD_WINDOWS.md).

# Build on macOS
The procedure for building GTSAM and gtsam_gnss on macOS is shown [here](./BUILD_macOS.md).

# Examples
- See [examples](./examples) directory
- Use in the Google Smartphone Decimeter Challenge. See [gsdc2023](https://github.com/taroz/gsdc2023) repository

# Citation
The preprint version is [here](https://arxiv.org/abs/2502.08158).
```
T. Suzuki, "Open-Source Factor Graph Optimization Package for GNSS: Examples and Applications," 2025 IEEE/ION Position, Location and Navigation Symposium (PLANS), (accepted)
```
