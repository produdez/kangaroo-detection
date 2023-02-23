# Environment Setups

## Note

Experiments are done on window laptop with GTX 1060.

## Quick start

Duplicate my environment with `conda` using environment config (`.yml` files)

```[bash]
    conda env create -f <config-filename>.yml
```

- `base-env.yml`: bare bone environment that can use GPU computation
- `full-env.yml`: full environment used in this project

## Self replicate

If you wanna install everything yourself. Follow instructions below

### Important packages

For GPU computation and basic needs

`Our environment will be named 'kangaroo'`

1. Python: 3.8

   ```[bash]
   conda create -n kangaroo python=3.8
   ```

2. Activate: `conda activate kangaroo`
3. Check python version

    ```[bash]
    python --version
    > Python 3.8.15
    ```

4. ⭐ Tensorflow-GPU:

    ```[bash]
    conda install tensorflow-gpu==2.5.0
    ```

    > (2.3.0) does not work !! at all
    > This install also included numpy (and keras)

5. (Extra) Install `cuda-nvcc` (Reference errors and fixes)

   ```[bash]
    conda install -c nvidia cuda-nvcc
   ```

6. (Optional) Check and sync/downgrade `tensorflow-base` version
   To match with tensorflow version

   ```[bash]
   conda install tensorflow-base==2.5.0
   ```

7. Verify installation packages recognizes your GPU

   ```[bash]
    python src/scripts/verify_gpu.py 
   ```

8. Continue install all other packages
9.  Clone submodule and install Mask-RCNN

   ```[bash]
    # clone
    git submodule init
    git submodule update

    # install
    cd src/submodules/akTwelve_MaskRCNN
    python setup.py install
   ```

### Other packages

Exception:

   1. `Mask_RCNN`: [Link](https://github.com/jbrownlee/Mask_RCNN)

Other used packages:

```[bash]
  conda install -c conda-forge [packages]
```

   1. `Pillow`: Image loading/processing (also the base of `Keras` Image)
   2. `scikit-image`: (**!** version: `0.16.2`)
   3. `ipykernel`
   4. `pycocotools`: Needed for training on windows (`pip`)
   5. `dvc`
   6. `imgaug`: image augmentation frame work used by MRCNN training method
   7. `imageio`: helper image reading lib
   8. `pandas`: data frame manipulation (test related purposes)

### Errors and Fixes

- Error: When installing `pycocotools`: Missing C++ stuffs
  - Suggested fix: Install C++ Build Tool 2015

- Pitfall: Wrong installation of build tools / installation with mismatching C++/SDK version / missing components
  - Fix: Install Dev package for C++ with win 10 SDK ([Reference](https://stackoverflow.com/questions/67940561/troubleshooting-pycocotools-installation))
  - Specifications: Exported to [.vsconfig](../docs/.vsconfig)
- Error: `module 'keras.engine' has no attribute 'Layer'`
  - Discussion: [Link](https://github.com/matterport/Mask_RCNN/issues/2783)
  - Fix: Use this [Repo](https://github.com/akTwelve/Mask_RCNN) and make sure to install `pycocotools` 

- Keras conflict with `scikit-image` in RCNN code
  - Error output: `Input image dtype is bool. Interpolation is not defined with bool data type`
  - Ref/Suggestions: [here](https://github.com/matterport/Mask_RCNN/issues/2243)
  - Resolve: down grade `scikit-image` from `0.19.3` to `0.16.2`
  - Note: but don't just downgrade it, force uninstall/reinstall with
    - `conda install ... --force-reinstall`
    - Or `pip install -U ...`

- Getting stuck with Error `No module named 'tensorflow_core.estimator'`
  - Reasons/Discussion: [here](https://stackoverflow.com/questions/66022256/modulenotfounderror-no-module-named-tensorflow-core-estimator-for-tensorflow)
  - Resolve: downgrade tensorflow-estimator to same version as tensorflow
- Tensorflow 2.1 conflict with `h5py`
  - [Ref](https://github.com/tensorflow/tensorflow/issues/44467)
  - [Solve](https://stackoverflow.com/questions/53740577/does-any-one-got-attributeerror-str-object-has-no-attribute-decode-whi): use `h5py` ver 2.10.0
- Warining: `Internal: Failed to launch ptxas`
  - Fix by installing `cuda-nvcc`
  - This warning comes after an error: `Call to CreateProcess failed. Error code: 2`
  - Reference: [Link](https://stackoverflow.com/questions/66623541/tensorflow-2-4-1-couldnt-invoke-ptxas-exe)

# Other versions tested

**1:**

- python 3.7
- tensorflow-gpu 2.1.0
