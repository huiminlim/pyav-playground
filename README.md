# pyav-playground

## Environments

```bash
# ffmpeg 4.4.2 needed as 6.0.0+ has broken api wrt pyav
# https://github.com/obsproject/obs-studio/issues/8375
conda create --name pyav-playground python=3.11 ffmpeg=4.4.2
conda activate pyav-playground
cd PyAV

# Install required dependencies
pip install --upgrade -r tests/requirements.txt

# Conda 3.0.0 causes problem with builds, so downgrade
# https://github.com/PyAV-Org/PyAV/issues/1177
# https://github.com/PyAV-Org/PyAV/issues/1140
pip install cython==0.29.37

# ffmpeg path: C:\Users\user\miniconda3\envs\pyav-playground\Library
python setup.py build --ffmpeg-dir=C:\Users\user\miniconda3\envs\pyav-playground\Library\bin
python setup.py install --ffmpeg-dir=C:\Users\user\miniconda3\envs\pyav-playground\Library\bin

# Install additional good to have dependencies
pip install klvdata opencv-python
```
