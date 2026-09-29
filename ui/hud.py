import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BOTTOM_PANEL_HEIGHT,
    ASSETS_DIR
)


class RetroHUD:

    def __init__(
        self
    ):

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
                14,
                bold=True
            )
        )


        self.portraits = {}


        for mood in (
            "happy",
            "neutral",
            "sad"
        ):

            path = (
                ASSETS_DIR
                / "portraits"
                / f"nihl_{mood}.png"
            )


            if path.exists():

                image = pygame.image.load(
                    str(path)
                ).convert_alpha()


                image = (
                    pygame.transform.smoothscale(
                        image,
                        (
                            70,
                            88
                        )
                    )
                )

            else:

                # Placeholder temporário.
                image = pygame.Surface(
                    (
                        70,
                        88
                    ),
                    pygame.SRCALPHA
                )


                pygame.draw.ellipse(
                    image,
                    (
                        150,
                        160,
                        155
                    ),
                    (
                        13,
                        6,
                        44,
                        65
                    )
                )


                pygame.draw.ellipse(
                    image,
                    (
                        20,
                        25,
                        24
                    ),
                    (
                        18,
                        25,
                        13,
                        22
                    )
                )


                pygame.draw.ellipse(
                    image,
                    (
                        20,
                        25,
                        24
                    ),
                    (
                        39,
                        25,
                        13,
                        22
                    )
                )


            self.portraits[
                mood
            ] = image


    def get_nihl_mood(
        self,
        player
    ):

        # Vida cheia.
        if (
            player.hp
            == player.max_hp
        ):

            return "happy"


        # Próximo tiro mata.
        if player.hp <= 1:

            return "sad"


        return "neutral"


    def draw(
        self,
        screen,
        player,
        level_number,
        nav_core_parts
    ):

        # ==================================
        # HUD SUPERIOR
        # ==================================

        top_panel = pygame.Surface(
            (
                SCREEN_WIDTH,
                55
            ),
            pygame.SRCALPHA
        )


        top_panel.fill(
            (
                12,
                22,
                24,
                215
            )
        )


        screen.blit(
            top_panel,
            (0, 0)
        )


        pygame.draw.line(
            screen,
            (
                210,
                190,
                120
            ),
            (
                0,
                54
            ),
            (
                SCREEN_WIDTH,
                54
            ),
            2
        )


        hp = (
            self.font.render(
                (
                    f"HP "
                    f"{player.hp}/"
                    f"{player.max_hp}"
                ),
                True,
                (
                    240,
                    225,
                    175
                )
            )
        )


        screen.blit(
            hp,
            (
                15,
                7
            )
        )


        money = (
            self.font.render(
                f"$ {player.money}",
                True,
                (
                    240,
                    225,
                    175
                )
            )
        )


        screen.blit(
            money,
            money.get_rect(
                topright=(
                    SCREEN_WIDTH - 15,
                    7
                )
            )
        )


        # ==================================
        # HUD INFERIOR
        # ==================================

        y = (
            SCREEN_HEIGHT
            - BOTTOM_PANEL_HEIGHT
        )


        bottom_panel = pygame.Surface(
            (
                SCREEN_WIDTH,
                BOTTOM_PANEL_HEIGHT
            ),
            pygame.SRCALPHA
        )


        bottom_panel.fill(
            (
                10,
                18,
                20,
                235
            )
        )


        screen.blit(
            bottom_panel,
            (
                0,
                y
            )
        )


        pygame.draw.line(
            screen,
            (
                210,
                190,
                120
            ),
            (
                0,
                y
            ),
            (
                SCREEN_WIDTH,
                y
            ),
            2
        )


        mood = (
            self.get_nihl_mood(
                player
            )
        )


        portrait = (
            self.portraits[
                mood
            ]
        )


        screen.blit(
            portrait,
            (
                12,
                y + 6
            )
        )


        ship_text = (
            self.font.render(
                player.ship_name,
                True,
                (
                    245,
                    225,
                    175
                )
            )
        )


        screen.blit(
            ship_text,
            (
                100,
                y + 16
            )
        )


        weapon = (
            self.small_font.render(
                (
                    "WEAPON: "
                    f"{player.weapon_name}"
                ),
                True,
                (
                    130,
                    220,
                    190
                )
            )
        )


        screen.blit(
            weapon,
            (
                100,
                y + 48
            )
        )


        core = (
            self.small_font.render(
                (
                    "NAV CORE: "
                    f"{nav_core_parts}/3"
                ),
                True,
                (
                    130,
                    220,
                    190
                )
            )
        )


        screen.blit(
            core,
            (
                100,
                y + 70
            )
        )


        level = (
            self.font.render(
                f"LEVEL {level_number}",
                True,
                (
                    245,
                    225,
                    175
                )
            )
        )


        screen.blit(
            level,
            level.get_rect(
                topright=(
                    SCREEN_WIDTH - 15,
                    y + 18
                )
            )
        )