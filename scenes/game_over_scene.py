import pygame

from settings import (
    SCREEN_WIDTH
)


class GameOverScene:

    def __init__(
        self,
        game,
        retry_progress,
        level_number
    ):

        self.game = game

        self.retry_progress = (
            retry_progress
        )

        self.level_number = (
            level_number
        )


        self.big_font = (
            pygame.font.SysFont(
                "couriernew",
                62,
                bold=True
            )
        )


        self.font = (
            pygame.font.SysFont(
                "couriernew",
                24,
                bold=True
            )
        )


    def handle_event(
        self,
        event
    ):

        if (
            event.type
            != pygame.KEYDOWN
        ):

            return


        if event.key == pygame.K_r:

            self.game.progress = (
                self.retry_progress
            )


            self.game.launch_level(
                self.level_number
            )


        elif event.key in (
            pygame.K_RETURN,
            pygame.K_ESCAPE
        ):

            self.game.show_menu()


    def update(
        self,
        dt
    ):

        pass


    def draw(
        self,
        screen
    ):

        screen.fill(
            (
                18,
                8,
                8
            )
        )


        title = (
            self.big_font.render(
                "GAME OVER",
                True,
                (
                    230,
                    75,
                    60
                )
            )
        )


        screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    230
                )
            )
        )


        retry = (
            self.font.render(
                "R - RETRY LEVEL",
                True,
                (
                    230,
                    220,
                    200
                )
            )
        )


        screen.blit(
            retry,
            retry.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    360
                )
            )
        )


        menu = (
            self.font.render(
                "ENTER - MAIN MENU",
                True,
                (
                    230,
                    220,
                    200
                )
            )
        )


        screen.blit(
            menu,
            menu.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    410
                )
            )
        )