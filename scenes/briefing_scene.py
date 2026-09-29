import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR
)

from game_data import (
    LEVELS
)


class BriefingScene:

    def __init__(
        self,
        game,
        level_number
    ):

        self.game = game

        self.level_number = (
            level_number
        )


        self.config = (
            LEVELS[
                level_number
            ]
        )


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                34,
                bold=True
            )
        )


        self.font = (
            pygame.font.SysFont(
                "couriernew",
                20,
                bold=True
            )
        )


        self.small_font = (
            pygame.font.SysFont(
                "couriernew",
                13,
                bold=True
            )
        )


        requested = (
            ASSETS_DIR
            / "backgrounds"
            / self.config[
                "background"
            ]
        )


        fallback = (
            ASSETS_DIR
            / "backgrounds"
            / "background_01.png"
        )


        path = (
            requested
            if requested.exists()
            else fallback
        )


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


        self.launch_rect = pygame.Rect(
            370,
            590,
            280,
            44
        )


        self.map_rect = pygame.Rect(
            70,
            590,
            180,
            44
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

                self.game.launch_level(
                    self.level_number
                )


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
                self.launch_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.game.launch_level(
                    self.level_number
                )

                return


            if (
                self.map_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.game.show_map()

                return


    def update(
        self,
        dt
    ):

        pass


    # =====================================================
    # BUTTON
    # =====================================================

    def draw_button(
        self,
        screen,
        rect,
        text
    ):

        pygame.draw.rect(
            screen,
            (
                50,
                65,
                62
            ),
            rect,
            border_radius=6
        )


        label = (
            self.small_font.render(
                text,
                True,
                (
                    245,
                    220,
                    150
                )
            )
        )


        screen.blit(
            label,
            label.get_rect(
                center=rect.center
            )
        )


    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen
    ):

        screen.blit(
            self.background,
            (
                0,
                0
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
                4,
                10,
                12,
                205
            )
        )


        screen.blit(
            overlay,
            (
                0,
                0
            )
        )


        title = (
            self.title_font.render(
                "MISSION BRIEFING",
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
                    55
                )
            )
        )


        subtitle = (
            self.font.render(
                self.config[
                    "name"
                ],
                True,
                (
                    120,
                    220,
                    190
                )
            )
        )


        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    100
                )
            )
        )


        mission = (
            self.font.render(
                self.config[
                    "briefing_title"
                ],
                True,
                (
                    245,
                    225,
                    170
                )
            )
        )


        screen.blit(
            mission,
            mission.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    150
                )
            )
        )


        y = 205


        for line in (
            self.config[
                "briefing"
            ]
        ):

            text = (
                self.font.render(
                    line,
                    True,
                    (
                        220,
                        220,
                        205
                    )
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        y
                    )
                )
            )


            y += 29


        core = (
            self.font.render(
                (
                    "NAV CORE: "
                    f"{self.game.progress.nav_core_parts}/3"
                ),
                True,
                (
                    120,
                    220,
                    190
                )
            )
        )


        screen.blit(
            core,
            core.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    535
                )
            )
        )


        self.draw_button(
            screen,
            self.map_rect,
            "MAP"
        )


        self.draw_button(
            screen,
            self.launch_rect,
            "LAUNCH"
        )