import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR
)

from game_data import (
    MAP_LOCATIONS,
    MAP_CONNECTIONS,
    TRADING_POSTS
)


class MapScene:

    def __init__(self, game):

        self.game = game

        self.progress = (
            game.progress
        )

        self.current_location = (
            self.progress.next_level
        )

        # Segurança caso algum password
        # venha com localização inválida.
        if (
            self.current_location
            not in MAP_LOCATIONS
        ):

            self.current_location = 1

            self.progress.next_level = 1


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
                ]["position"]
            )
        )

        self.travel_speed = 380


        # =================================================
        # FONTS
        # =================================================

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


        # =================================================
        # OPTIONAL LOCATION IMAGES
        # =================================================

        self.location_images = {}

        for (
            location_id,
            data
        ) in MAP_LOCATIONS.items():

            sprite_name = (
                data.get("sprite")
            )

            if not sprite_name:
                continue

            path = (
                ASSETS_DIR
                / "map"
                / sprite_name
            )

            if not path.exists():
                continue

            image = (
                pygame.image.load(
                    str(path)
                ).convert_alpha()
            )

            image = (
                pygame.transform.smoothscale(
                    image,
                    (40, 40)
                )
            )

            self.location_images[
                location_id
            ] = image


        # =================================================
        # OPTIONAL SHIP IMAGE
        # =================================================

        self.ship_image = None

        ship_path = (
            ASSETS_DIR
            / "map"
            / "map_ship.png"
        )

        if ship_path.exists():

            image = (
                pygame.image.load(
                    str(ship_path)
                ).convert_alpha()
            )

            self.ship_image = (
                pygame.transform.smoothscale(
                    image,
                    (34, 34)
                )
            )


        # =================================================
        # CLICK AREAS
        # =================================================

        self.node_rects = {}

        self.market_rects = {}


        self.start_rect = pygame.Rect(
            430,
            600,
            250,
            44
        )

        self.market_button_rect = (
            pygame.Rect(
                40,
                600,
                175,
                44
            )
        )

        self.loadout_button_rect = (
            pygame.Rect(
                225,
                600,
                190,
                44
            )
        )


    # =====================================================
    # GRAPH
    # =====================================================

    def get_neighbors(self, location):

        neighbors = []

        for a, b in MAP_CONNECTIONS:

            if a == location:

                neighbors.append(b)

            elif b == location:

                neighbors.append(a)

        return neighbors


    def can_travel_to(self, target):

        if (
            target
            == self.current_location
        ):

            return True

        if not (
            self.progress
            .is_discovered(
                target
            )
        ):

            return False

        # O mapa continua exigindo
        # viagens entre nós conectados.
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
                data["location"]
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

        # Já está ali.
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


    def arrive(self):

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

    def start_level(self):

        if self.moving:
            return

        self.game.start_location(
            self.current_location
        )


    # =====================================================
    # MARKET
    # =====================================================

    def open_market(self):

        if self.moving:
            return

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

    def handle_event(self, event):

        # =================================================
        # KEYBOARD
        # =================================================

        if (
            event.type
            == pygame.KEYDOWN
        ):

            if (
                event.key
                == pygame.K_RETURN
            ):

                self.start_level()

                return


            if (
                event.key
                == pygame.K_m
            ):

                self.open_market()

                return


            if (
                event.key
                == pygame.K_l
            ):

                if not self.moving:

                    self.game.show_loadout()

                return


            if (
                event.key
                == pygame.K_ESCAPE
            ):

                self.game.show_menu()

                return


        # =================================================
        # MOUSE
        # =================================================

        if (
            event.type
            == pygame.MOUSEBUTTONDOWN

            and event.button == 1
        ):

            if self.moving:
                return


            # =============================================
            # MAP NODES
            # =============================================

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


            # =============================================
            # MARKET ICONS
            # =============================================

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


            # =============================================
            # BOTTOM BUTTONS
            # =============================================

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

                return


            if (
                self.loadout_button_rect
                .collidepoint(
                    event.pos
                )
            ):

                self.game.show_loadout()

                return


    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        if not self.moving:
            return


        destination = (
            pygame.Vector2(
                MAP_LOCATIONS[
                    self.travel_target
                ]["position"]
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


        if distance <= step:

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
    # DRAW STARFIELD
    # =====================================================

    def draw_starfield(self, screen):

        # Determinístico.
        # Não pisca a cada frame.
        for i in range(75):

            x = (
                i * 97
            ) % SCREEN_WIDTH

            y = (
                i * 53
            ) % 565

            radius = (
                2
                if i % 11 == 0
                else 1
            )

            pygame.draw.circle(
                screen,
                (
                    90,
                    115,
                    145
                ),
                (
                    x,
                    y
                ),
                radius
            )


    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        screen.fill(
            (
                5,
                10,
                20
            )
        )


        self.draw_starfield(
            screen
        )


        # =================================================
        # TITLE
        # =================================================

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
                    30
                )
            )
        )


        # =================================================
        # CONNECTIONS
        # =================================================

        for a, b in MAP_CONNECTIONS:

            # Rota só aparece quando
            # os dois pontos foram revelados.
            if not (
                self.progress
                .is_discovered(a)
            ):

                continue

            if not (
                self.progress
                .is_discovered(b)
            ):

                continue


            pygame.draw.line(
                screen,
                (
                    70,
                    105,
                    125
                ),
                MAP_LOCATIONS[a][
                    "position"
                ],
                MAP_LOCATIONS[b][
                    "position"
                ],
                2
            )


        self.node_rects.clear()

        self.market_rects.clear()


        # =================================================
        # LOCATIONS
        # =================================================

        for (
            location,
            data
        ) in MAP_LOCATIONS.items():

            if not (
                self.progress
                .is_discovered(
                    location
                )
            ):

                continue


            position = (
                data["position"]
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


            # =============================================
            # OPTIONAL IMAGE
            # =============================================

            if (
                location
                in self.location_images
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


            # =============================================
            # ICON FALLBACK
            # =============================================

            else:

                if (
                    location
                    == self.current_location
                ):

                    color = (
                        255,
                        225,
                        110
                    )

                elif completed:

                    color = (
                        100,
                        220,
                        165
                    )

                elif accessible:

                    color = (
                        210,
                        190,
                        100
                    )

                else:

                    color = (
                        95,
                        115,
                        125
                    )


                pygame.draw.circle(
                    screen,
                    color,
                    position,
                    10
                )


                pygame.draw.circle(
                    screen,
                    (
                        230,
                        230,
                        215
                    ),
                    position,
                    10,
                    1
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
            ] = rect.inflate(
                12,
                12
            )


            # =============================================
            # LABEL
            # =============================================

            label = (
                self.small_font.render(
                    data["name"],
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
                        position[1] + 28
                    )
                )
            )


            # =============================================
            # MARKET ICON
            # =============================================

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
                    position[0] + 19,
                    position[1] - 17
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
                ] = market_rect


        # =================================================
        # PLAYER SHIP
        # =================================================

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

            x = round(
                self.ship_position.x
            )

            y = round(
                self.ship_position.y
            )


            # Nave simples tipo ponteiro.
            pygame.draw.polygon(
                screen,
                (
                    235,
                    240,
                    235
                ),
                [
                    (x, y - 14),
                    (x - 9, y + 9),
                    (x, y + 5),
                    (x + 9, y + 9)
                ]
            )


        # =================================================
        # CURRENT LOCATION
        # =================================================

        current_name = (
            MAP_LOCATIONS[
                self.current_location
            ]["name"]
        )


        info = (
            self.font.render(
                (
                    "LOCATION: "
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
                565
            )
        )


        chips = (
            self.small_font.render(
                (
                    "NAV CHIPS: "
                    f"{self.progress.nav_chips}"
                ),
                True,
                (
                    100,
                    220,
                    235
                )
            )
        )

        screen.blit(
            chips,
            (
                530,
                570
            )
        )


        # =================================================
        # MARKET BUTTON
        # =================================================

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
            self.small_font.render(
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
                self.market_button_rect.center
            )
        )


        # =================================================
        # LOADOUT BUTTON
        # =================================================

        pygame.draw.rect(
            screen,
            (
                55,
                70,
                72
            ),
            self.loadout_button_rect,
            border_radius=6
        )


        text = (
            self.small_font.render(
                "LOADOUT [L]",
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
                self.loadout_button_rect.center
            )
        )


        # =================================================
        # START BUTTON
        # =================================================

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
            self.small_font.render(
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