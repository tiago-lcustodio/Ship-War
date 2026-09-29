import pygame

from settings import (
    SCREEN_WIDTH
)

from game_data import (
    PRIMARY_WEAPONS,
    SECONDARY_WEAPONS,
    DEFENSE_MODULES,
    SHIPS
)


class LoadoutScene:

    def __init__(
        self,
        game
    ):

        self.game = game

        self.progress = (
            game.progress
        )


        self.categories = [
            "PRIMARY",
            "SECONDARY",
            "DEFENSE",
            "SHIP"
        ]


        self.category_index = 0

        self.item_index = 0


        self.title_font = (
            pygame.font.SysFont(
                "couriernew",
                36,
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
                14,
                bold=True
            )
        )


        self.category_rects = []

        self.item_rects = []


        self.equip_rect = pygame.Rect(
            390,
            590,
            140,
            42
        )


        self.back_rect = pygame.Rect(
            190,
            590,
            140,
            42
        )


    # =====================================================
    # OWNED
    # =====================================================

    def get_items(
        self
    ):

        category = (
            self.categories[
                self.category_index
            ]
        )


        if (
            category
            == "PRIMARY"
        ):

            return [

                item_id

                for item_id
                in PRIMARY_WEAPONS

                if self.progress
                .owns_primary(
                    item_id
                )
            ]


        if (
            category
            == "SECONDARY"
        ):

            return [

                item_id

                for item_id
                in SECONDARY_WEAPONS

                if self.progress
                .owns_secondary(
                    item_id
                )
            ]


        if (
            category
            == "DEFENSE"
        ):

            return [

                item_id

                for item_id
                in DEFENSE_MODULES

                if self.progress
                .owns_defense(
                    item_id
                )
            ]


        return [

            ship_id

            for ship_id
            in SHIPS

            if self.progress
            .owns_ship(
                ship_id
            )
        ]


    # =====================================================
    # EQUIP
    # =====================================================

    def equip(
        self
    ):

        items = (
            self.get_items()
        )


        if not items:

            return


        self.item_index = min(

            self.item_index,

            len(items) - 1
        )


        selected_id = (
            items[
                self.item_index
            ]
        )


        category = (
            self.categories[
                self.category_index
            ]
        )


        if (
            category
            == "PRIMARY"
        ):

            self.progress.equipped_primary = (
                selected_id
            )


        elif (
            category
            == "SECONDARY"
        ):

            self.progress.equipped_secondary = (
                selected_id
            )


        elif (
            category
            == "DEFENSE"
        ):

            self.progress.equipped_defense = (
                selected_id
            )


        else:

            self.progress.ship_id = (
                selected_id
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

            if (
                event.key
                == pygame.K_ESCAPE
            ):

                self.game.show_map()

                return


            if (
                event.key
                == pygame.K_LEFT
            ):

                self.category_index = (

                    self.category_index - 1

                ) % len(
                    self.categories
                )


                self.item_index = 0


            elif (
                event.key
                == pygame.K_RIGHT
            ):

                self.category_index = (

                    self.category_index + 1

                ) % len(
                    self.categories
                )


                self.item_index = 0


            elif (
                event.key
                == pygame.K_UP
            ):

                items = (
                    self.get_items()
                )


                if items:

                    self.item_index = (

                        self.item_index - 1

                    ) % len(items)


            elif (
                event.key
                == pygame.K_DOWN
            ):

                items = (
                    self.get_items()
                )


                if items:

                    self.item_index = (

                        self.item_index + 1

                    ) % len(items)


            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                self.equip()


        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN

            and event.button == 1
        ):

            for (
                index,
                rect
            ) in enumerate(
                self.category_rects
            ):

                if rect.collidepoint(
                    event.pos
                ):

                    self.category_index = (
                        index
                    )

                    self.item_index = 0

                    return


            for (
                index,
                rect
            ) in enumerate(
                self.item_rects
            ):

                if rect.collidepoint(
                    event.pos
                ):

                    self.item_index = (
                        index
                    )

                    return


            if (
                self.equip_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.equip()

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
    # DRAW BUTTON
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
                70,
                72
            ),
            rect,
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
                8,
                14,
                20
            )
        )


        title = (
            self.title_font.render(
                "LOADOUT",
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


        # =================================================
        # TABS
        # =================================================

        self.category_rects = []


        x = 45


        for (
            index,
            category
        ) in enumerate(
            self.categories
        ):

            rect = pygame.Rect(
                x,
                90,
                150,
                38
            )


            self.category_rects.append(
                rect
            )


            selected = (
                index
                == self.category_index
            )


            if selected:

                pygame.draw.rect(
                    screen,
                    (
                        45,
                        65,
                        70
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
                    150,
                    160,
                    165
                )
            )


            text = (
                self.small_font.render(
                    category,
                    True,
                    color
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=rect.center
                )
            )


            x += 160


        # =================================================
        # ITEMS
        # =================================================

        items = (
            self.get_items()
        )


        if items:

            self.item_index = min(

                self.item_index,

                len(items) - 1
            )


        category = (
            self.categories[
                self.category_index
            ]
        )


        self.item_rects = []


        y = 170


        for (
            index,
            item_id
        ) in enumerate(
            items
        ):

            rect = pygame.Rect(
                90,
                y - 7,
                540,
                38
            )


            self.item_rects.append(
                rect
            )


            if (
                category
                == "PRIMARY"
            ):

                data = (
                    PRIMARY_WEAPONS[
                        item_id
                    ]
                )


                name = (
                    data[
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .equipped_primary
                    == item_id
                )


            elif (
                category
                == "SECONDARY"
            ):

                data = (
                    SECONDARY_WEAPONS[
                        item_id
                    ]
                )


                name = (
                    data[
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .equipped_secondary
                    == item_id
                )


            elif (
                category
                == "DEFENSE"
            ):

                data = (
                    DEFENSE_MODULES[
                        item_id
                    ]
                )


                name = (
                    data[
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .equipped_defense
                    == item_id
                )


            else:

                data = (
                    SHIPS[
                        item_id
                    ]
                )


                name = (
                    data[
                        "name"
                    ]
                )


                equipped = (
                    self.progress.ship_id
                    == item_id
                )


            selected = (
                index
                == self.item_index
            )


            if selected:

                pygame.draw.rect(
                    screen,
                    (
                        40,
                        55,
                        60
                    ),
                    rect,
                    border_radius=4
                )


            suffix = (
                "   [EQUIPPED]"
                if equipped
                else ""
            )


            if (
                data.get(
                    "special",
                    False
                )
            ):

                suffix += (
                    "   [SECRET]"
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
                    210
                )
            )


            text = (
                self.font.render(
                    (
                        name
                        + suffix
                    ),
                    True,
                    color
                )
            )


            screen.blit(
                text,
                (
                    100,
                    y
                )
            )


            y += 45


        chips = (
            self.font.render(
                (
                    "FORBIDDEN NAV CHIPS: "
                    f"{self.progress.nav_chips}"
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
            chips.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    545
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
            self.equip_rect,
            "EQUIP"
        )