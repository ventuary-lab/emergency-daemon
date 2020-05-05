# emergency-daemon
Emergency daemon that shuts down the Neutrino control contract when the price delta is too high

## How to run
1. ```pip3 install pywaves```
2. Fill in control contract address (oracles.sc) and the privateKey of production oracle in emdaemon.py
3. To run: ```python3 emdaemon.py``` (or use https://github.com/Unitech/pm2 for process management)
