import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BOTTOM_PANEL_HEIGHT,
    ASSETS_DIR
)

from game_data import (
    LEVELS,
    PRIMARY_WEAPONS,
    SECONDARY_WEAPONS,
    DEFENSE_MODULES
)


class RetroHUD:

    def __init__(self):

        self.font = (
            pygame.font.SysFont(
                "couriernew",
                14,
                bold=True
            )
        )


        self.small_font = (
            pygame.font.SysFont(
                "couriernew",
                11,
                bold=True
            )
        )


        self.tiny_font = (
            pygame.font.SysFont(
                "couriernew",
                10,
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

                image = (
                    pygame.image.load(
                        str(path)
                    ).convert_alpha()
                )


                image = (
                    pygame.transform.smoothscale(
                        image,
                        (
                            64,
                            64
                        )
                    )
                )


            else:

                image = pygame.Surface(
                    (
                        64,
                        64
                    ),
                    pygame.SRCALPHA
                )


                pygame.draw.circle(
                    image,
                    (
                        165,
                        185,
                        180
                    ),
                    (
                        32,
                        32
                    ),
                    25
                )


                pygame.draw.ellipse(
                    image,
                    (
                        20,
                        25,
                        25
                    ),
                    (
                        17,
                        22,
                        12,
                        18
                    )
                )


                pygame.draw.ellipse(
                    image,
                    (
                        20,
                        25,
                        25
                    ),
                    (
                        35,
                        22,
                        12,
                        18
                    )
                )


            self.portraits[
                mood
            ] = image


    # =====================================================
    # MOOD
    # =====================================================

    def get_mood(
        self,
        player
    ):

        if (
            player.hp
            == player.max_hp
        ):

            return "happy"


        if (
            player.hp <= 1
        ):

            return "sad"


        return "neutral"


    # =====================================================
    # SPECIAL MARK
    # =====================================================

    def special_suffix(
        self,
        config
    ):

        if config.get(
            "special",
            False
        ):

            return " *"

        return ""


    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen,
        player,
        level_number,
        nav_core_parts,
        nav_chips=0
    ):

        level_name = (
            LEVELS[
                level_number
            ]["name"]
        )


        # =================================================
        # TOP HUD
        # =================================================

        top_panel = pygame.Surface(
            (
                SCREEN_WIDTH,
                34
            ),
            pygame.SRCALPHA
        )


        top_panel.fill(
            (
                5,
                10,
                12,
                190
            )
        )


        screen.blit(
            top_panel,
            (
                0,
                0
            )
        )


        hull = (
            self.font.render(
                (
                    "HULL "
                    f"{player.hp}/"
                    f"{player.max_hp}"
                ),
                True,
                (
                    120,
                    240,
                    170
                )
            )
        )


        screen.blit(
            hull,
            (
                12,
                9
            )
        )


        x = 125


        if (
            player.shield_capacity
            > 0
        ):

            shield = (
                self.font.render(
                    (
                        "SHIELD "
                        f"{player.shield_points}/"
                        f"{player.shield_capacity}"
                    ),
                    True,
                    (
                        100,
                        195,
                        255
                    )
                )
            )


            screen.blit(
                shield,
                (
                    x,
                    9
                )
            )


            x += 125


        credits = (
            self.font.render(
                (
                    "CR "
                    f"{player.money}"
                ),
                True,
                (
                    245,
                    215,
                    110
                )
            )
        )


        screen.blit(
            credits,
            (
                x,
                9
            )
        )


        level_text = (
            self.font.render(
                (
                    f"LEVEL {level_number} - "
                    f"{level_name}"
                ),
                True,
                (
                    225,
                    225,
                    210
                )
            )
        )


        screen.blit(
            level_text,
            level_text.get_rect(
                right=
                SCREEN_WIDTH - 12,
                centery=17
            )
        )


        # =================================================
        # BOTTOM PANEL
        # =================================================

        panel_y = (
            SCREEN_HEIGHT
            - BOTTOM_PANEL_HEIGHT
        )


        pygame.draw.rect(
            screen,
            (
                10,
                18,
                22
            ),
            (
                0,
                panel_y,
                SCREEN_WIDTH,
                BOTTOM_PANEL_HEIGHT
            )
        )


        pygame.draw.line(
            screen,
            (
                85,
                145,
                145
            ),
            (
                0,
                panel_y
            ),
            (
                SCREEN_WIDTH,
                panel_y
            ),
            2
        )


        # =================================================
        # NIHL
        # =================================================

        mood = (
            self.get_mood(
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
                panel_y + 18
            )
        )


        # =================================================
        # ACTIVE LOADOUT
        # =================================================

        primary = (
            PRIMARY_WEAPONS[
                player.primary_id
            ]
        )


        secondary = (
            SECONDARY_WEAPONS[
                player.secondary_id
            ]
        )


        defense = (
            DEFENSE_MODULES[
                player.defense_id
            ]
        )


        ship_text = (
            self.small_font.render(
                (
                    "SHIP: "
                    + player.ship_name
                ),
                True,
                (
                    200,
                    210,
                    205
                )
            )
        )


        screen.blit(
            ship_text,
            (
                90,
                panel_y + 10
            )
        )


        primary_text = (
            self.small_font.render(
                (
                    "PRIMARY: "
                    + primary["name"]
                    + self.special_suffix(
                        primary
                    )
                ),
                True,
                (
                    120,
                    225,
                    235
                )
            )
        )


        screen.blit(
            primary_text,
            (
                90,
                panel_y + 29
            )
        )


        # =================================================
        # SECONDARY STATUS
        # =================================================

        if (
            player.secondary_id == 0
        ):

            secondary_status = (
                "NONE"
            )


        elif (
            player.secondary_timer <= 0
        ):

            secondary_status = (
                secondary["name"]
                + self.special_suffix(
                    secondary
                )
                + " [READY]"
            )


        else:

            secondary_status = (

                secondary["name"]

                + self.special_suffix(
                    secondary
                )

                + " ["

                + f"{player.secondary_timer:.1f}s"

                + "]"
            )


        secondary_text = (
            self.small_font.render(
                (
                    "SECONDARY: "
                    + secondary_status
                ),
                True,
                (
                    220,
                    185,
                    110
                )
            )
        )


        screen.blit(
            secondary_text,
            (
                90,
                panel_y + 48
            )
        )


        defense_text = (
            self.small_font.render(
                (
                    "DEFENSE: "
                    + defense["name"]
                    + self.special_suffix(
                        defense
                    )
                ),
                True,
                (
                    170,
                    205,
                    255
                )
            )
        )


        screen.blit(
            defense_text,
            (
                90,
                panel_y + 67
            )
        )


        # =================================================
        # RIGHT SIDE
        # =================================================

        core_text = (
            self.small_font.render(
                (
                    "NAV CORE "
                    f"{nav_core_parts}/3"
                ),
                True,
                (
                    120,
                    235,
                    200
                )
            )
        )


        screen.blit(
            core_text,
            (
                520,
                panel_y + 12
            )
        )


        chips_text = (
            self.small_font.render(
                (
                    "NAV CHIPS "
                    f"{nav_chips}"
                ),
                True,
                (
                    100,
                    205,
                    240
                )
            )
        )


        screen.blit(
            chips_text,
            (
                520,
                panel_y + 31
            )
        )


        # =================================================
        # OVERHEAT
        # =================================================

        if (
            player.overheat_timer > 0
        ):

            overheat = (
                self.small_font.render(
                    (
                        "OVERHEAT "
                        f"{player.overheat_timer:.1f}s"
                    ),
                    True,
                    (
                        255,
                        120,
                        80
                    )
                )
            )


            screen.blit(
                overheat,
                (
                    520,
                    panel_y + 50
                )
            )


        elif (
            "overheat_after"
            in primary
        ):

            heat = (
                self.tiny_font.render(
                    (
                        "HEAT "
                        f"{player.overheat_shots}/"
                        f"{primary['overheat_after']}"
                    ),
                    True,
                    (
                        230,
                        190,
                        100
                    )
                )
            )


            screen.blit(
                heat,
                (
                    520,
                    panel_y + 51
                )
            )


        special_hint = (
            self.tiny_font.render(
                "* SECRET EQUIPMENT",
                True,
                (
                    135,
                    130,
                    160
                )
            )
        )


        screen.blit(
            special_hint,
            (
                520,
                panel_y + 73
            )
        )