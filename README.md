# chess-puzzle-evaluator

## Script setup
### I would recommend setting up a [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) before installing this project's requirements</sub>
  
Install the project requirements  
```
pip install -r requirements.txt
```
### AND  
Install stockfish on your machine: https://github.com/official-stockfish/Stockfish

## Running the script
```
python3 main.py <path_to_stockfish> <path_to_pgn_directory>
```
Any invalid pgn's are logged to `invalid.txt` with errors messages   
<sub>
`invalid.txt` is created in the same directory as `main.py`
</sub>

## Features
This script:
- Validates multiple pgn files in a directory
- Validates multiple games within a single file
- Coloured terminal output whilst running
- Detailed log file in the format \<FEN> \<MOVES> \<ERROR>
<sub>
Coming soon... requesting move data from a 'Site' url specified in the pgn file if there are no moves
</sub>
