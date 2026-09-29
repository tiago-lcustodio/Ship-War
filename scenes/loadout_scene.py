import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
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


    # =====================================================
    # OWNED LIST
    # =====================================================

    def get_items(
        self
    ):

        category = (
            self.categories[
                self.category_index
            ]
        )


        if category == "PRIMARY":

            return [

                item_id

                for item_id
                in PRIMARY_WEAPONS

                if self.progress
                .owns_primary(
                    item_id
                )
            ]


        if category == "SECONDARY":

            return [

                item_id

                for item_id
                in SECONDARY_WEAPONS

                if self.progress
                .owns_secondary(
                    item_id
                )
            ]


        if category == "DEFENSE":

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


    def equip(
        self
    ):

        items = (
            self.get_items()
        )


        if not items:

            return


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


        if category == "PRIMARY":

            self.progress.equipped_primary = (
                selected_id
            )


        elif category == "SECONDARY":

            self.progress.equipped_secondary = (
                selected_id
            )


        elif category == "DEFENSE":

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
            != pygame.KEYDOWN
        ):

            return


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


        # ==================================
        # CATEGORY TABS
        # ==================================

        x = 70


        for (
            index,
            category
        ) in enumerate(
            self.categories
        ):

            selected = (
                index
                == self.category_index
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
                (
                    x,
                    105
                )
            )


            x += 155


        items = (
            self.get_items()
        )


        category = (
            self.categories[
                self.category_index
            ]
        )


        y = 175


        for (
            index,
            item_id
        ) in enumerate(
            items
        ):

            if category == "PRIMARY":

                name = (
                    PRIMARY_WEAPONS[
                        item_id
                    ][
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .equipped_primary
                    == item_id
                )


            elif category == "SECONDARY":

                name = (
                    SECONDARY_WEAPONS[
                        item_id
                    ][
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .equipped_secondary
                    == item_id
                )


            elif category == "DEFENSE":

                name = (
                    DEFENSE_MODULES[
                        item_id
                    ][
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .equipped_defense
                    == item_id
                )


            else:

                name = (
                    SHIPS[
                        item_id
                    ][
                        "name"
                    ]
                )


                equipped = (
                    self.progress
                    .ship_id
                    == item_id
                )


            selected = (
                index
                == self.item_index
            )


            prefix = (
                "> "
                if selected
                else "  "
            )


            suffix = (
                "   [EQUIPPED]"
                if equipped
                else ""
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
                    prefix
                    + name
                    + suffix,
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
                    555
                )
            )
        )


        controls = (
            self.small_font.render(
                (
                    "LEFT/RIGHT CATEGORY   "
                    "UP/DOWN SELECT   "
                    "ENTER EQUIP   ESC MAP"
                ),
                True,
                (
                    180,
                    190,
                    190
                )
            )
        )


        screen.blit(
            controls,
            controls.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    635
                )
            )
        )