import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class GameOverScene:

    def __init__(
        self,
        game,
        retry_progress,
        level_number
    ):

        self.game = game

        # Snapshot feito antes de entrar na fase.
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


    # =====================================================
    # EVENTS
    # =====================================================

    def handle_event(self, event):

        if (
            event.type
            != pygame.KEYDOWN
        ):

            return


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

            option = (
                self.options[
                    self.selected
                ]
            )


            if option == "RETRY":

                # Restaura exatamente o estado
                # anterior à tentativa.
                self.game.progress = (
                    self.retry_progress.clone()
                )

                # Retry direto.
                # Não mostra o briefing novamente
                # dentro da mesma tentativa.
                self.game.launch_level(
                    self.level_number
                )


            elif option == "MAP":

                self.game.progress = (
                    self.retry_progress.clone()
                )

                self.game.progress.next_level = (
                    self.level_number
                )

                self.game.show_map()


        elif (
            event.key
            == pygame.K_ESCAPE
        ):

            self.game.progress = (
                self.retry_progress.clone()
            )

            self.game.show_map()


    def update(self, dt):

        pass


    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

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
                    "Mission progress from this "
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


        for (
            index,
            option
        ) in enumerate(
            self.options
        ):

            selected = (
                index == self.selected
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


            prefix = (
                "> "
                if selected
                else "  "
            )


            text = (
                self.font.render(
                    prefix + option,
                    True,
                    color
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        340
                        + index * 60
                    )
                )
            )