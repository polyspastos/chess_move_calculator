#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from typing import Union
from numpy import zeros

import click
import pygame

APP_DIR = Path(__file__).parent
log = logging.getLogger()


@click.command()
@click.option(
    "-b", "--board-size", nargs=2, type=int, help="please provide row, then column"
)
@click.option("--piece", help="name of piece, e.g. knight")
def main(
    board_size,
    piece,
):

    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 255)
    GREY = (84, 84, 84)

    game_display = pygame.display.set_mode(
        (50 + board_size[0] * 50 + 50, 50 + board_size[1] * 50 + 50)
    )
    game_display.fill(GREY)

    board_clicked = False
    board_calculated = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                if (
                    mouse_pos[0] > 50
                    and mouse_pos[0] < 50 + board_size[0] * 50
                    and mouse_pos[1] > 50
                    and mouse_pos[1] < 50 + board_size[1] * 50
                ):
                    board_clicked = True
                else:
                    board_clicked = False

                piece_position = (mouse_pos[0] // 50 - 1, mouse_pos[1] // 50 - 1)
                
                if board_clicked:
                    board = give_moves(board_size, piece, piece_position)
                    board_calculated = True

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for i in range(0, board_size[0]):
            for j in range(0, board_size[1]):
                if ((i - j) % 2) == 0:
                    pygame.draw.rect(
                        game_display, WHITE, (50 + i * 50, 50 + j * 50, 50, 50)
                    )
                else:
                    pygame.draw.rect(
                        game_display, BLACK, (50 + i * 50, 50 + j * 50, 50, 50)
                    )

        if board_calculated:
            row_number = 0
            for row in board:
                row_number += 1
                column_number = 0
                for square_value in row:
                    column_number += 1
                    if square_value == 1:
                        pygame.draw.rect(
                            game_display,
                            GREEN,
                            (50 + (row_number - 1) * 50, 50 + (column_number - 1) * 50, 50, 50),
                        )
                    if square_value == 9:
                        pygame.draw.rect(
                            game_display,
                            BLUE,
                            (50 + (row_number - 1) * 50, 50 + (column_number - 1) * 50, 50, 50),
                        )            

        if board_clicked:
            pygame.draw.rect(
                game_display,
                BLUE,
                ((mouse_pos[0] // 50) * 50, (mouse_pos[1] // 50) * 50, 50, 50),
            )

        pygame.display.update()


def give_moves(board_size, piece, piece_position):
    board = zeros(board_size, int)

    board[piece_position[0]][piece_position[1]] = 9

    if piece == "knight":
        move_vectors = [
            (1, 2),
            (1, -2),
            (2, 1),
            (2, -1),
            (-1, 2),
            (-1, -2),
            (-2, 1),
            (-2, -1),
        ]
    else: raise NotImplementedError

    for v in move_vectors:
        if (
            piece_position[0] + v[0] >= 0
            and piece_position[0] + v[0] <= board_size[0]
            and piece_position[1] + v[1] >= 0
            and piece_position[1] + v[1] <= board_size[1]
        ):
            new_pos = piece_position[0] + v[0], piece_position[1] + v[1]
            try:
                board[new_pos[0], new_pos[1]] = 1
            except Exception as e:
                # print(e)
                log.error(e)
    # print("board after:\n", board)

    return board


if __name__ == "__main__":
    handler = logging.FileHandler(APP_DIR / "piece_moves.log")
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    main()
