## Note

Experiments are done on window laptop with GTX 1060.

### Scripts

> in `/scripts

- `verify_gpu.py`: check if gpu exists

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

1. Python: 3.7

   ```[bash]
   conda create -n kangaroo python=3.7
   ```

    > I also recommend python 3.7 for compatibility purposes (from personal experience)

2. Activate: `conda activate kangaroo`
3. Check python version

    ```[bash]
    python --version
    > Python 3.7.15
    ```

4. Ipykernel: `conda install ipykernel`
5. ⭐ Tensorflow-GPU:

    ```[bash]
    conda install tensorflow-gpu==2.1.0
    ```

    > current version as of now (2.3.0) does not work for my system
    > This install also included numpy (and keras)

6. Verify install with `/notebooks/test-gpu.ipynb`

### Other packages

Other used packages

1. `Mask_RCNN`: [Link](https://github.com/jbrownlee/Mask_RCNN)
2. `Pillow`: Image loading/processing (also the base of `Keras` Image)
3. `sk-image`: (**!** version: `0.16.2`)
4. `pycocotools`: Needed for training on windows (`pip`)

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

- Getting stuck with Error `No module named 'tensorflow_core.estimator'`
  - Reasons/Discussion: [here](https://stackoverflow.com/questions/66022256/modulenotfounderror-no-module-named-tensorflow-core-estimator-for-tensorflow)
  - Resolve: downgrade tensorflow-estimator to same version as tensorflow
- Tensorflow 2.1 conflict with `h5py`
  - [Ref](https://github.com/tensorflow/tensorflow/issues/44467)
  - [Solve](https://stackoverflow.com/questions/53740577/does-any-one-got-attributeerror-str-object-has-no-attribute-decode-whi): use `h5py` ver 2.10.0 
