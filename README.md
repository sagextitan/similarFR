# Installation Steps:

Note: Make sure to install python on your device through Homebrew (if using Mac)

1. Clone the repository: `git clone https://github.com/sagextitan/similarFR.git`

2. Setting up Python environment to execute python files and install the packages :

```python

# For creating and activating the virtual environment provided by Python for running commands

python3 -m venv venv
source venv/bin/activate

# For installing the packages

pip install -r requirements.txt

```

3. To start the server:

```bash

# After running this command you will get a url for starting the project on your local terminal that goes by this: http://127.0.0.1:5000


python3 app.py

```

4. If you want some new images to be added to local collection so that the API can process selfie and collect all similar images, add them to the `AllImages` folder and run this command so that on selfie submission the new images can be included if similarity is found:

```python

# This will create a new file `encoded_faces.npy` having details of all the faces. If there already exists a file then one can remove it and then run the above command

python3 preprocess_and_encode.py


```

[Do restart the server on which the application is running]
