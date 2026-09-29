import pygame

from settings import (
    SCREEN_WIDTH
)


class EndingChoiceScene:

    def __init__(
        self,
        game
    ):

        self.game = game


        self.options = [

            "LEAVE THE SOLAR SYSTEM",

            "STAY"
        ]


        self.selected = 0


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                42,
                bold=True
            )
        )


        self.font = (
            pygame.font.SysFont(
                "couriernew",
                25,
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


        if event.key in (
            pygame.K_UP,
            pygame.K_DOWN
        ):

            self.selected = (
                1 - self.selected
            )


        elif event.key in (
            pygame.K_RETURN,
            pygame.K_SPACE
        ):

            if self.selected == 0:

                self.game.show_ending(
                    "leave"
                )

            else:

                self.game.show_ending(
                    "stay"
                )


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
                5,
                10,
                18
            )
        )


        title = (
            self.title_font.render(
                "NAVIGATION CORE ONLINE",
                True,
                (
                    120,
                    240,
                    180
                )
            )
        )


        screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    120
                )
            )
        )


        question = (
            self.font.render(
                "WHAT WILL NIHL DO?",
                True,
                (
                    245,
                    220,
                    150
                )
            )
        )


        screen.blit(
            question,
            question.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    240
                )
            )
        )


        for (
            index,
            option
        ) in enumerate(
            self.options
        ):

            selected = (
                index
                == self.selected
            )


            color = (
                (
                    255,
                    210,
                    80
                )
                if selected
                else (
                    220,
                    220,
                    210
                )
            )


            prefix = (
                "> "
                if selected
                else "  "
            )


            rendered = (
                self.font.render(
                    prefix + option,
                    True,
                    color
                )
            )


            screen.blit(
                rendered,
                rendered.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        360
                        + index * 65
                    )
                )
            )