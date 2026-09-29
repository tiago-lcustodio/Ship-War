import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE
)

from game import Game


def normalize_event(event):
    """
    Faz o Enter do teclado numérico funcionar
    exatamente como o Enter principal.

    Isso vale para TODAS as scenes sem precisar
    alterar cada uma individualmente.
    """

    if (
        event.type
        in (
            pygame.KEYDOWN,
            pygame.KEYUP
        )
        and
        event.key
        == pygame.K_KP_ENTER
    ):

        data = (
            event.dict.copy()
        )

        data["key"] = (
            pygame.K_RETURN
        )

        return pygame.event.Event(
            event.type,
            data
        )

    return event


def main():

    pygame.init()

    pygame.display.set_caption(
        TITLE
    )

    screen = (
        pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )
    )

    clock = pygame.time.Clock()

    game = Game(
        screen
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


            event = (
                normalize_event(
                    event
                )
            )


            game.handle_event(
                event
            )


        game.update(
            dt
        )


        game.draw()


        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":

    main()