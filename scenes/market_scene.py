import random
import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR
)

from game_data import (
    MARKET_ITEMS,
    TRADING_POSTS,
    MERCHANT_SPECIES,
    MERCHANT_MOODS,
    PRIMARY_WEAPONS,
    SECONDARY_WEAPONS,
    DEFENSE_MODULES,
    SHIPS,
    HULL_UPGRADE_PRICES,
    MAX_PLAYER_HP
)


MERCHANT_NAMES = {

    "gray": [
        "ZIH",
        "KEL",
        "ORR",
        "NEM",
        "VEK",
        "TYL",
        "QIR",
        "SIL"
    ],

    "reptilian": [
        "KRAZ",
        "VORRAK",
        "SSEK",
        "THRAK",
        "ZARR",
        "KESS",
        "DRAAL",
        "VESS"
    ],

    "mantid": [
        "KT'IK",
        "ZAAK",
        "THI'RA",
        "KLIK",
        "IX'KA",
        "TRIIL",
        "KHAK",
        "ZIK'TA"
    ]
}


class MarketScene:

    def __init__(
        self,
        game,
        market_id
    ):

        self.game = game

        self.market_id = (
            market_id
        )


        self.post = (
            TRADING_POSTS[
                market_id
            ]
        )


        self.item_ids = list(
            self.post[
                "stock"
            ]
        )


        self.selected = 0

        self.message = ""


        # =================================================
        # MERCHANT
        # =================================================

        self.species_id = (
            random.choice(
                list(
                    MERCHANT_SPECIES.keys()
                )
            )
        )


        mood_id = (
            random.choice(
                list(
                    MERCHANT_MOODS.keys()
                )
            )
        )


        self.species = (
            MERCHANT_SPECIES[
                self.species_id
            ]
        )


        self.merchant_name = (
            random.choice(
                MERCHANT_NAMES[
                    self.species_id
                ]
            )
        )


        self.mood = (
            MERCHANT_MOODS[
                mood_id
            ]
        )


        self.price_modifier = (
            self.mood[
                "price_modifier"
            ]
        )


        filename = (

            self.species[
                "portrait_prefix"
            ]

            + "_"

            + mood_id

            + ".png"
        )


        portrait_path = (
            ASSETS_DIR
            / "portraits"
            / filename
        )


        self.portrait = pygame.Surface(
            (
                110,
                140
            ),
            pygame.SRCALPHA
        )


        if portrait_path.exists():

            image = (
                pygame.image.load(
                    str(portrait_path)
                ).convert_alpha()
            )


            self.portrait = (
                pygame.transform.smoothscale(
                    image,
                    (
                        110,
                        140
                    )
                )
            )


        else:

            pygame.draw.rect(
                self.portrait,
                (
                    55,
                    80,
                    70
                ),
                self.portrait.get_rect(),
                border_radius=8
            )


        # =================================================
        # FONTS
        # =================================================

        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                35,
                bold=True
            )
        )


        self.font = (
            pygame.font.SysFont(
                "couriernew",
                18,
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


        # =================================================
        # MOUSE AREAS
        # =================================================

        self.item_rects = []


        self.buy_rect = pygame.Rect(
            370,
            580,
            130,
            42
        )


        self.loadout_rect = pygame.Rect(
            510,
            580,
            170,
            42
        )


        self.back_rect = pygame.Rect(
            40,
            580,
            130,
            42
        )


    # =====================================================
    # PRICE
    # =====================================================

    def base_price(
        self,
        item_id
    ):

        progress = (
            self.game.progress
        )


        item = (
            MARKET_ITEMS[
                item_id
            ]
        )


        item_type = (
            item[
                "type"
            ]
        )


        if (
            item_type
            == "hull"
        ):

            if (
                progress.max_hp
                >= MAX_PLAYER_HP
            ):

                return None


            return (
                HULL_UPGRADE_PRICES[
                    progress.max_hp
                ]
            )


        if (
            item_type
            == "nav_chip"
        ):

            return (
                self.post[
                    "nav_chip_price"
                ]
            )


        equipment_id = (
            item[
                "equipment_id"
            ]
        )


        if (
            item_type
            == "primary"
        ):

            return (
                PRIMARY_WEAPONS[
                    equipment_id
                ][
                    "price"
                ]
            )


        if (
            item_type
            == "secondary"
        ):

            return (
                SECONDARY_WEAPONS[
                    equipment_id
                ][
                    "price"
                ]
            )


        if (
            item_type
            == "defense"
        ):

            return (
                DEFENSE_MODULES[
                    equipment_id
                ][
                    "price"
                ]
            )


        if (
            item_type
            == "ship"
        ):

            return (
                SHIPS[
                    equipment_id
                ][
                    "price"
                ]
            )


        return None


    def get_price(
        self,
        item_id
    ):

        price = (
            self.base_price(
                item_id
            )
        )


        if price is None:

            return None


        modified = (
            price
            * self.price_modifier
        )


        return int(
            round(
                modified / 10
            )
            * 10
        )


    # =====================================================
    # OWNED
    # =====================================================

    def is_owned(
        self,
        item_id
    ):

        item = (
            MARKET_ITEMS[
                item_id
            ]
        )


        progress = (
            self.game.progress
        )


        item_type = (
            item[
                "type"
            ]
        )


        if item_type in (
            "hull",
            "nav_chip"
        ):

            return False


        equipment_id = (
            item[
                "equipment_id"
            ]
        )


        if (
            item_type
            == "primary"
        ):

            return (
                progress
                .owns_primary(
                    equipment_id
                )
            )


        if (
            item_type
            == "secondary"
        ):

            return (
                progress
                .owns_secondary(
                    equipment_id
                )
            )


        if (
            item_type
            == "defense"
        ):

            return (
                progress
                .owns_defense(
                    equipment_id
                )
            )


        if (
            item_type
            == "ship"
        ):

            return (
                progress
                .owns_ship(
                    equipment_id
                )
            )


        return False


    # =====================================================
    # BUY
    # =====================================================

    def buy_selected(
        self
    ):

        if not self.item_ids:

            return


        item_id = (
            self.item_ids[
                self.selected
            ]
        )


        item = (
            MARKET_ITEMS[
                item_id
            ]
        )


        progress = (
            self.game.progress
        )


        if self.is_owned(
            item_id
        ):

            self.message = (
                "ALREADY OWNED"
            )

            return


        price = (
            self.get_price(
                item_id
            )
        )


        if price is None:

            self.message = (
                "MAXIMUM REACHED"
            )

            return


        if (
            progress.money
            < price
        ):

            self.message = (
                "NOT ENOUGH CREDITS"
            )

            return


        progress.money -= (
            price
        )


        item_type = (
            item[
                "type"
            ]
        )


        if (
            item_type
            == "hull"
        ):

            progress.max_hp += 1

            self.message = (
                "MAX HULL INCREASED"
            )


        elif (
            item_type
            == "nav_chip"
        ):

            if (
                progress.nav_chips >= 7
            ):

                progress.money += (
                    price
                )


                self.message = (
                    "CHIP STORAGE FULL"
                )

                return


            progress.nav_chips += 1


            self.message = (
                "NAV CHIP ACQUIRED"
            )


        elif (
            item_type
            == "primary"
        ):

            equipment_id = (
                item[
                    "equipment_id"
                ]
            )


            progress.own_primary(
                equipment_id
            )


            progress.equipped_primary = (
                equipment_id
            )


            self.message = (
                "PRIMARY ACQUIRED + EQUIPPED"
            )


        elif (
            item_type
            == "secondary"
        ):

            equipment_id = (
                item[
                    "equipment_id"
                ]
            )


            progress.own_secondary(
                equipment_id
            )


            progress.equipped_secondary = (
                equipment_id
            )


            self.message = (
                "SECONDARY ACQUIRED + EQUIPPED"
            )


        elif (
            item_type
            == "defense"
        ):

            equipment_id = (
                item[
                    "equipment_id"
                ]
            )


            progress.own_defense(
                equipment_id
            )


            progress.equipped_defense = (
                equipment_id
            )


            self.message = (
                "MODULE ACQUIRED + EQUIPPED"
            )


        elif (
            item_type
            == "ship"
        ):

            equipment_id = (
                item[
                    "equipment_id"
                ]
            )


            progress.own_ship(
                equipment_id
            )


            progress.ship_id = (
                equipment_id
            )


            self.message = (
                "SHIP ACQUIRED + EQUIPPED"
            )


    # =====================================================
    # EVENTS
    # =====================================================

    def handle_event(
        self,
        event
    ):

        # =================================================
        # KEYBOARD
        # =================================================

        if (
            event.type
            == pygame.KEYDOWN
        ):

            if (
                event.key
                == pygame.K_ESCAPE
            ):

                self.game.show_map()

                return


            if (
                event.key
                == pygame.K_l
            ):

                self.game.show_loadout()

                return


            if not self.item_ids:

                return


            if (
                event.key
                == pygame.K_UP
            ):

                self.selected = (

                    self.selected - 1

                ) % len(
                    self.item_ids
                )


            elif (
                event.key
                == pygame.K_DOWN
            ):

                self.selected = (

                    self.selected + 1

                ) % len(
                    self.item_ids
                )


            elif event.key in (
                pygame.K_RETURN,
                pygame.K_b
            ):

                self.buy_selected()


        # =================================================
        # MOUSE
        # =================================================

        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN

            and event.button == 1
        ):

            for (
                index,
                rect
            ) in enumerate(
                self.item_rects
            ):

                if rect.collidepoint(
                    event.pos
                ):

                    self.selected = (
                        index
                    )

                    return


            if (
                self.buy_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.buy_selected()

                return


            if (
                self.loadout_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.game.show_loadout()

                return


            if (
                self.back_rect
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
                55,
                72,
                72
            ),
            rect,
            border_radius=5
        )


        pygame.draw.rect(
            screen,
            (
                115,
                145,
                130
            ),
            rect,
            1,
            border_radius=5
        )


        label = (
            self.small_font.render(
                text,
                True,
                (
                    235,
                    225,
                    200
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

        screen.fill(
            (
                17,
                24,
                25
            )
        )


        title = (
            self.title_font.render(
                self.post[
                    "name"
                ],
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
                    38
                )
            )
        )


        screen.blit(
            self.portrait,
            (
                18,
                90
            )
        )


        identity = (
            self.small_font.render(
                (
                    self.merchant_name
                    + " - "
                    + self.species[
                        "name"
                    ]
                ),
                True,
                (
                    180,
                    220,
                    200
                )
            )
        )


        screen.blit(
            identity,
            (
                20,
                240
            )
        )


        mood = (
            self.small_font.render(
                (
                    "MOOD: "
                    + self.mood[
                        "name"
                    ]
                ),
                True,
                (
                    210,
                    190,
                    130
                )
            )
        )


        screen.blit(
            mood,
            (
                20,
                262
            )
        )


        credits = (
            self.font.render(
                (
                    "CREDITS: "
                    f"{self.game.progress.money}"
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
            credits,
            (
                185,
                90
            )
        )


        chips = (
            self.small_font.render(
                (
                    "NAV CHIPS: "
                    f"{self.game.progress.nav_chips}"
                ),
                True,
                (
                    100,
                    220,
                    230
                )
            )
        )


        screen.blit(
            chips,
            (
                185,
                120
            )
        )


        # =================================================
        # ITEMS
        # =================================================

        self.item_rects = []


        y = 165


        for (
            index,
            item_id
        ) in enumerate(
            self.item_ids
        ):

            item = (
                MARKET_ITEMS[
                    item_id
                ]
            )


            selected = (
                index
                == self.selected
            )


            owned = (
                self.is_owned(
                    item_id
                )
            )


            price = (
                self.get_price(
                    item_id
                )
            )


            if owned:

                price_text = (
                    "OWNED"
                )


            elif price is None:

                price_text = (
                    "MAX"
                )


            else:

                price_text = (
                    f"{price} CR"
                )


            rect = pygame.Rect(
                165,
                y - 6,
                515,
                36
            )


            self.item_rects.append(
                rect
            )


            if selected:

                pygame.draw.rect(
                    screen,
                    (
                        48,
                        58,
                        48
                    ),
                    rect,
                    border_radius=4
                )


            color = (

                (
                    255,
                    210,
                    80
                )

                if selected

                else (
                    225,
                    225,
                    210
                )
            )


            text = (
                self.font.render(
                    (
                        item[
                            "name"
                        ]
                        + "   "
                        + price_text
                    ),
                    True,
                    color
                )
            )


            screen.blit(
                text,
                (
                    175,
                    y
                )
            )


            y += 43


        if self.message:

            message = (
                self.font.render(
                    self.message,
                    True,
                    (
                        245,
                        190,
                        90
                    )
                )
            )


            screen.blit(
                message,
                message.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        540
                    )
                )
            )


        self.draw_button(
            screen,
            self.back_rect,
            "MAP"
        )


        self.draw_button(
            screen,
            self.buy_rect,
            "BUY"
        )


        self.draw_button(
            screen,
            self.loadout_rect,
            "LOADOUT"
        )