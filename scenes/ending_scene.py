import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR
)


class EndingScene:

    def __init__(
        self,
        game,
        ending_type
    ):

        self.game = game

        self.ending_type = (
            ending_type
        )


        if ending_type == "leave":

            filename = (
                "ending_leave.png"
            )

            self.title = (
                "DESTINATION: HOME"
            )

            self.message = (
                "NIHL LEFT THE SOLAR SYSTEM."
            )

        else:

            filename = (
                "ending_stay.png"
            )

            self.title = (
                "NAVIGATION CANCELLED"
            )

            self.message = (
                "NIHL DECIDED TO STAY."
            )


        path = (
            ASSETS_DIR
            / "backgrounds"
            / filename
        )


        self.background = None


        if path.exists():

            image = (
                pygame.image.load(
                    str(path)
                ).convert()
            )


            self.background = (
                pygame.transform.smoothscale(
                    image,
                    (
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT
                    )
                )
            )


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                40,
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

        if self.background:

            screen.blit(
                self.background,
                (0, 0)
            )

        else:

            screen.fill(
                (
                    4,
                    8,
                    15
                )
            )


        overlay = pygame.Surface(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )


        overlay.fill(
            (
                0,
                0,
                0,
                75
            )
        )


        screen.blit(
            overlay,
            (0, 0)
        )


        title = (
            self.title_font.render(
                self.title,
                True,
                (
                    245,
                    220,
                    150
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


        message = (
            self.font.render(
                self.message,
                True,
                (
                    230,
                    230,
                    215
                )
            )
        )


        screen.blit(
            message,
            message.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    320
                )
            )
        )


        end = (
            self.font.render(
                "THE END",
                True,
                (
                    120,
                    230,
                    180
                )
            )
        )


        screen.blit(
            end,
            end.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    395
                )
            )
        )


        back = (
            self.font.render(
                "PRESS ENTER",
                True,
                (
                    210,
                    210,
                    200
                )
            )
        )


        screen.blit(
            back,
            back.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    580
                )
            )
        )