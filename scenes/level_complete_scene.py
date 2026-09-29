import pygame

from settings import (
    SCREEN_WIDTH
)

from password_system import (
    generate_password
)


class LevelCompleteScene:

    def __init__(
        self,
        game,
        progress,
        completed_level,
        stats,
        first_clear=False
    ):

        self.game = game

        self.progress = (
            progress
        )


        self.completed_level = (
            completed_level
        )


        self.stats = (
            stats
        )


        self.first_clear = (
            first_clear
        )


        self.password = (
            generate_password(
                progress
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
                21,
                bold=True
            )
        )


        self.small_font = (
            pygame.font.SysFont(
                "couriernew",
                14,
                bold=True
            )
        )


        self.continue_rect = (
            pygame.Rect(
                230,
                545,
                260,
                50
            )
        )


    # =====================================================
    # CONTINUE
    # =====================================================

    def continue_game(
        self
    ):

        self.game.after_level_complete(

            self.completed_level,

            self.first_clear
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
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                self.continue_game()


            elif (
                event.key
                == pygame.K_ESCAPE
            ):

                self.game.show_map()


        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN

            and event.button == 1
        ):

            if (
                self.continue_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.continue_game()


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
                10,
                22,
                24
            )
        )


        if self.first_clear:

            title_text = (
                f"LEVEL "
                f"{self.completed_level}"
                " COMPLETED"
            )

        else:

            title_text = (
                "MISSION COMPLETE"
            )


        title = (
            self.title_font.render(
                title_text,
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
                    65
                )
            )
        )


        if self.first_clear:

            clear = (
                self.font.render(
                    "FIRST CLEAR",
                    True,
                    (
                        120,
                        240,
                        180
                    )
                )
            )


            screen.blit(
                clear,
                clear.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        110
                    )
                )
            )


        enemies = (
            self.font.render(
                (
                    "ENEMIES DESTROYED: "
                    f"{self.stats['enemies_destroyed']}"
                ),
                True,
                (
                    220,
                    220,
                    205
                )
            )
        )


        screen.blit(
            enemies,
            enemies.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    175
                )
            )
        )


        earned = (
            self.font.render(
                (
                    "CREDITS EARNED: "
                    f"{self.stats['money_earned']}"
                ),
                True,
                (
                    220,
                    220,
                    205
                )
            )
        )


        screen.blit(
            earned,
            earned.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    215
                )
            )
        )


        core = (
            self.font.render(
                (
                    "NAV CORE: "
                    f"{self.progress.nav_core_parts}/3"
                ),
                True,
                (
                    120,
                    230,
                    180
                )
            )
        )


        screen.blit(
            core,
            core.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    265
                )
            )
        )


        password_label = (
            self.font.render(
                "NAVIGATION PASSWORD",
                True,
                (
                    245,
                    220,
                    150
                )
            )
        )


        screen.blit(
            password_label,
            password_label.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    350
                )
            )
        )


        password = (
            self.font.render(
                self.password,
                True,
                (
                    120,
                    240,
                    180
                )
            )
        )


        screen.blit(
            password,
            password.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    390
                )
            )
        )


        pygame.draw.rect(
            screen,
            (
                55,
                75,
                70
            ),
            self.continue_rect,
            border_radius=6
        )


        button = (
            self.font.render(
                "CONTINUE",
                True,
                (
                    245,
                    215,
                    120
                )
            )
        )


        screen.blit(
            button,
            button.get_rect(
                center=
                self.continue_rect.center
            )
        )