# Build dependencies for the required packages
apt install gcc g++ make cmake build-essential -y

# Install Python 3.11 and create a virtual environment
apt install python3.11 python3.11-venv -y

# Create a virtual environment & install dependencies
cd /root/medbot
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt