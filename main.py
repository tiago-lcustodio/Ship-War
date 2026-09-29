import sys
import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE
)

from game import Game


def main():

    pygame.init()


    screen = (
        pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )
    )


    pygame.display.set_caption(
        TITLE
    )


    clock = (
        pygame.time.Clock()
    )


    game = (
        Game(
            screen
        )
    )


    while game.running:

        dt = (
            clock.tick(FPS)
            / 1000.0
        )


        for event in (
            pygame.event.get()
        ):

            if (
                event.type
                == pygame.QUIT
            ):

                game.running = False

                continue


            game.handle_event(
                event
            )


        game.update(
            dt
        )


        game.draw()


        pygame.display.flip()


    pygame.quit()

    sys.exit()


if __name__ == "__main__":

    main()