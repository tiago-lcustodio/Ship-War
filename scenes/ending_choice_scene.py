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
            (
                "LEAVE THE SOLAR SYSTEM",
                "leave"
            ),
            (
                "STAY",
                "stay"
            )
        ]


        self.selected = 0


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                38,
                bold=True
            )
        )


        self.font = (
            pygame.font.SysFont(
                "couriernew",
                22,
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
    # ACTIVATE
    # =====================================================

    def activate(
        self,
        index
    ):

        ending_type = (
            self.options[
                index
            ][1]
        )


        self.game.show_ending(
            ending_type
        )


    # =====================================================
    # EVENTS
    # =====================================================

    def handle_event(
        self,
        event
    ):

        if (
            event.type
            == pygame.KEYDOWN
        ):

            if event.key in (
                pygame.K_UP,
                pygame.K_LEFT
            ):

                self.selected = (

                    self.selected - 1

                ) % len(
                    self.options
                )


            elif event.key in (
                pygame.K_DOWN,
                pygame.K_RIGHT
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
                    self.selected
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
                        index
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
                5,
                10,
                18
            )
        )


        title = (
            self.title_font.render(
                "THE NAVIGATION CORE IS COMPLETE",
                True,
                (
                    120,
                    235,
                    210
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
                    190
                )
            )
        )


        self.option_rects = []


        for (
            index,
            item
        ) in enumerate(
            self.options
        ):

            label = (
                item[0]
            )


            rect = pygame.Rect(
                170,
                285
                + index * 100,
                380,
                60
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
                    65,
                    85,
                    75
                )
                if selected
                else
                (
                    40,
                    50,
                    55
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
                    label,
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


        note = (
            self.small_font.render(
                "THERE IS NO RIGHT ANSWER.",
                True,
                (
                    135,
                    145,
                    150
                )
            )
        )


        screen.blit(
            note,
            note.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    535
                )
            )
        )