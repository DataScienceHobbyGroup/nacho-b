# Binance SDK

Python Sofware Development Kit (SDK) for interacting with [Binance Cryptocurrency Exchange][1] through API endpoints.

## Instalation
- Activate environment: `source ./venv/bin/activate`  
- Change directory: `cd ./app/binance`  
- Upgrade `builder` package: `python -m pip install --upgrade build`  
- Build package wheels: `python -m build`  
- Install packge in ***editable*** mode: `python -m pip install -e .`  

**Done!** You are now able interact with Binance.  
More infortmation on Python Project Packaging can be found [here][2].  

## Examples
    >>> from binance import Binance
    >>> binance = Binance.from_env_file('<PATH TO .env FILE>')
    >>> binance.public.serverTime()
    datetime.datetime(2021, 6, 4, 20, 37, 58, 574000)

[1]: https://www.binance.com/
[2]: https://packaging.python.org/tutorials/packaging-projects/
