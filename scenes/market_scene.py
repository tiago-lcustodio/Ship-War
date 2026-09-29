import random
import pygame

from settings import (
    SCREEN_WIDTH,
    ASSETS_DIR
)

from game_data import (
    MARKET_ITEMS,
    SPECIAL_MARKET_POOL,
    TRADING_POSTS,
    SHIPS,
    MERCHANT_SPECIES,
    MERCHANT_MOODS,
    ROUTE_ITEM_BITS
)


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


        # ==================================
        # STOCK
        # ==================================

        self.item_ids = list(
            self.post.get(
                "stock",
                []
            )
        )


        special_slots = (
            self.post.get(
                "special_slots",
                0
            )
        )


        if (
            special_slots > 0
            and SPECIAL_MARKET_POOL
        ):

            available = [

                item

                for item in
                SPECIAL_MARKET_POOL

                if item
                not in self.item_ids
            ]


            amount = min(
                special_slots,
                len(
                    available
                )
            )


            self.item_ids.extend(

                random.sample(
                    available,
                    amount
                )
            )


        # ==================================
        # MERCHANT
        # ==================================

        self.merchant_species_id = (
            random.choice(
                list(
                    MERCHANT_SPECIES.keys()
                )
            )
        )


        self.merchant_mood_id = (
            random.choice(
                list(
                    MERCHANT_MOODS.keys()
                )
            )
        )


        self.merchant_species = (
            MERCHANT_SPECIES[
                self.merchant_species_id
            ]
        )


        self.merchant_mood = (
            MERCHANT_MOODS[
                self.merchant_mood_id
            ]
        )


        self.price_modifier = (
            self.merchant_mood[
                "price_modifier"
            ]
        )


        # ==================================
        # PORTRAIT
        # ==================================

        filename = (

            self.merchant_species[
                "portrait_prefix"
            ]

            + "_"

            + self.merchant_mood_id

            + ".png"
        )


        path = (
            ASSETS_DIR
            / "portraits"
            / filename
        )


        if path.exists():

            image = (
                pygame.image.load(
                    str(path)
                ).convert_alpha()
            )


            self.merchant_portrait = (
                pygame.transform.smoothscale(
                    image,
                    (
                        110,
                        140
                    )
                )
            )

        else:

            self.merchant_portrait = (
                pygame.Surface(
                    (
                        110,
                        140
                    ),
                    pygame.SRCALPHA
                )
            )


            pygame.draw.rect(
                self.merchant_portrait,
                (
                    60,
                    85,
                    75
                ),
                (
                    0,
                    0,
                    110,
                    140
                ),
                border_radius=8
            )


        self.selected = 0

        self.message = ""

        self.purchase_done = False


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
                19,
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


    # =====================================================
    # PRICE
    # =====================================================

    def get_price(
        self,
        item
    ):

        price = (
            item["price"]
            * self.price_modifier
        )


        return int(
            round(
                price / 10
            )
            * 10
        )


    def get_selected_item(
        self
    ):

        if not self.item_ids:

            return None


        return MARKET_ITEMS[
            self.item_ids[
                self.selected
            ]
        ]


    # =====================================================
    # BUY
    # =====================================================

    def buy_selected(
        self
    ):

        if self.purchase_done:

            self.message = (
                "ONLY ONE PURCHASE ALLOWED"
            )

            return


        item = (
            self.get_selected_item()
        )


        if item is None:

            return


        progress = (
            self.game.progress
        )


        price = (
            self.get_price(
                item
            )
        )


        if (
            progress.money
            < price
        ):

            self.message = (
                "NOT ENOUGH CREDITS"
            )

            return


        # ==================================
        # HP
        # ==================================

        if (
            item["type"]
            == "hp_upgrade"
        ):

            if (
                progress.max_hp
                >= item["max_hp"]
            ):

                self.message = (
                    "HULL ALREADY MAXIMUM"
                )

                return


            progress.money -= price

            progress.max_hp += 1


            self.message = (
                "HULL UPGRADED"
            )


        # ==================================
        # SHIP
        # ==================================

        elif (
            item["type"]
            == "ship"
        ):

            new_ship_id = (
                item["ship_id"]
            )


            if (
                progress.ship_id
                == new_ship_id
            ):

                self.message = (
                    "ALREADY EQUIPPED"
                )

                return


            progress.money -= price

            progress.ship_id = (
                new_ship_id
            )


            progress.max_hp = max(

                progress.max_hp,

                SHIPS[
                    new_ship_id
                ][
                    "base_hp"
                ]
            )


            self.message = (
                "SHIP PURCHASED"
            )


        # ==================================
        # ROUTE ITEM
        # ==================================

        elif (
            item["type"]
            == "route_item"
        ):

            route_item = (
                item[
                    "route_item"
                ]
            )


            bit = (
                ROUTE_ITEM_BITS[
                    route_item
                ]
            )


            if (
                progress
                .has_route_item_bit(
                    bit
                )
            ):

                self.message = (
                    "ALREADY IN INVENTORY"
                )

                return


            progress.money -= price


            progress.add_route_item_bit(
                bit
            )


            self.message = (
                "NAVIGATION ITEM ACQUIRED"
            )


        else:

            self.message = (
                "ITEM NOT IMPLEMENTED"
            )

            return


        self.purchase_done = (
            True
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
            != pygame.KEYDOWN
        ):

            return


        if event.key in (
            pygame.K_ESCAPE,
            pygame.K_RETURN
        ):

            self.game.show_map()

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


        elif (
            event.key
            == pygame.K_b
        ):

            self.buy_selected()


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
                    45
                )
            )
        )


        screen.blit(
            self.merchant_portrait,
            (
                18,
                90
            )
        )


        species = (
            self.small_font.render(
                self.merchant_species[
                    "name"
                ],
                True,
                (
                    180,
                    220,
                    200
                )
            )
        )


        screen.blit(
            species,
            (
                20,
                238
            )
        )


        mood = (
            self.small_font.render(
                (
                    "MOOD: "
                    + self.merchant_mood[
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
                260
            )
        )


        progress = (
            self.game.progress
        )


        credits = (
            self.font.render(
                (
                    "CREDITS: $ "
                    f"{progress.money}"
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
            credits.get_rect(
                center=(
                    430,
                    95
                )
            )
        )


        ship = (
            self.small_font.render(
                (
                    "CURRENT SHIP: "
                    + SHIPS[
                        progress.ship_id
                    ][
                        "name"
                    ]
                ),
                True,
                (
                    210,
                    210,
                    200
                )
            )
        )


        screen.blit(
            ship,
            ship.get_rect(
                center=(
                    430,
                    125
                )
            )
        )


        # ==================================
        # STOCK
        # ==================================

        if not self.item_ids:

            empty = (
                self.font.render(
                    "SPECIAL STOCK COMING SOON",
                    True,
                    (
                        180,
                        180,
                        170
                    )
                )
            )


            screen.blit(
                empty,
                empty.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        330
                    )
                )
            )


        else:

            start_y = 185


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


                price = (
                    self.get_price(
                        item
                    )
                )


                selected = (
                    index
                    == self.selected
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


                prefix = (
                    "> "
                    if selected
                    else "  "
                )


                text = (
                    self.font.render(
                        (
                            prefix
                            + item["name"]
                            + "   $"
                            + str(price)
                        ),
                        True,
                        color
                    )
                )


                screen.blit(
                    text,
                    (
                        180,
                        start_y
                        + index * 48
                    )
                )


            item = (
                self.get_selected_item()
            )


            if item:

                description = (
                    self.small_font.render(
                        item[
                            "description"
                        ],
                        True,
                        (
                            170,
                            210,
                            200
                        )
                    )
                )


                screen.blit(
                    description,
                    description.get_rect(
                        center=(
                            SCREEN_WIDTH // 2,
                            465
                        )
                    )
                )


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
                        530
                    )
                )
            )


        controls = (
            self.small_font.render(
                (
                    "UP/DOWN SELECT   "
                    "B BUY   "
                    "ENTER RETURN TO MAP"
                ),
                True,
                (
                    190,
                    190,
                    180
                )
            )
        )


        screen.blit(
            controls,
            controls.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    625
                )
            )
        )