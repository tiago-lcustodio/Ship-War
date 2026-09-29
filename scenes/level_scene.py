import random
import re
import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAY_AREA_BOTTOM,
    ASSETS_DIR,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    EXPLOSION_SIZE,
    BACKGROUND_SPEED,
    SLOW_BACKGROUND_EXTRA_HEIGHT,
    LEVEL_INTRO_DURATION,
    NAV_CORE_MESSAGE_TIME,
    BOSS_THREAT_TIME,
    SHAKE_PLAYER_HIT,
    SHAKE_EXPLOSION
)

from game_data import (
    ENEMY_TYPES,
    SHIPS,
    BOSS_TYPES,
    NEXT_MAINLINE,
    SECRET_ROUTES,
    ROUTE_ITEM_BITS,
    ROUTE_ITEM_NAMES,
    COMMON_DROP_CHANCE,
    COMMON_DROPS,
    ROUTE_DROP_BY_LEVEL
)

from password_system import (
    GameProgress
)

from entities.player import (
    Player
)

from entities.enemy import (
    Enemy
)

from entities.explosion import (
    Explosion
)

from entities.hit_spark import (
    HitSpark
)

from entities.nav_core_piece import (
    NavCorePiece
)

from entities.pickup import (
    Pickup
)

from ui.hud import (
    RetroHUD
)

from scenes.level_complete_scene import (
    LevelCompleteScene
)

from scenes.game_over_scene import (
    GameOverScene
)


class LevelScene:

    def __init__(
        self,
        game,
        progress,
        level_config
    ):

        self.game = game

        self.sound = (
            game.sound
        )


        self.config = (
            level_config
        )


        self.level_number = (
            self.config[
                "number"
            ]
        )


        # ==================================
        # FIRST CLEAR?
        # ==================================

        self.first_play = (
            not progress
            .is_completed(
                self.level_number
            )
        )


        self.environment = (
            self.config[
                "environment"
            ]
        )


        self.boss_id = (
            self.config[
                "boss"
            ]
        )


        self.background_mode = (
            self.config.get(
                "background_mode",
                "scroll"
            )
        )


        self.background_speed = (
            self.config.get(
                "background_speed",
                BACKGROUND_SPEED
            )
        )


        self.starting_progress = (
            GameProgress(

                next_level=
                self.level_number,

                money=
                progress.money,

                max_hp=
                progress.max_hp,

                continues=
                progress.continues,

                primary_weapon=
                progress.primary_weapon,

                flags=
                progress.flags,

                ship_id=
                progress.ship_id,

                nav_core_parts=
                progress.nav_core_parts,

                completed_mask=
                progress.completed_mask,

                discovered_mask=
                progress.discovered_mask,

                route_items_mask=
                progress.route_items_mask
            )
        )


        self.load_assets()

        self.hud = (
            RetroHUD()
        )


        self.reset()


    # =====================================================
    # ASSETS
    # =====================================================

    def load_assets(
        self
    ):

        # ==================================
        # PLAYER
        # ==================================

        ship_config = (
            SHIPS[
                self.starting_progress
                .ship_id
            ]
        )


        requested = (
            ASSETS_DIR
            / "player"
            / ship_config[
                "sprite"
            ]
        )


        fallback = (
            ASSETS_DIR
            / "player"
            / "player.png"
        )


        ship_path = (
            requested
            if requested.exists()
            else fallback
        )


        image = (
            pygame.image.load(
                str(ship_path)
            ).convert_alpha()
        )


        self.player_image = (
            pygame.transform.smoothscale(
                image,
                (
                    PLAYER_WIDTH,
                    PLAYER_HEIGHT
                )
            )
        )


        # ==================================
        # PLAYER SHOT
        # ==================================

        image = (
            pygame.image.load(
                str(
                    ASSETS_DIR
                    / "shots"
                    / "shot_player.png"
                )
            ).convert_alpha()
        )


        self.player_shot_image = (
            pygame.transform.smoothscale(
                image,
                (
                    12,
                    30
                )
            )
        )


        # ==================================
        # ENEMY SHOT
        # ==================================

        image = (
            pygame.image.load(
                str(
                    ASSETS_DIR
                    / "shots"
                    / "shot_enemy.png"
                )
            ).convert_alpha()
        )


        image = (
            pygame.transform.smoothscale(
                image,
                (
                    12,
                    28
                )
            )
        )


        self.enemy_shot_image = (
            pygame.transform.rotate(
                image,
                180
            )
        )


        # ==================================
        # ENEMIES
        # ==================================

        self.enemy_images = {}


        for enemy_id in (
            self.config[
                "enemy_types"
            ]
        ):

            enemy_config = (
                ENEMY_TYPES[
                    enemy_id
                ]
            )


            image = (
                pygame.image.load(
                    str(
                        ASSETS_DIR
                        / "enemies"
                        / enemy_config[
                            "sprite"
                        ]
                    )
                ).convert_alpha()
            )


            image = (
                pygame.transform.smoothscale(
                    image,
                    (
                        enemy_config[
                            "width"
                        ],
                        enemy_config[
                            "height"
                        ]
                    )
                )
            )


            self.enemy_images[
                enemy_id
            ] = image


        # ==================================
        # BOSS
        # ==================================

        self.boss_image = None


        if (
            self.boss_id
            and self.boss_id
            in BOSS_TYPES
        ):

            boss_config = (
                BOSS_TYPES[
                    self.boss_id
                ]
            )


            boss_path = (
                ASSETS_DIR
                / "enemies"
                / boss_config[
                    "sprite"
                ]
            )


            if boss_path.exists():

                image = (
                    pygame.image.load(
                        str(boss_path)
                    ).convert_alpha()
                )

            else:

                # Fallback para primeiro inimigo.
                first_enemy = (
                    self.config[
                        "enemy_types"
                    ][0]
                )


                image = (
                    self.enemy_images[
                        first_enemy
                    ]
                )


            self.boss_image = (
                pygame.transform.smoothscale(
                    image,
                    (
                        boss_config[
                            "width"
                        ],
                        boss_config[
                            "height"
                        ]
                    )
                )
            )


        # ==================================
        # EXPLOSIONS
        # ==================================

        self.explosion_frames = []


        for number in range(
            1,
            4
        ):

            image = (
                pygame.image.load(
                    str(
                        ASSETS_DIR
                        / "explosions"
                        / (
                            f"explosion_"
                            f"{number}.png"
                        )
                    )
                ).convert_alpha()
            )


            image = (
                pygame.transform.smoothscale(
                    image,
                    (
                        EXPLOSION_SIZE,
                        EXPLOSION_SIZE
                    )
                )
            )


            self.explosion_frames.append(
                image
            )


        # ==================================
        # BACKGROUND
        # ==================================

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


        raw_background = (
            pygame.image.load(
                str(path)
            ).convert()
        )


        if (
            self.background_mode
            == "scroll"
        ):

            self.background = (
                pygame.transform.smoothscale(
                    raw_background,
                    (
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT
                    )
                )
            )


        elif (
            self.background_mode
            == "slow_scroll"
        ):

            self.background = (
                pygame.transform.smoothscale(
                    raw_background,
                    (
                        SCREEN_WIDTH,

                        SCREEN_HEIGHT
                        + SLOW_BACKGROUND_EXTRA_HEIGHT
                    )
                )
            )


        else:

            self.background = (
                pygame.transform.smoothscale(
                    raw_background,
                    (
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT
                    )
                )
            )


    # =====================================================
    # RESET
    # =====================================================

    def reset(
        self
    ):

        ship_config = (
            SHIPS[
                self.starting_progress
                .ship_id
            ]
        )


        max_hp = max(

            self.starting_progress
            .max_hp,

            ship_config[
                "base_hp"
            ]
        )


        self.player = Player(

            image=
            self.player_image,

            shot_image=
            self.player_shot_image,

            ship_config=
            ship_config,

            max_hp=
            max_hp,

            money=
            self.starting_progress
            .money
        )


        self.enemies = (
            pygame.sprite.Group()
        )

        self.player_shots = (
            pygame.sprite.Group()
        )

        self.enemy_shots = (
            pygame.sprite.Group()
        )

        self.explosions = (
            pygame.sprite.Group()
        )

        self.hit_sparks = (
            pygame.sprite.Group()
        )

        self.nav_core_items = (
            pygame.sprite.Group()
        )

        self.pickups = (
            pygame.sprite.Group()
        )


        # ==================================
        # BACKGROUND
        # ==================================

        self.background_y1 = 0

        self.background_y2 = (
            -SCREEN_HEIGHT
        )


        self.slow_background_y = (
            -SLOW_BACKGROUND_EXTRA_HEIGHT
        )


        # ==================================
        # LEVEL
        # ==================================

        self.state = "intro"

        self.state_timer = 0

        self.level_timer = 0

        self.death_timer = 0

        self.spawn_timer = 1.0


        self.enemies_destroyed = 0


        self.money_at_start = (
            self.player.money
        )


        self.shake_timer = 0

        self.shake_strength = 0


        # ==================================
        # NAV CORE
        # ==================================

        self.core_piece_number = (
            self.config[
                "nav_core_piece"
            ]
        )


        self.core_piece_spawned = False

        self.core_piece_collected = False


        if (
            self.core_piece_number
            is not None

            and self.starting_progress
            .nav_core_parts
            >= self.core_piece_number
        ):

            self.core_piece_collected = (
                True
            )


        self.core_message = ""

        self.core_message_timer = 0


        # ==================================
        # ROUTE DISCOVERY
        # ==================================

        self.secret_target = None

        self.exit_reason = (
            "normal"
        )


        # ==================================
        # BOSS
        # ==================================

        self.boss_spawned = False

        self.boss_defeated = False

        self.boss_sprite = None


        self.boss_threat_text = ""

        self.boss_threat_timer = 0


        # Boss existe apenas na primeira clear.
        self.should_have_boss = (

            self.first_play

            and self.boss_id

            and self.boss_id
            in BOSS_TYPES
        )


        # ==================================
        # PAUSE
        # ==================================

        self.paused = False

        self.pause_selected = 0


        self.pause_options = [
            "CONTINUE",
            "QUIT"
        ]


        # ==================================
        # TERMINAL
        # ==================================

        self.terminal_open = False

        self.terminal_text = ""

        self.terminal_message = ""

        self.jump_target = None


        # ==================================
        # FONTS
        # ==================================

        self.medium_font = (
            pygame.font.SysFont(
                "couriernew",
                38,
                bold=True
            )
        )


        self.pause_font = (
            pygame.font.SysFont(
                "couriernew",
                27,
                bold=True
            )
        )


        self.terminal_font = (
            pygame.font.SysFont(
                "couriernew",
                17,
                bold=True
            )
        )


        self.message_font = (
            pygame.font.SysFont(
                "couriernew",
                27,
                bold=True
            )
        )


        self.sound.play(
            "level_start"
        )


    # =====================================================
    # ROUTE ITEM HELPERS
    # =====================================================

    def has_route_item(
        self,
        item_name
    ):

        bit = (
            ROUTE_ITEM_BITS[
                item_name
            ]
        )


        return (
            self.game.progress
            .has_route_item_bit(
                bit
            )
        )


    def add_route_item(
        self,
        item_name
    ):

        bit = (
            ROUTE_ITEM_BITS[
                item_name
            ]
        )


        self.game.progress.add_route_item_bit(
            bit
        )


        self.starting_progress.route_items_mask = (
            self.game.progress
            .route_items_mask
        )


    def consume_route_item(
        self,
        item_name
    ):

        bit = (
            ROUTE_ITEM_BITS[
                item_name
            ]
        )


        self.game.progress.consume_route_item_bit(
            bit
        )


        self.starting_progress.route_items_mask = (
            self.game.progress
            .route_items_mask
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


        # ==================================
        # TERMINAL
        # ==================================

        if self.terminal_open:

            if (
                event.key
                == pygame.K_ESCAPE
            ):

                self.terminal_open = (
                    False
                )

                return


            if (
                event.key
                == pygame.K_BACKSPACE
            ):

                self.terminal_text = (
                    self.terminal_text[:-1]
                )

                return


            if (
                event.key
                == pygame.K_RETURN
            ):

                self.execute_terminal_command()

                return


            if (
                event.unicode
                and event.unicode.isprintable()
            ):

                self.terminal_text += (
                    event.unicode
                )


            return


        # ==================================
        # PAUSE
        # ==================================

        if self.paused:

            if (
                event.key
                == pygame.K_t

                and (
                    event.mod
                    & pygame.KMOD_CTRL
                )
            ):

                self.terminal_open = (
                    True
                )

                self.terminal_text = ""

                self.terminal_message = ""

                return


            if (
                event.key
                == pygame.K_ESCAPE
            ):

                self.paused = False

                return


            if (
                event.key
                == pygame.K_UP
            ):

                self.pause_selected = (
                    self.pause_selected - 1
                ) % len(
                    self.pause_options
                )

                return


            if (
                event.key
                == pygame.K_DOWN
            ):

                self.pause_selected = (
                    self.pause_selected + 1
                ) % len(
                    self.pause_options
                )

                return


            if event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                option = (
                    self.pause_options[
                        self.pause_selected
                    ]
                )


                if option == "CONTINUE":

                    self.paused = False


                else:

                    self.game.show_map()


                return


            return


        # ==================================
        # SECRET ROUTE — TAB
        # ==================================

        if (
            event.key
            == pygame.K_TAB

            and self.state
            == "playing"
        ):

            self.try_secret_route()

            return


        # ==================================
        # PAUSE
        # ==================================

        if (
            event.key
            == pygame.K_ESCAPE
        ):

            if self.state in (
                "intro",
                "playing"
            ):

                self.paused = (
                    True
                )


    # =====================================================
    # CHEATS
    # =====================================================

    def execute_terminal_command(
        self
    ):

        command = (
            self.terminal_text.strip()
        )


        # ==================================
        # MONEY
        # ==================================

        if (
            command
            == "need money"
        ):

            self.player.money += (
                100000
            )


            self.starting_progress.money = (
                self.player.money
            )


            self.game.progress.money = (
                self.player.money
            )


            self.terminal_message = (
                "+100000 CREDITS"
            )


            self.terminal_text = ""

            return


        # ==================================
        # JUMP
        # ==================================

        match = re.fullmatch(

            r"jump to level (1[0-4]|[1-9])",

            command
        )


        if match:

            target = int(
                match.group(1)
            )


            self.game.progress.discover(
                target
            )


            self.game.progress.next_level = (
                target
            )


            self.jump_target = (
                target
            )


            self.terminal_open = False

            self.paused = False


            self.exit_reason = (
                "jump"
            )


            self.start_level_exit(
                force=True
            )

            return


        self.terminal_message = (
            "UNKNOWN COMMAND"
        )


        self.terminal_text = ""


    # =====================================================
    # SECRET ROUTES
    # =====================================================

    def try_secret_route(
        self
    ):

        route = (
            SECRET_ROUTES.get(
                self.level_number
            )
        )


        if route is None:

            self.core_message = (
                "NO HIDDEN ROUTE DETECTED"
            )


            self.core_message_timer = (
                2.0
            )

            return


        target = (
            route[
                "target"
            ]
        )


        if (
            self.game.progress
            .is_discovered(
                target
            )
        ):

            self.core_message = (
                "ROUTE ALREADY KNOWN"
            )


            self.core_message_timer = (
                2.0
            )

            return


        item_name = (
            route[
                "item"
            ]
        )


        if not self.has_route_item(
            item_name
        ):

            self.core_message = (
                "NAVIGATION ITEM REQUIRED"
            )


            self.core_message_timer = (
                2.0
            )

            return


        # Consome item.
        self.consume_route_item(
            item_name
        )


        # Revela destino.
        self.game.progress.discover(
            target
        )


        self.starting_progress.discovered_mask = (
            self.game.progress
            .discovered_mask
        )


        self.secret_target = (
            target
        )


        self.exit_reason = (
            "secret_route"
        )


        self.core_message = (
            route[
                "message"
            ]
        )


        self.core_message_timer = (
            2.0
        )


        # Mesma animação de saída da fase.
        self.start_level_exit(
            force=True
        )


    # =====================================================
    # BOSS
    # =====================================================

    def spawn_boss(
        self
    ):

        if not self.should_have_boss:

            return


        if self.boss_spawned:

            return


        boss_config = (
            BOSS_TYPES[
                self.boss_id
            ]
        )


        boss = Enemy(

            image=
            self.boss_image,

            shot_image=
            self.enemy_shot_image,

            config=
            boss_config
        )


        boss.is_boss = True


        self.enemies.add(
            boss
        )


        self.boss_sprite = (
            boss
        )


        self.boss_spawned = True


        self.boss_threat_text = (
            boss_config[
                "threat"
            ]
        )


        self.boss_threat_timer = (
            BOSS_THREAT_TIME
        )


    # =====================================================
    # NAV CORE
    # =====================================================

    def spawn_nav_core_piece(
        self
    ):

        if (
            self.core_piece_number
            is None
        ):

            return


        if self.core_piece_spawned:

            return


        if self.core_piece_collected:

            return


        x = (
            random.randint(
                180,
                SCREEN_WIDTH - 180
            )
        )


        y = int(
            PLAY_AREA_BOTTOM
            * 0.45
        )


        piece = (
            NavCorePiece(
                (
                    x,
                    y
                )
            )
        )


        self.nav_core_items.add(
            piece
        )


        self.core_piece_spawned = (
            True
        )


    def check_nav_core_collision(
        self
    ):

        for piece in list(
            self.nav_core_items
        ):

            if (
                piece.rect
                .colliderect(
                    self.player.hitbox
                )
            ):

                piece.kill()


                self.core_piece_collected = (
                    True
                )


                self.starting_progress.nav_core_parts = max(

                    self.starting_progress
                    .nav_core_parts,

                    self.core_piece_number
                )


                self.game.progress.nav_core_parts = (
                    self.starting_progress
                    .nav_core_parts
                )


                self.core_message = (
                    "GOT IT!"
                )


                self.core_message_timer = (
                    NAV_CORE_MESSAGE_TIME
                )


                self.sound.play(
                    "pickup"
                )


    # =====================================================
    # DROPS
    # =====================================================

    def spawn_drop(
        self,
        center
    ):

        # ==================================
        # ROUTE ITEM
        # ==================================

        route_drop = (
            ROUTE_DROP_BY_LEVEL.get(
                self.level_number
            )
        )


        if route_drop:

            item = (
                route_drop[
                    "item"
                ]
            )


            route = (
                SECRET_ROUTES.get(
                    self.level_number
                )
            )


            target_known = False


            if route:

                target_known = (
                    self.game.progress
                    .is_discovered(
                        route[
                            "target"
                        ]
                    )
                )


            if (
                not self.has_route_item(
                    item
                )

                and not target_known

                and random.random()
                < route_drop[
                    "chance"
                ]
            ):

                pickup = (
                    Pickup(

                        pickup_type=
                        "route_item",

                        center=
                        center,

                        route_item=
                        item
                    )
                )


                self.pickups.add(
                    pickup
                )

                return


        # ==================================
        # COMMON DROP
        # ==================================

        if (
            random.random()
            > COMMON_DROP_CHANCE
        ):

            return


        total_weight = sum(
            item[
                "weight"
            ]
            for item
            in COMMON_DROPS
        )


        roll = (
            random.uniform(
                0,
                total_weight
            )
        )


        current = 0


        selected = (
            COMMON_DROPS[0]
        )


        for item in (
            COMMON_DROPS
        ):

            current += (
                item[
                    "weight"
                ]
            )


            if roll <= current:

                selected = item

                break


        pickup = (
            Pickup(

                pickup_type=
                selected[
                    "type"
                ],

                center=
                center,

                value=
                selected[
                    "value"
                ]
            )
        )


        self.pickups.add(
            pickup
        )


    def collect_pickups(
        self
    ):

        for pickup in list(
            self.pickups
        ):

            if not (
                pickup.rect
                .colliderect(
                    self.player.hitbox
                )
            ):

                continue


            # =================================
            # CREDITS
            # =================================

            if (
                pickup.pickup_type
                == "credits"
            ):

                self.player.money += (
                    pickup.value
                )


                self.core_message = (
                    "+100 CREDITS"
                )


            # =================================
            # HEALTH
            # =================================

            elif (
                pickup.pickup_type
                == "health"
            ):

                if (
                    self.player.hp
                    < self.player.max_hp
                ):

                    self.player.hp = min(

                        self.player.max_hp,

                        self.player.hp
                        + pickup.value
                    )


                    self.core_message = (
                        "+1 HULL"
                    )

                else:

                    self.core_message = (
                        "HULL FULL"
                    )


            # =================================
            # ROUTE ITEM
            # =================================

            elif (
                pickup.pickup_type
                == "route_item"
            ):

                self.add_route_item(
                    pickup.route_item
                )


                self.core_message = (

                    ROUTE_ITEM_NAMES[
                        pickup.route_item
                    ]

                    + " ACQUIRED"
                )


            pickup.kill()


            self.sound.play(
                "pickup"
            )


            self.core_message_timer = (
                2.0
            )


    # =====================================================
    # SCREEN SHAKE
    # =====================================================

    def add_shake(
        self,
        strength,
        duration=0.10
    ):

        self.shake_strength = max(
            self.shake_strength,
            strength
        )


        self.shake_timer = max(
            self.shake_timer,
            duration
        )


    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_background(
        self,
        dt
    ):

        if (
            self.background_mode
            == "static"
        ):

            return


        speed = (
            self.background_speed
        )


        if (
            self.state
            == "ending"

            and self.background_mode
            == "scroll"
        ):

            speed *= 4


        if (
            self.background_mode
            == "scroll"
        ):

            self.background_y1 += (
                speed * dt
            )


            self.background_y2 += (
                speed * dt
            )


            if (
                self.background_y1
                >= SCREEN_HEIGHT
            ):

                self.background_y1 = (

                    self.background_y2

                    - SCREEN_HEIGHT
                )


            if (
                self.background_y2
                >= SCREEN_HEIGHT
            ):

                self.background_y2 = (

                    self.background_y1

                    - SCREEN_HEIGHT
                )


        elif (
            self.background_mode
            == "slow_scroll"
        ):

            self.slow_background_y += (
                speed * dt
            )


            self.slow_background_y = min(
                0,
                self.slow_background_y
            )


    # =====================================================
    # SPAWN ENEMY
    # =====================================================

    def spawn_enemy(
        self
    ):

        if (
            len(self.enemies)
            >= self.config[
                "max_enemies"
            ]
        ):

            return


        enemy_id = (
            random.choice(
                self.config[
                    "enemy_types"
                ]
            )
        )


        config = (
            ENEMY_TYPES[
                enemy_id
            ]
        )


        enemy = (
            Enemy(

                image=
                self.enemy_images[
                    enemy_id
                ],

                shot_image=
                self.enemy_shot_image,

                config=
                config
            )
        )


        enemy.is_boss = False


        self.enemies.add(
            enemy
        )


    # =====================================================
    # EFFECTS
    # =====================================================

    def create_explosion(
        self,
        center
    ):

        self.explosions.add(

            Explosion(
                self.explosion_frames,
                center
            )
        )


    def create_hit_spark(
        self,
        center
    ):

        self.hit_sparks.add(

            HitSpark(
                center
            )
        )


    # =====================================================
    # START EXIT
    # =====================================================

    def start_level_exit(
        self,
        force=False
    ):

        if (
            self.state
            == "ending"
        ):

            return


        if (
            not force

            and self.core_piece_number
            is not None

            and not self.core_piece_collected
        ):

            self.core_message = (
                "GET THE NAV CORE PIECE!"
            )


            self.core_message_timer = (
                2.0
            )

            return


        if (
            not force

            and self.should_have_boss

            and not self.boss_defeated
        ):

            self.core_message = (
                "DESTROY THE BOSS!"
            )


            self.core_message_timer = (
                2.0
            )

            return


        self.state = (
            "ending"
        )


        self.enemies.empty()

        self.player_shots.empty()

        self.enemy_shots.empty()

        self.nav_core_items.empty()

        self.pickups.empty()


    # =====================================================
    # FINISH
    # =====================================================

    def finish_level(
        self
    ):

        # ==================================
        # SECRET ROUTE EXIT
        # ==================================

        if (
            self.exit_reason
            == "secret_route"
        ):

            self.game.progress.money = (
                self.player.money
            )


            self.game.progress.max_hp = (
                self.player.max_hp
            )


            self.game.progress.next_level = (
                self.level_number
            )


            self.game.show_map()

            return


        # ==================================
        # ADMIN JUMP
        # ==================================

        if (
            self.exit_reason
            == "jump"
        ):

            self.game.progress.money = (
                self.player.money
            )


            self.game.progress.next_level = (
                self.jump_target
            )


            self.game.show_map()

            return


        # ==================================
        # NORMAL COMPLETION
        # ==================================

        first_clear = (
            not self.game.progress
            .is_completed(
                self.level_number
            )
        )


        self.game.progress.mark_completed(
            self.level_number
        )


        # A fase atual é conhecida,
        # naturalmente.
        self.game.progress.discover(
            self.level_number
        )


        # Somente a campanha principal
        # libera a próxima fase automaticamente.
        next_main = (
            NEXT_MAINLINE.get(
                self.level_number
            )
        )


        if next_main:

            self.game.progress.discover(
                next_main
            )


        self.game.progress.money = (
            self.player.money
        )


        self.game.progress.max_hp = (
            self.player.max_hp
        )


        self.game.progress.ship_id = (
            self.player.ship_id
        )


        self.game.progress.nav_core_parts = (
            self.starting_progress
            .nav_core_parts
        )


        self.game.progress.next_level = (
            self.level_number
        )


        stats = {

            "enemies_destroyed":
            self.enemies_destroyed,

            "money_earned":
            (
                self.player.money
                - self.money_at_start
            )
        }


        self.game.change_scene(

            LevelCompleteScene(

                self.game,

                self.game.progress,

                self.level_number,

                stats,

                first_clear=
                first_clear
            )
        )


    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt
    ):

        if self.paused:

            return


        self.update_background(
            dt
        )


        self.explosions.update(
            dt
        )


        self.hit_sparks.update(
            dt
        )


        self.nav_core_items.update(
            dt
        )


        self.pickups.update(
            dt
        )


        if (
            self.core_message_timer
            > 0
        ):

            self.core_message_timer -= (
                dt
            )


        if (
            self.boss_threat_timer
            > 0
        ):

            self.boss_threat_timer -= (
                dt
            )


        if self.shake_timer > 0:

            self.shake_timer -= dt

        else:

            self.shake_strength = 0


        # ==================================
        # INTRO
        # ==================================

        if self.state == "intro":

            self.state_timer += dt


            if (
                self.state_timer
                >= LEVEL_INTRO_DURATION
            ):

                self.state = (
                    "playing"
                )


            return


        # ==================================
        # PLAYING
        # ==================================

        if self.state == "playing":

            self.level_timer += dt


            keys = (
                pygame.key.get_pressed()
            )


            self.player.update(
                dt,
                keys
            )


            self.enemies.update(
                dt
            )


            self.player_shots.update(
                dt
            )


            self.enemy_shots.update(
                dt
            )


            self.collect_pickups()


            # =================================
            # NAV CORE
            # =================================

            if (
                self.core_piece_number
                is not None

                and self.level_timer
                >= self.config[
                    "duration"
                ] * 0.50
            ):

                self.spawn_nav_core_piece()


            self.check_nav_core_collision()


            # =================================
            # BOSS
            # =================================

            if (
                self.should_have_boss

                and self.level_timer
                >= self.config[
                    "duration"
                ] * 0.75
            ):

                self.spawn_boss()


            # =================================
            # PLAYER SHOOT
            # =================================

            mouse = (
                pygame.mouse.get_pressed()
            )


            if mouse[0]:

                projectile = (
                    self.player.shoot()
                )


                if projectile:

                    self.player_shots.add(
                        projectile
                    )


                    self.sound.play(
                        "shot_player"
                    )


            # =================================
            # SPAWN
            # =================================

            self.spawn_timer -= dt


            if (
                self.spawn_timer
                <= 0
            ):

                self.spawn_enemy()


                self.spawn_timer = (
                    random.uniform(
                        1.5,
                        3.0
                    )
                )


            # =================================
            # ENEMY SHOOT
            # =================================

            for enemy in list(
                self.enemies
            ):

                if (
                    enemy.can_shoot()
                ):

                    projectile = (
                        enemy.shoot()
                    )


                    self.enemy_shots.add(
                        projectile
                    )


                    self.sound.play(
                        "shot_enemy"
                    )


            # =================================
            # PLAYER SHOT x ENEMY
            # =================================

            for projectile in list(
                self.player_shots
            ):

                for enemy in list(
                    self.enemies
                ):

                    if not (
                        projectile.rect
                        .colliderect(
                            enemy.rect
                        )
                    ):

                        continue


                    impact = (
                        projectile
                        .rect.center
                    )


                    projectile.kill()


                    self.create_hit_spark(
                        impact
                    )


                    self.sound.play(
                        "hit"
                    )


                    destroyed = (
                        enemy.take_damage(
                            projectile.damage
                        )
                    )


                    if destroyed:

                        center = (
                            enemy.rect.center
                        )


                        reward = (
                            enemy.reward
                        )


                        is_boss = (
                            getattr(
                                enemy,
                                "is_boss",
                                False
                            )
                        )


                        enemy.kill()


                        self.create_explosion(
                            center
                        )


                        self.sound.play(
                            "explosion"
                        )


                        self.add_shake(
                            SHAKE_EXPLOSION,
                            0.15
                        )


                        self.player.money += (
                            reward
                        )


                        self.enemies_destroyed += (
                            1
                        )


                        if is_boss:

                            self.boss_defeated = (
                                True
                            )

                        else:

                            self.spawn_drop(
                                center
                            )


                    break


            # =================================
            # ENEMY SHOT x PLAYER
            # =================================

            for projectile in list(
                self.enemy_shots
            ):

                if (
                    projectile.rect
                    .colliderect(
                        self.player.hitbox
                    )
                ):

                    projectile.kill()


                    damaged = (
                        self.player
                        .take_damage(
                            projectile.damage
                        )
                    )


                    if damaged:

                        self.create_hit_spark(
                            self.player
                            .rect.center
                        )


                        self.sound.play(
                            "player_hit"
                        )


                        self.add_shake(
                            SHAKE_PLAYER_HIT,
                            0.18
                        )


            # =================================
            # ENEMY x PLAYER
            # =================================

            for enemy in list(
                self.enemies
            ):

                if (
                    enemy.rect
                    .colliderect(
                        self.player.hitbox
                    )
                ):

                    damaged = (
                        self.player
                        .take_damage(
                            1
                        )
                    )


                    if damaged:

                        # Boss não é destruído
                        # por simples colisão.
                        if not getattr(
                            enemy,
                            "is_boss",
                            False
                        ):

                            center = (
                                enemy.rect.center
                            )


                            enemy.kill()


                            self.create_explosion(
                                center
                            )


                        self.add_shake(
                            SHAKE_PLAYER_HIT,
                            0.18
                        )


            # =================================
            # DEATH
            # =================================

            if (
                self.player.is_dead()
            ):

                self.create_explosion(
                    self.player
                    .rect.center
                )


                self.state = (
                    "dying"
                )


                self.death_timer = 0


                self.player_shots.empty()

                self.enemy_shots.empty()


                return


            # =================================
            # TIMER COMPLETE
            # =================================

            if (
                self.level_timer
                >= self.config[
                    "duration"
                ]
            ):

                self.start_level_exit()

                return


        # ==================================
        # DYING
        # ==================================

        elif self.state == "dying":

            self.death_timer += dt


            if (
                self.death_timer
                >= 1.0
            ):

                self.game.change_scene(

                    GameOverScene(

                        self.game,

                        self.starting_progress,

                        self.level_number
                    )
                )


        # ==================================
        # EXIT ANIMATION
        # ==================================

        elif self.state == "ending":

            self.player.position.y -= (
                650 * dt
            )


            self.player.rect.center = (

                round(
                    self.player
                    .position.x
                ),

                round(
                    self.player
                    .position.y
                )
            )


            if (
                self.player.rect.bottom
                < 0
            ):

                self.finish_level()


    # =====================================================
    # BACKGROUND DRAW
    # =====================================================

    def draw_background(
        self,
        surface
    ):

        if (
            self.background_mode
            == "scroll"
        ):

            surface.blit(
                self.background,
                (
                    0,
                    int(
                        self.background_y1
                    )
                )
            )


            surface.blit(
                self.background,
                (
                    0,
                    int(
                        self.background_y2
                    )
                )
            )


        elif (
            self.background_mode
            == "slow_scroll"
        ):

            surface.blit(
                self.background,
                (
                    0,
                    int(
                        self.slow_background_y
                    )
                )
            )


        else:

            surface.blit(
                self.background,
                (
                    0,
                    0
                )
            )


    # =====================================================
    # PAUSE
    # =====================================================

    def draw_pause(
        self,
        screen
    ):

        overlay = pygame.Surface(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )


        overlay.fill(
            (
                0,
                0,
                0,
                175
            )
        )


        screen.blit(
            overlay,
            (
                0,
                0
            )
        )


        pause = (
            self.medium_font.render(
                "PAUSED",
                True,
                (
                    245,
                    220,
                    150
                )
            )
        )


        screen.blit(
            pause,
            pause.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    220
                )
            )
        )


        for (
            index,
            option
        ) in enumerate(
            self.pause_options
        ):

            selected = (
                index
                == self.pause_selected
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
                self.pause_font.render(
                    prefix + option,
                    True,
                    color
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        320
                        + index * 55
                    )
                )
            )


    # =====================================================
    # TERMINAL
    # =====================================================

    def draw_terminal(
        self,
        screen
    ):

        terminal = pygame.Surface(
            (
                SCREEN_WIDTH - 80,
                210
            ),
            pygame.SRCALPHA
        )


        terminal.fill(
            (
                5,
                12,
                8,
                245
            )
        )


        pygame.draw.rect(
            terminal,
            (
                80,
                220,
                120
            ),
            terminal.get_rect(),
            2
        )


        title = (
            self.terminal_font.render(
                "SYSTEM TERMINAL",
                True,
                (
                    80,
                    230,
                    120
                )
            )
        )


        terminal.blit(
            title,
            (
                20,
                20
            )
        )


        command = (
            self.terminal_font.render(
                (
                    "> "
                    + self.terminal_text
                    + "_"
                ),
                True,
                (
                    180,
                    250,
                    190
                )
            )
        )


        terminal.blit(
            command,
            (
                20,
                80
            )
        )


        if self.terminal_message:

            message = (
                self.terminal_font.render(
                    self.terminal_message,
                    True,
                    (
                        245,
                        220,
                        100
                    )
                )
            )


            terminal.blit(
                message,
                (
                    20,
                    130
                )
            )


        screen.blit(
            terminal,
            (
                40,
                230
            )
        )


    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen
    ):

        world = (
            pygame.Surface(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )
            )
        )


        self.draw_background(
            world
        )


        self.player_shots.draw(
            world
        )

        self.enemy_shots.draw(
            world
        )

        self.enemies.draw(
            world
        )

        self.nav_core_items.draw(
            world
        )

        self.pickups.draw(
            world
        )

        self.hit_sparks.draw(
            world
        )

        self.explosions.draw(
            world
        )


        # ==================================
        # PLAYER
        # ==================================

        if (
            self.state
            != "dying"
        ):

            draw_player = True


            if (
                self.player
                .invulnerable_timer
                > 0
            ):

                draw_player = (

                    int(
                        self.player
                        .invulnerable_timer
                        * 12
                    )

                    % 2

                    == 0
                )


            if draw_player:

                world.blit(
                    self.player.image,
                    self.player.rect
                )


        # ==================================
        # SCREEN SHAKE
        # ==================================

        offset_x = 0

        offset_y = 0


        if (
            self.shake_timer > 0

            and self.shake_strength > 0
        ):

            offset_x = (
                random.randint(
                    -self.shake_strength,
                    self.shake_strength
                )
            )


            offset_y = (
                random.randint(
                    -self.shake_strength,
                    self.shake_strength
                )
            )


        screen.fill(
            (
                0,
                0,
                0
            )
        )


        screen.blit(
            world,
            (
                offset_x,
                offset_y
            )
        )


        # ==================================
        # INTRO
        # ==================================

        if (
            self.state
            == "intro"
        ):

            text = (
                self.medium_font.render(
                    (
                        "LEVEL "
                        f"{self.level_number}"
                    ),
                    True,
                    (
                        245,
                        225,
                        170
                    )
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        110
                    )
                )
            )


        # ==================================
        # HUD
        # ==================================

        if self.state in (
            "playing",
            "ending"
        ):

            self.hud.draw(
                screen,
                self.player,
                self.level_number,
                self.starting_progress
                .nav_core_parts
            )


        # ==================================
        # MESSAGE
        # ==================================

        if (
            self.core_message_timer
            > 0
        ):

            text = (
                self.message_font.render(
                    self.core_message,
                    True,
                    (
                        120,
                        255,
                        210
                    )
                )
            )


            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        115
                    )
                )
            )


        # ==================================
        # BOSS THREAT
        # ==================================

        if (
            self.boss_threat_timer
            > 0
        ):

            threat = (
                self.message_font.render(
                    self.boss_threat_text,
                    True,
                    (
                        255,
                        90,
                        80
                    )
                )
            )


            screen.blit(
                threat,
                threat.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        155
                    )
                )
            )


        if self.paused:

            self.draw_pause(
                screen
            )


        if self.terminal_open:

            self.draw_terminal(
                screen
            )