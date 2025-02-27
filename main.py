import os
import argparse
import chess.pgn
from stockfish import Stockfish
from colorama import Fore, Style


OUTPUT_FILE = "invalid.txt"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Puzzle Checker",
        description="Checks pgn files to ensure mainline plays best moves",
        epilog=f"NOTE: The file {OUTPUT_FILE} is cleared at start of script"
    )
    parser.add_argument('stockfish_path')
    parser.add_argument('pgn_directory')
    args = parser.parse_args()

    # Clear output file
    open(OUTPUT_FILE, 'w').close()

    # Initialise stockfish engine
    stockfish = Stockfish(
        path=args.stockfish_path,
        depth=20,
        parameters={"Threads": 8, "Minimum Thinking Time": 10}
    )

    for file in os.listdir(args.pgn_directory):
        # Skip if not .pgn
        if not file.endswith(".pgn"):
            continue

        file_path = args.pgn_directory + file
        print(f"{Fore.YELLOW}File: {file_path}{Style.RESET_ALL}")
        pgn = open(file_path)

        # A loop to read multiple pgn from a single file
        while True:
            puzzle = chess.pgn.read_game(pgn)

            if puzzle is None:
                break

            valid = valid_puzzle(stockfish, puzzle)

            if valid:
                print(f"{Fore.GREEN}VALID!{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}INVALID!{Style.RESET_ALL}\n")


def valid_puzzle(stockfish: Stockfish, puzzle: chess.pgn.Game) -> bool:
    fen = puzzle.headers["FEN"]

    # TODO: If no mainline moves then try to request from "Site" header
    mainline_moves = puzzle.mainline_moves()

    print(f"{Fore.MAGENTA}Evaluating: {fen}{Style.RESET_ALL}")
    print(mainline_moves)

    stockfish.set_fen_position(fen)
    for i, move in enumerate(mainline_moves):
        puzzle_move = str(move)

        # Only check every second move, as it would be the players move
        # Doesn't matter if opponent has multiple lines
        if i % 2 == 0:
            best_move = str(stockfish.get_best_move())
            if puzzle_move != best_move:
                print(f"{puzzle_move}-->{best_move}")
                append_output(f"{fen} {puzzle_move}-->{best_move}")
                return False

            # TODO: Check for multiple best moves, and if so, mark as invalid

        stockfish.make_moves_from_current_position([puzzle_move])
    return True


def append_output(line: str) -> None:
    with open(OUTPUT_FILE, 'a') as f:
        f.write(f"{line}\n")


if __name__ == "__main__":
    main()
