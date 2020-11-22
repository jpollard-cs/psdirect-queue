# psdirect-queue
I offer no support or anything related to this script. May have more success if you browse YouTube or something a little bit in the browser that opens initially.

# Installation
From PowerShell:

# Setup
```bash
git clone https://github.com/ima9rd/psdirect-queue.git  
cd psdirect-queue  
bash script_setup.sh
bash bootstrap.sh
```

# Running PS Direct Queue
```bash
bash activate_pyenv.sh
python3 app.py
```

# Setting up Microsoft Checkout
- you need to first get the item in your cart while logged into your microsoft account - fortunately there seem to be many opportunities for this
- copy the `config\microsoft_config_template.json` to `config\microsoft_config.json` and provide your own info (same account associated with your cart)

# Running Microsoft Checkout
```bash
bash activate_pyenv.sh
python3 microsoft.py
```

If you encounter errors such as `No module named win32com.client, No module named win32, or No module named win32api`, you will need to install `pypiwin32`:
```bash
pip3 install pypiwin32
```