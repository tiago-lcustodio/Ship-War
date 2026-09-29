import pygame

from settings import (
    SCREEN_WIDTH
)

from password_system import (
    decode_password
)


class PasswordScene:

    def __init__(
        self,
        game
    ):

        self.game = game

        self.password = ""

        self.message = ""


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
                22,
                bold=True
            )
        )


        self.password_font = (
            pygame.font.SysFont(
                "couriernew",
                22,
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


        if (
            event.key
            == pygame.K_ESCAPE
        ):

            self.game.show_menu()

            return


        if (
            event.key
            == pygame.K_BACKSPACE
        ):

            self.password = (
                self.password[:-1]
            )

            self.message = ""

            return


        if (
            event.key
            == pygame.K_RETURN
        ):

            progress = (
                decode_password(
                    self.password
                )
            )


            if progress is None:

                self.message = (
                    "INVALID PASSWORD"
                )

            else:

                self.game.resume_progress(
                    progress
                )


            return


        if (
            len(self.password) < 30
            and event.unicode
            and event.unicode.isprintable()
            and not event.unicode.isspace()
        ):

            self.password += (
                event.unicode
            )


            self.message = ""


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
                12,
                18,
                24
            )
        )


        title = (
            self.title_font.render(
                "PASSWORD",
                True,
                (
                    245,
                    225,
                    170
                )
            )
        )


        screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    110
                )
            )
        )


        instruction = (
            self.font.render(
                "TYPE YOUR 30 CHARACTER PASSWORD",
                True,
                (
                    220,
                    220,
                    210
                )
            )
        )


        screen.blit(
            instruction,
            instruction.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    200
                )
            )
        )


        rendered = (
            self.password_font.render(
                self.password + "_",
                True,
                (
                    120,
                    240,
                    180
                )
            )
        )


        screen.blit(
            rendered,
            rendered.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    300
                )
            )
        )


        counter = (
            self.font.render(
                (
                    f"{len(self.password)}"
                    "/30"
                ),
                True,
                (
                    150,
                    150,
                    150
                )
            )
        )


        screen.blit(
            counter,
            counter.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    345
                )
            )
        )


        if self.message:

            message = (
                self.font.render(
                    self.message,
                    True,
                    (
                        255,
                        90,
                        90
                    )
                )
            )


            screen.blit(
                message,
                message.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        420
                    )
                )
            )


        back = (
            self.font.render(
                "ENTER: CONFIRM     ESC: BACK",
                True,
                (
                    190,
                    190,
                    190
                )
            )
        )


        screen.blit(
            back,
            back.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    590
                )
            )
        )