import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR
)


class MenuScene:

    def __init__(
        self,
        game
    ):

        self.game = game


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                68,
                bold=True
            )
        )


        self.option_font = (
            pygame.font.SysFont(
                "couriernew",
                30,
                bold=True
            )
        )


        path = (
            ASSETS_DIR
            / "backgrounds"
            / "menu_background.png"
        )


        if path.exists():

            image = pygame.image.load(
                str(path)
            ).convert()


            self.background = (
                pygame.transform.smoothscale(
                    image,
                    (
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT
                    )
                )
            )

        else:

            self.background = (
                pygame.Surface(
                    (
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT
                    )
                )
            )


            self.background.fill(
                (
                    10,
                    15,
                    20
                )
            )


        self.options = [

            "NEW GAME",

            "PASSWORD",

            "QUIT"
        ]


        self.selected = 0

        self.option_rects = []


    def activate_option(
        self,
        index
    ):

        option = (
            self.options[
                index
            ]
        )


        if option == "NEW GAME":

            self.game.new_game()


        elif option == "PASSWORD":

            self.game.show_password_screen()


        elif option == "QUIT":

            self.game.running = False


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
                == pygame.K_DOWN
            ):

                self.selected = (
                    self.selected + 1
                ) % len(
                    self.options
                )


            elif (
                event.key
                == pygame.K_UP
            ):

                self.selected = (
                    self.selected - 1
                ) % len(
                    self.options
                )


            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                self.activate_option(
                    self.selected
                )


        elif (
            event.type
            == pygame.MOUSEMOTION
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

                    self.activate_option(
                        index
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

        screen.blit(
            self.background,
            (0, 0)
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
                65
            )
        )


        screen.blit(
            overlay,
            (0, 0)
        )


        title = (
            self.title_font.render(
                "SHIP WAR",
                True,
                (
                    250,
                    225,
                    160
                )
            )
        )


        screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    90
                )
            )
        )


        self.option_rects.clear()


        start_y = 390


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
                    215,
                    80
                )
                if selected
                else (
                    235,
                    230,
                    210
                )
            )


            prefix = (
                "> "
                if selected
                else "  "
            )


            text = (
                self.option_font.render(
                    prefix + option,
                    True,
                    color
                )
            )


            rect = (
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        start_y
                        + index * 60
                    )
                )
            )


            self.option_rects.append(
                rect.inflate(
                    40,
                    18
                )
            )


            screen.blit(
                text,
                rect
            )