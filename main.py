import os
import argparse
import chess.pgn
from stockfish import Stockfish
from colorama import Fore, Style


LOG_FILEPATH = "invalid.txt"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Puzzle Checker",
        description="Checks pgn files to ensure mainline plays best moves",
        epilog=f"NOTE: The file {LOG_FILEPATH} is cleared at start of script"
    )
    parser.add_argument('stockfish_path')
    parser.add_argument('pgn_directory')
    args = parser.parse_args()

    # Clear output file
    open(LOG_FILEPATH, 'w').close()

    # Initialise stockfish engine
    stockfish = Stockfish(
        path=args.stockfish_path,
        depth=20,
        parameters={"Threads": 16, "Minimum Thinking Time": 8}
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

    # NOTE: Only checking main line moves atm
    moves = puzzle.mainline_moves()

    print(f"{Fore.MAGENTA}Evaluating: {fen}{Style.RESET_ALL}")

    # TODO: If no moves then try to request from "Site" header
    if not moves:
        print("NO MOVES IN PUZZLE?!")
        return False

    print(moves)

    stockfish.set_fen_position(fen)
    for i, move in enumerate(moves):
        puzzle_move = str(move)

        # Only check every second move, as it would be the players move
        # Doesn't matter if opponent has multiple lines
        if i % 2 == 0:
            top_moves = stockfish.get_top_moves(2)
            best_move = top_moves[0]['Move']
            next_best_move = top_moves[1]['Move']

            # Check for multiple best moves, and if so, mark as invalid
            if (
                top_moves[0]['Centipawn'] == top_moves[1]['Centipawn'] and
                top_moves[0]['Mate'] == top_moves[1]['Mate']
            ):

                print(f"Two best moves: {best_move} & {next_best_move}")
                append_log(f"{fen} {moves} {best_move} & {next_best_move}")
                return False

            # If best move doesnt match pgn then error
            if puzzle_move != best_move:
                print(f"Not best move: {puzzle_move} < {best_move}")
                append_log(f"{fen} {moves} {puzzle_move} < {best_move}")
                return False

        # Make the move on the stockfish board
        stockfish.make_moves_from_current_position([puzzle_move])

    return True


def append_log(line: str) -> None:
    with open(LOG_FILEPATH, 'a') as f:
        f.write(f"{line}\n")


if __name__ == "__main__":
    main()
