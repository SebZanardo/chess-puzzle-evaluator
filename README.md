# chess-puzzle-evaluator

I would recommend setting up a [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) before running this project  

## Before running the project
Install the project requirements  
```
pip install -r requirements.txt
```
AND  
Install stockfish on your machine: https://github.com/official-stockfish/Stockfish

## How to run the project
```
python3 main.py <path_to_stockfish> <path_to_pgn_directory>
```
Any invalid pgn's are logged to `invalid.txt` with errors messages   
<sub>`invalid.txt` is created in the same directory as `main.py`  </sub>
