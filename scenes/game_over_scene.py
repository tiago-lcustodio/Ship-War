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
            retry_progress.clone()
        )


        self.level_number = (
            level_number
        )


        self.options = [
            "RETRY",
            "MAP"
        ]


        self.selected = 0


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                48,
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


        self.small_font = (
            pygame.font.SysFont(
                "couriernew",
                15,
                bold=True
            )
        )


        self.option_rects = []


    # =====================================================
    # SELECT
    # =====================================================

    def activate(
        self,
        option
    ):

        if (
            option
            == "RETRY"
        ):

            self.game.progress = (
                self.retry_progress
                .clone()
            )


            self.game.launch_level(
                self.level_number
            )


        elif (
            option
            == "MAP"
        ):

            self.game.progress = (
                self.retry_progress
                .clone()
            )


            self.game.progress.next_level = (
                self.level_number
            )


            self.game.show_map()


    # =====================================================
    # EVENT
    # =====================================================

    def handle_event(
        self,
        event
    ):

        if (
            event.type
            == pygame.KEYDOWN
        ):

            if (
                event.key
                == pygame.K_UP
            ):

                self.selected = (

                    self.selected - 1

                ) % len(
                    self.options
                )


            elif (
                event.key
                == pygame.K_DOWN
            ):

                self.selected = (

                    self.selected + 1

                ) % len(
                    self.options
                )


            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                self.activate(
                    self.options[
                        self.selected
                    ]
                )


            elif (
                event.key
                == pygame.K_ESCAPE
            ):

                self.activate(
                    "MAP"
                )


        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN

            and event.button == 1
        ):

            for (
                index,
                rect
            ) in enumerate(
                self.option_rects
            ):

                if rect.collidepoint(
                    event.pos
                ):

                    self.selected = (
                        index
                    )


                    self.activate(
                        self.options[
                            index
                        ]
                    )


                    return


    def update(
        self,
        dt
    ):

        pass


    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen
    ):

        screen.fill(
            (
                10,
                10,
                15
            )
        )


        title = (
            self.title_font.render(
                "SHIP DESTROYED",
                True,
                (
                    230,
                    90,
                    80
                )
            )
        )


        screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    150
                )
            )
        )


        subtitle = (
            self.small_font.render(
                (
                    "Progress from this "
                    "attempt was lost."
                ),
                True,
                (
                    180,
                    180,
                    175
                )
            )
        )


        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    210
                )
            )
        )


        self.option_rects = []


        for (
            index,
            option
        ) in enumerate(
            self.options
        ):

            rect = pygame.Rect(
                240,
                310
                + index * 70,
                240,
                48
            )


            self.option_rects.append(
                rect
            )


            selected = (
                index
                == self.selected
            )


            pygame.draw.rect(
                screen,
                (
                    60,
                    65,
                    68
                )
                if not selected
                else
                (
                    75,
                    85,
                    70
                ),
                rect,
                border_radius=6
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
                    205
                )
            )


            text = (
                self.font.render(
                    option,
                    True,
                    color
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=rect.center
                )
            )