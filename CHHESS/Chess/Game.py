# from . import Objects
import Objects


class Referee:
    def moves_as_squares(
        moves: list[Objects.Position], board: Objects.Board
    ) -> list[Objects.Square]:
        """Returns a list of Position objects as a list of corresponding Square
        objects, given a Board object.

        Args:
            moves (list[Objects.Position]): Original move list containing Position objects.
            board (Objects.Board): Board in play.

        Returns:
            list[Objects.Square]: New move list containing Square objects.
        """
        moves_squares = []
        for move in moves:
            moves_squares.append(board.board[move.index()[0]][move.index()[1]])
        return moves_squares

    def legal_moves(
        piece: Objects.Piece, board: Objects.Board, checked: bool = False
    ) -> list[Objects.Square]:
        if piece is None or board is None:
            raise ValueError("Invalid piece or board.")
        if checked:
            pass
        else:
            # Get all possible moves as a list of Squares
            moves = Referee.moves_as_squares(piece.possible_moves(), board)

            # Remove blocked lines of sights
            if isinstance(piece, Objects.Pawn):
                moves = Referee.Pawn.prune_lines(moves, piece, board)
            elif isinstance(piece, Objects.Bishop):
                moves = Referee.Bishop.prune_lines(moves, piece)
            elif isinstance(piece, Objects.Rook):
                moves = Referee.Rook.prune_lines(moves, piece)
            elif isinstance(piece, Objects.Queen):
                moves = Referee.Queen.prune_lines(moves, piece)

            # Remove moves that arrive on a piece of the same team
            i = 0
            while i < len(moves):
                if moves[i].piece is not None and board.colour == moves[i].piece.colour:
                    moves.pop(i)
                    i -= 1
                i += 1

            # TODO Remove moves that result in a check

        return moves

    def copy_board(board: Objects.Board) -> Objects.Board:
        return Objects.Board(board.sequence)

    # def check_check(board: Objects.Board) -> bool:
    #     """Returns True if the board is in a checked state.

    #     Args:
    #         board (Objects.Board): The current board.

    #     Returns:
    #         bool: Whether or not the current player is in check.
    #     """
    #     # Check every one of opponent's legal moves for King
    #     for piece in board.active[0 if board.colour else 1]:
    #         for move in legal_moves(piece, board):
    #             if isinstance(move.piece, Objects.King) and (
    #                 (move.piece.colour and board.colour)
    #                 or (not move.piece.colour and not board.colour)
    #             ):
    #                 return True
    #     return False

    # def check_mate(board: Objects.Board) -> bool:
    #     """Returns True if the board is in a checkmate state.

    #     Args:
    #         board (Objects.Board): The current board.

    #     Returns:
    #         bool: Whether or not the current player is in checkmate.
    #     """
    #     for piece in board.active[1 if board.colour else 0]:
    #         if (
    #             isinstance(piece, Objects.King)
    #             and (
    #                 (piece.colour and board.colour)
    #                 or (not piece.colour and not board.colour)
    #             )
    #             and len(legal_moves(piece.possible_moves(), board)) == 0
    #         ):
    #             return True
    #     return False

    class Pawn:
        # TODO This method only needs board for the most recent move for en passant
        def prune_lines(
            moves: list[Objects.Square], pawn: Objects.Pawn, board: Objects.Board
        ) -> list[Objects.Square]:
            """Prunes blocked lines of sight within the passed set of moves for
            this piece.

            Args:
                moves (list[Objects.Square]): Moves possible for this piece.
                pawn (Objects.Pawn): Pawn in play.
                board (Objects.Board): Board in play.

            Returns:
                list[Objects.Square]: Possible moves for this piece, with
                    blocked lines of sight pruned.
            """
            file_p, rank_p = pawn.position.file, pawn.position.rank

            i = 0
            while i < len(moves):
                file_m, rank_m = moves[i].position.file, moves[i].position.rank
                piece_a = moves[i].piece

                # Remove file advancement if there is a piece in the way
                if file_m == file_p and piece_a is not None:
                    # If single advancement blocked, remove both single and double
                    if rank_m == rank_p + (-1 if pawn.colour else 1):
                        moves.pop(i)
                        i -= 1
                        # Search through moves for double to remove
                        for j in range(len(moves)):
                            if moves[j].position.rank == rank_p + (
                                -2 if pawn.colour else 2
                            ):
                                moves.pop(j)
                                i -= 1
                    # If double advancement blocked, only remove double
                    if rank_m == rank_p + (-2 if pawn.colour else 2):
                        moves.pop(i)
                        i -= 1

                # Remove capture if there is no piece and not en passant
                for j in (-1, 1):
                    if file_m == file_p + j:
                        if piece_a is None and not Referee.Pawn.en_passant(
                            pawn, board, j == -1
                        ):
                            moves.pop(i)
                            i -= 1

                i += 1

            return moves

        def en_passant(pawn: Objects.Pawn, board: Objects.Board, left: bool) -> bool:
            """Returns whether or not argument pawn is able to perform a capture en passant.

            Args:
                pawn (Objects.Pawn): Pawn in play.
                board (Objects.Board): Board in play.
                left (bool): True to check the file to the left of the pawn, False otherwise.

            Returns:
                bool: True if the pawn is able to capture en passant on the side specified.
            """
            if (
                (pawn.colour and pawn.position.rank != 4)
                or (not pawn.colour and pawn.position.rank != 5)
                or not isinstance(
                    board.sequence.sequence[-1].depart.piece, Objects.Pawn
                )
                or board.sequence.sequence[-1].arrive.position.file
                != pawn.position.file + (-1 if left else -1)
                or board.sequence.sequence[-1].arrive.position.rank
                != (4 if pawn.colour else 5)
            ):
                return False
            return True

    class Bishop:
        def prune_lines(
            moves: list[Objects.Square], bishop: Objects.Bishop
        ) -> list[Objects.Square]:
            """Prunes blocked lines of sight within the passed set of moves for
            this piece.

            Args:
                moves (list[Objects.Square]): Moves possible for this piece.
                bishop (Objects.Bishop): Bishop in play.
                board (Objects.Board): Board in play.

            Returns:
                list[Objects.Square]: Possible moves for this piece, with
                    blocked lines of sight pruned.
            """
            file_p, rank_p = bishop.position.file, bishop.position.rank
            left, right, up, down = file_p - 1, 8 - file_p, 8 - rank_p, rank_p - 1

            moves = Referee.Bishop.prune_line(
                moves, bishop, min(right, up), not bishop.colour, not bishop.colour
            )
            moves = Referee.Bishop.prune_line(
                moves, bishop, min(right, down), bishop.colour, not bishop.colour
            )
            moves = Referee.Bishop.prune_line(
                moves, bishop, min(left, down), bishop.colour, bishop.colour
            )
            moves = Referee.Bishop.prune_line(
                moves, bishop, min(left, up), not bishop.colour, bishop.colour
            )

            return moves

        def prune_line(
            moves: list[Objects.Square],
            bishop: Objects.Bishop,
            sight: int,
            up: bool,
            right: bool,
        ) -> list[Objects.Square]:
            """Prunes one line of sight within the passed set of moves for this piece.

            Args:
                moves (list[Objects.Square]): Possible moves for this piece.
                bishop (Objects.Bishop): Bishop in play.
                sight (int): Length of the line of sight, by number of squares.
                up (bool): If the line of sight is towards the 8-rank.
                right (bool): If the line of sight is towards the h-file.

            Returns:
                list[Objects.Square]: Possible moves for this piece, with a
                    single line of sight pruned.
            """
            file_p, rank_p = bishop.position.file, bishop.position.rank
            i, f, r, prune = 0, 1 if right else -1, 1 if up else -1, False

            # Loop over moves list to find squares along single line of sight
            while i < len(moves) and abs(f) <= sight and abs(r) <= sight:
                file_m, rank_m = moves[i].position.file, moves[i].position.rank
                piece_a = moves[i].piece

                # Prune move if line of sight is blocked
                if file_m == file_p + f and rank_m == rank_p + r:
                    if prune or piece_a is not None:
                        if prune or piece_a.colour == bishop.colour:
                            moves.pop(i)
                        i, f, r, prune = (
                            -1,
                            f + (1 if right else -1),
                            r + (1 if up else -1),
                            True,
                        )

                if i == len(moves) - 1:
                    i, f, r = -1, f + (1 if right else -1), r + (1 if up else -1)

                i += 1

            return moves

    class Rook:
        def prune_lines(
            moves: list[Objects.Square], rook: Objects.Rook
        ) -> list[Objects.Square]:
            """Prunes blocked lines of sight within the passed set of moves for
            this piece.

            Args:
                moves (list[Objects.Square]): Moves possible for this piece.
                rook (Objects.Rook): Rook in play.
                board (Objects.Board): Board in play.

            Returns:
                list[Objects.Square]: Possible moves for this piece, with
                    blocked lines of sight pruned.
            """
            file_p, rank_p = rook.position.file, rook.position.rank
            left, right, up, down = file_p - 1, 8 - file_p, 8 - rank_p, rank_p - 1

            moves = Referee.Rook.prune_line(moves, rook, right, not rook.colour, True)
            moves = Referee.Rook.prune_line(moves, rook, down, rook.colour, False)
            moves = Referee.Rook.prune_line(moves, rook, left, rook.colour, True)
            moves = Referee.Rook.prune_line(moves, rook, up, not rook.colour, False)

            return moves

        def prune_line(
            moves: list[Objects.Square],
            rook: Objects.Rook,
            sight: int,
            increasing: bool,
            along_files: bool,
        ) -> list[Objects.Square]:
            """Prunes one line of sight within the passed set of moves for this piece.

            Args:
                moves (list[Objects.Square]): Possible moves for this piece.
                rook (Objects.Rook): Rook in play.
                sight (int): Length of the line of sight, by number of squares.
                increasing (bool): If the line of sight is towards the 8-rank or
                h-file.
                along_files (bool): If the line of sight is along the files.

            Returns:
                list[Objects.Square]: Possible moves for this piece, with a
                    single line of sight pruned.
            """
            file_p, rank_p = rook.position.file, rook.position.rank
            i, a, prune = 0, 1 if increasing else -1, False

            # Loop over moves list to find squares along single line of sight
            while i < len(moves) and abs(a) <= sight:
                file_m, rank_m = moves[i].position.file, moves[i].position.rank
                piece_a = moves[i].piece

                # Prune move if line of sight is blocked
                if (along_files and file_m == file_p + a and rank_m == rank_p) or (
                    not along_files and file_m == file_p and rank_m == rank_p + a
                ):
                    if prune or piece_a is not None:
                        if prune or piece_a.colour == rook.colour:
                            moves.pop(i)
                        i, a, prune = -1, a + (1 if increasing else -1), True

                if i == len(moves) - 1:
                    i, a = -1, a + (1 if increasing else -1)

                i += 1

            return moves

    class Queen:
        def prune_lines(
            moves: list[Objects.Square], queen: Objects.Queen
        ) -> list[Objects.Square]:
            """Prunes blocked lines of sight within the passed set of moves for
            this piece.

            Args:
                moves (list[Objects.Square]): Moves possible for this piece.
                queen (Objects.Queen): Queen in play.
                board (Objects.Board): Board in play.

            Returns:
                list[Objects.Square]: Possible moves for this piece, with
                    blocked lines of sight pruned.
            """
            file_p, rank_p = queen.position.file, queen.position.rank
            left, right, up, down = 8 - file_p, file_p - 1, rank_p - 1, 8 - rank_p

            # Clean diagonal lines of sight
            moves = Referee.Bishop.prune_line(
                moves, queen, min(right, up), not queen.colour, not queen.colour
            )
            moves = Referee.Bishop.prune_line(
                moves, queen, min(right, down), queen.colour, not queen.colour
            )
            moves = Referee.Bishop.prune_line(
                moves, queen, min(left, down), queen.colour, queen.colour
            )
            moves = Referee.Bishop.prune_line(
                moves, queen, min(left, up), not queen.colour, queen.colour
            )

            # Clean axis lines of sight
            moves = Referee.Rook.prune_line(moves, queen, right, not queen.colour, True)
            moves = Referee.Rook.prune_line(moves, queen, down, queen.colour, False)
            moves = Referee.Rook.prune_line(moves, queen, left, queen.colour, True)
            moves = Referee.Rook.prune_line(moves, queen, up, not queen.colour, False)

            return moves


class Player:
    def move(board: Objects.Board, event: Objects.Event) -> Objects.Board:
        # TODO Implement string interpretation?
        # Assume legal moves by the power of Game

        # Remove captured piece if capture event
        if event.capture:
            i_c = 0 if board.colour else 1
            for i in range(len(board.active[i_c])):
                if str(board.active[i_c][i].position) == str(event.arrive.position):
                    board.active[i_c].pop(i)
                    board.captured[i_c].append(i)
                    break

        # Move piece from depart to arrive
        i_a = event.arrive.position.index()
        i_d = event.depart.position.index()
        board.board[i_a[0]][i_a[1]].piece = event.depart.piece
        board.board[i_a[0]][i_a[1]].piece.position = event.arrive.position
        board.board[i_d[0]][i_d[1]].piece = None

        board.sequence.add_event(event)
        board.colour = not board.colour

        return board

    def user_turn(board: Objects.Board) -> None:
        print(board)

        # Current input: depart arrive, e.g. e4 e6
        input_user = input().split()
        i_d = Objects.Position(input_user[0], mode=3).index()
        i_s = Objects.Position(input_user[1], mode=3).index()

        # Restarts turn if move not legal
        legal_moves = Referee.legal_moves(board.board[i_d[0]][i_d[1]].piece, board)
        legal_pos = [str(legal_moves[i].position) for i in range(len(legal_moves))]
        if str(Objects.Position(input_user[1], mode=3)) not in legal_pos:
            print("Invalid move. Please try another move.")
            return

        # Move piece across board and change turn
        event = Objects.Event(board.board[i_d[0]][i_d[1]], board.board[i_s[0]][i_s[1]])
        Player.move(board, event)

    def play():
        board = Objects.Board(notate=True)

        for i in range(10):
            Player.user_turn(board)


Player.play()
