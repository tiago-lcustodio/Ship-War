import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class ComingSoonScene:

    def __init__(
        self,
        game,
        progress
    ):

        self.game = game

        self.progress = progress


        self.title_font = pygame.font.SysFont(
            "couriernew",
            48,
            bold=True
        )


        self.font = pygame.font.SysFont(
            "couriernew",
            27,
            bold=True
        )


    def handle_event(
        self,
        event
    ):

        if (
            event.type
            == pygame.KEYDOWN
        ):

            if event.key in (
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
            (10, 18, 24)
        )


        title = self.title_font.render(
            "PASSWORD ACCEPTED",
            True,
            (110, 245, 175)
        )


        screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    250
                )
            )
        )


        level = self.font.render(
            f"NEXT LEVEL: {self.progress.next_level}",
            True,
            (235, 225, 200)
        )


        screen.blit(
            level,
            level.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    380
                )
            )
        )


        money = self.font.render(
            f"MONEY: $ {self.progress.money}",
            True,
            (235, 225, 200)
        )


        screen.blit(
            money,
            money.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    430
                )
            )
        )


        message = self.font.render(
            "LEVEL 2 IS NOT IMPLEMENTED YET",
            True,
            (230, 150, 80)
        )


        screen.blit(
            message,
            message.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    540
                )
            )
        )


        back = self.font.render(
            "ENTER - MAIN MENU",
            True,
            (190, 190, 190)
        )


        screen.blit(
            back,
            back.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    680
                )
            )
        )