import math
import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR
)

from game_data import (
    MAP_LOCATIONS,
    MAP_CONNECTIONS,
    TRADING_POSTS,
    SHIPS
)


class MapScene:

    def __init__(
        self,
        game
    ):

        self.game = game

        self.progress = (
            game.progress
        )


        self.current_location = (
            self.progress.next_level
        )


        self.selected_location = (
            self.current_location
        )


        self.travel_target = None

        self.moving = False

        self.pending_market = False


        self.ship_position = (
            pygame.Vector2(
                MAP_LOCATIONS[
                    self.current_location
                ][
                    "position"
                ]
            )
        )


        self.travel_speed = (
            380
        )


        # ==================================
        # FONTS
        # ==================================

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
                17,
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


        # ==================================
        # ICONS
        # ==================================

        self.location_images = {}


        for (
            level_id,
            data
        ) in MAP_LOCATIONS.items():

            path = (
                ASSETS_DIR
                / "map"
                / data[
                    "sprite"
                ]
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
                            40,
                            40
                        )
                    )
                )


                self.location_images[
                    level_id
                ] = image


        ship_path = (
            ASSETS_DIR
            / "map"
            / "map_ship.png"
        )


        self.ship_image = None


        if ship_path.exists():

            image = (
                pygame.image.load(
                    str(ship_path)
                ).convert_alpha()
            )


            self.ship_image = (
                pygame.transform.smoothscale(
                    image,
                    (
                        34,
                        34
                    )
                )
            )


        self.node_rects = {}

        self.market_rects = {}


        self.start_rect = pygame.Rect(
            420,
            600,
            260,
            44
        )


        self.market_button_rect = pygame.Rect(
            40,
            600,
            260,
            44
        )


    # =====================================================
    # GRAPH
    # =====================================================

    def get_neighbors(
        self,
        location
    ):

        neighbors = []


        for a, b in (
            MAP_CONNECTIONS
        ):

            if a == location:

                neighbors.append(
                    b
                )


            elif b == location:

                neighbors.append(
                    a
                )


        return neighbors


    def can_travel_to(
        self,
        target
    ):

        if (
            target
            == self.current_location
        ):

            return True


        if (
            not self.progress
            .is_discovered(
                target
            )
        ):

            return False


        return (
            target
            in self.get_neighbors(
                self.current_location
            )
        )


    # =====================================================
    # MARKET
    # =====================================================

    def get_market_at_location(
        self,
        location
    ):

        for (
            market_id,
            data
        ) in TRADING_POSTS.items():

            if (
                data[
                    "location"
                ]
                == location
            ):

                return market_id


        return None


    # =====================================================
    # TRAVEL
    # =====================================================

    def start_travel(
        self,
        target,
        open_market=False
    ):

        if self.moving:

            return


        if not self.can_travel_to(
            target
        ):

            return


        if (
            target
            == self.current_location
        ):

            self.selected_location = (
                target
            )


            if open_market:

                self.open_market()


            return


        self.travel_target = (
            target
        )


        self.pending_market = (
            open_market
        )


        self.moving = True


    def arrive(
        self
    ):

        self.current_location = (
            self.travel_target
        )


        self.selected_location = (
            self.current_location
        )


        self.progress.next_level = (
            self.current_location
        )


        self.travel_target = None

        self.moving = False


        if self.pending_market:

            self.pending_market = False

            self.open_market()


    # =====================================================
    # START LEVEL
    # =====================================================

    def start_level(
        self
    ):

        if self.moving:

            return


        self.game.start_location(
            self.current_location
        )


    def open_market(
        self
    ):

        market_id = (
            self.get_market_at_location(
                self.current_location
            )
        )


        if market_id:

            self.game.show_market(
                market_id
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
                == pygame.K_RETURN
            ):

                self.start_level()


            elif (
                event.key
                == pygame.K_m
            ):

                self.open_market()


            elif (
                event.key
                == pygame.K_ESCAPE
            ):

                self.game.show_menu()


        elif (
            event.type
            == pygame.MOUSEBUTTONDOWN

            and event.button == 1
        ):

            # =================================
            # NODES
            # =================================

            for (
                location,
                rect
            ) in self.node_rects.items():

                if rect.collidepoint(
                    event.pos
                ):

                    self.start_travel(
                        location
                    )

                    return


            # =================================
            # MARKET ICONS
            # =================================

            for (
                location,
                rect
            ) in self.market_rects.items():

                if rect.collidepoint(
                    event.pos
                ):

                    self.start_travel(
                        location,
                        open_market=True
                    )

                    return


            # =================================
            # BUTTONS
            # =================================

            if (
                self.start_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.start_level()

                return


            if (
                self.market_button_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.open_market()


    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt
    ):

        if not self.moving:

            return


        destination = (
            pygame.Vector2(
                MAP_LOCATIONS[
                    self.travel_target
                ][
                    "position"
                ]
            )
        )


        difference = (
            destination
            - self.ship_position
        )


        distance = (
            difference.length()
        )


        step = (
            self.travel_speed
            * dt
        )


        if (
            distance
            <= step
        ):

            self.ship_position = (
                destination
            )


            self.arrive()

            return


        if distance > 0:

            self.ship_position += (
                difference.normalize()
                * step
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
                5,
                10,
                20
            )
        )


        # ==================================
        # STARFIELD SIMPLES
        # ==================================

        for i in range(
            70
        ):

            x = (
                (
                    i * 97
                )
                % SCREEN_WIDTH
            )


            y = (
                (
                    i * 53
                )
                % 570
            )


            pygame.draw.circle(
                screen,
                (
                    90,
                    110,
                    140
                ),
                (
                    x,
                    y
                ),
                1
            )


        # ==================================
        # TITLE
        # ==================================

        title = (
            self.title_font.render(
                "SOLAR SYSTEM MAP",
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
                    32
                )
            )
        )


        # ==================================
        # CONNECTIONS
        # ==================================

        for a, b in (
            MAP_CONNECTIONS
        ):

            # Uma rota secreta só aparece
            # se os dois lados forem conhecidos.
            if (
                not self.progress
                .is_discovered(a)

                or not self.progress
                .is_discovered(b)
            ):

                continue


            pos_a = (
                MAP_LOCATIONS[a][
                    "position"
                ]
            )


            pos_b = (
                MAP_LOCATIONS[b][
                    "position"
                ]
            )


            pygame.draw.line(
                screen,
                (
                    75,
                    110,
                    125
                ),
                pos_a,
                pos_b,
                2
            )


        # ==================================
        # NODES
        # ==================================

        self.node_rects.clear()

        self.market_rects.clear()


        for (
            location,
            data
        ) in MAP_LOCATIONS.items():

            if (
                not self.progress
                .is_discovered(
                    location
                )
            ):

                continue


            position = (
                data[
                    "position"
                ]
            )


            accessible = (
                self.can_travel_to(
                    location
                )
            )


            completed = (
                self.progress
                .is_completed(
                    location
                )
            )


            if location in (
                self.location_images
            ):

                image = (
                    self.location_images[
                        location
                    ]
                )


                rect = (
                    image.get_rect(
                        center=position
                    )
                )


                screen.blit(
                    image,
                    rect
                )

            else:

                if completed:

                    color = (
                        110,
                        220,
                        170
                    )

                elif accessible:

                    color = (
                        245,
                        210,
                        100
                    )

                else:

                    color = (
                        100,
                        120,
                        130
                    )


                pygame.draw.circle(
                    screen,
                    color,
                    position,
                    10
                )


                rect = pygame.Rect(
                    0,
                    0,
                    34,
                    34
                )


                rect.center = (
                    position
                )


            self.node_rects[
                location
            ] = (
                rect.inflate(
                    12,
                    12
                )
            )


            label = (
                self.small_font.render(
                    data[
                        "name"
                    ],
                    True,
                    (
                        210,
                        210,
                        200
                    )
                )
            )


            screen.blit(
                label,
                label.get_rect(
                    center=(
                        position[0],
                        position[1] + 29
                    )
                )
            )


            # =================================
            # MARKET ICON
            # =================================

            market_id = (
                self.get_market_at_location(
                    location
                )
            )


            if market_id:

                market_rect = (
                    pygame.Rect(
                        0,
                        0,
                        20,
                        20
                    )
                )


                market_rect.center = (
                    position[0] + 20,
                    position[1] - 18
                )


                pygame.draw.circle(
                    screen,
                    (
                        230,
                        190,
                        80
                    ),
                    market_rect.center,
                    10
                )


                dollar = (
                    self.small_font.render(
                        "$",
                        True,
                        (
                            20,
                            20,
                            15
                        )
                    )
                )


                screen.blit(
                    dollar,
                    dollar.get_rect(
                        center=
                        market_rect.center
                    )
                )


                self.market_rects[
                    location
                ] = (
                    market_rect
                )


        # ==================================
        # PLAYER SHIP
        # ==================================

        if self.ship_image:

            rect = (
                self.ship_image
                .get_rect(
                    center=(
                        round(
                            self.ship_position.x
                        ),
                        round(
                            self.ship_position.y
                        )
                    )
                )
            )


            screen.blit(
                self.ship_image,
                rect
            )

        else:

            # Triângulo temporário.
            x = round(
                self.ship_position.x
            )

            y = round(
                self.ship_position.y
            )


            pygame.draw.polygon(
                screen,
                (
                    230,
                    240,
                    240
                ),
                [
                    (x, y - 13),
                    (x - 9, y + 9),
                    (x + 9, y + 9)
                ]
            )


        # ==================================
        # INFO
        # ==================================

        current_name = (
            MAP_LOCATIONS[
                self.current_location
            ][
                "name"
            ]
        )


        info = (
            self.font.render(
                (
                    "CURRENT LOCATION: "
                    + current_name
                ),
                True,
                (
                    150,
                    220,
                    200
                )
            )
        )


        screen.blit(
            info,
            (
                25,
                570
            )
        )


        # ==================================
        # MARKET BUTTON
        # ==================================

        market = (
            self.get_market_at_location(
                self.current_location
            )
        )


        pygame.draw.rect(
            screen,
            (
                55,
                70,
                72
            ),
            self.market_button_rect,
            border_radius=6
        )


        market_text = (
            "MARKET [M]"
            if market
            else "NO MARKET"
        )


        text = (
            self.font.render(
                market_text,
                True,
                (
                    230,
                    220,
                    190
                )
            )
        )


        screen.blit(
            text,
            text.get_rect(
                center=
                self.market_button_rect
                .center
            )
        )


        # ==================================
        # START BUTTON
        # ==================================

        pygame.draw.rect(
            screen,
            (
                65,
                85,
                75
            ),
            self.start_rect,
            border_radius=6
        )


        start = (
            self.font.render(
                "START MISSION [ENTER]",
                True,
                (
                    245,
                    225,
                    175
                )
            )
        )


        screen.blit(
            start,
            start.get_rect(
                center=
                self.start_rect.center
            )
        )