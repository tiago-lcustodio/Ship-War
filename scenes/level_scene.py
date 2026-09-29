import random
import re
import pygame


from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAY_AREA_BOTTOM,
    ASSETS_DIR,
    PLAYER_WIDTH,
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
    COMMON_DROP_CHANCE,
    COMMON_DROPS,
    NAV_CHIP_DROP_CHANCE,
    LEVELS
)


from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from entities.explosion import Explosion
from entities.hit_spark import HitSpark
from entities.nav_core_piece import NavCorePiece
from entities.pickup import Pickup


from ui.hud import RetroHUD


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


        self.entry_progress = (
            progress.clone()
        )


        self.run_progress = (
            progress.clone()
        )


        self.first_play = (
            not self.entry_progress
            .is_completed(
                self.level_number
            )
        )


        self.is_replay = (
            not self.first_play
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


        self.load_assets()


        self.hud = (
            RetroHUD()
        )


        self.reset()


    # =====================================================
    # LOAD ASSETS
    # =====================================================

    def load_assets(self):

        # =================================================
        # PLAYER
        # =================================================

        ship_config = (
            SHIPS[
                self.run_progress.ship_id
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


        # =================================================
        # PRESERVE ASPECT RATIO
        # =================================================

        original_width = (
            image.get_width()
        )


        original_height = (
            image.get_height()
        )


        if original_width <= 0:

            original_width = 1


        aspect_ratio = (

            original_height
            / original_width
        )


        player_height = max(

            1,

            int(
                PLAYER_WIDTH
                * aspect_ratio
            )
        )


        self.player_image = (
            pygame.transform.smoothscale(
                image,
                (
                    PLAYER_WIDTH,
                    player_height
                )
            )
        )


        # =================================================
        # PLAYER SHOT
        # =================================================

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


        # =================================================
        # ENEMY SHOT
        # =================================================

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


        # =================================================
        # ENEMIES
        # =================================================

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


            enemy_path = (
                ASSETS_DIR
                / "enemies"
                / enemy_config[
                    "sprite"
                ]
            )


            image = (
                pygame.image.load(
                    str(enemy_path)
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


        # =================================================
        # BOSS
        # =================================================

        self.boss_image = None


        if (
            self.boss_id is not None

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

                first_enemy_id = (
                    self.config[
                        "enemy_types"
                    ][0]
                )


                image = (
                    self.enemy_images[
                        first_enemy_id
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


        # =================================================
        # EXPLOSIONS
        # =================================================

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


        # =================================================
        # BACKGROUND
        # =================================================

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


        background_path = (
            requested
            if requested.exists()
            else fallback
        )


        raw_background = (
            pygame.image.load(
                str(background_path)
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

    def reset(self):

        ship_config = (
            SHIPS[
                self.run_progress
                .ship_id
            ]
        )


        self.player = (
            Player(

                image=
                self.player_image,

                shot_image=
                self.player_shot_image,

                ship_config=
                ship_config,

                progress=
                self.run_progress
            )
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


        self.background_y1 = 0

        self.background_y2 = (
            -SCREEN_HEIGHT
        )


        self.slow_background_y = (
            -SLOW_BACKGROUND_EXTRA_HEIGHT
        )


        self.state = (
            "intro"
        )


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


        # =================================================
        # NAV CORE
        # =================================================

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

            and self.run_progress
            .nav_core_parts
            >= self.core_piece_number
        ):

            self.core_piece_collected = (
                True
            )


        self.core_message = ""

        self.core_message_timer = 0


        # =================================================
        # ROUTE / EXIT
        # =================================================

        self.secret_target = None

        self.exit_reason = (
            "normal"
        )


        self.jump_target = None


        # =================================================
        # BOSS
        # =================================================

        self.boss_spawned = False

        self.boss_defeated = False

        self.boss_sprite = None


        self.boss_threat_text = ""

        self.boss_threat_timer = 0


        self.should_have_boss = bool(

            self.first_play

            and self.boss_id is not None

            and self.boss_id
            in BOSS_TYPES
        )


        # =================================================
        # PAUSE
        # =================================================

        self.paused = False

        self.pause_selected = 0


        if self.is_replay:

            self.pause_options = [
                "CONTINUE",
                "LEAVE MISSION"
            ]

        else:

            self.pause_options = [
                "CONTINUE",
                "QUIT"
            ]


        # =================================================
        # TERMINAL
        # =================================================

        self.terminal_open = False

        self.terminal_text = ""

        self.terminal_message = ""


        # =================================================
        # FONTS
        # =================================================

        self.medium_font = (
            pygame.font.SysFont(
                "couriernew",
                31,
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
                24,
                bold=True
            )
        )


        self.sound.play(
            "level_start"
        )


    # =====================================================
    # MESSAGE
    # =====================================================

    def show_message(
        self,
        text,
        duration=2.0
    ):

        self.core_message = (
            text
        )

        self.core_message_timer = (
            duration
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


        # =================================================
        # TERMINAL
        # =================================================

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

                and event.unicode
                .isprintable()
            ):

                self.terminal_text += (
                    event.unicode
                )


            return


        # =================================================
        # PAUSE
        # =================================================

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

                self.paused = (
                    False
                )

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


                if (
                    option
                    == "CONTINUE"
                ):

                    self.paused = (
                        False
                    )


                elif (
                    option
                    == "LEAVE MISSION"
                ):

                    self.paused = (
                        False
                    )


                    self.exit_reason = (
                        "replay_exit"
                    )


                    self.start_level_exit(
                        force=True
                    )


                elif (
                    option
                    == "QUIT"
                ):

                    self.game.progress = (
                        self.entry_progress
                        .clone()
                    )


                    self.game.show_map()


                return


            return


        # =================================================
        # TAB ROUTE
        # =================================================

        if (
            event.key
            == pygame.K_TAB

            and self.state
            == "playing"
        ):

            self.try_secret_route()

            return


        # =================================================
        # PAUSE
        # =================================================

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
            self.terminal_text
            .strip()
        )


        # =================================================
        # MONEY
        # =================================================

        if (
            command
            == "need money"
        ):

            self.player.money += (
                100000
            )


            self.run_progress.money = (
                self.player.money
            )


            self.entry_progress.money = (
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


        # =================================================
        # COMPLETE HEALTH
        # =================================================

        if (
            command
            == "complete health"
        ):

            self.player.max_hp = 7

            self.player.hp = 7


            self.run_progress.max_hp = 7

            self.entry_progress.max_hp = 7

            self.game.progress.max_hp = 7


            self.terminal_message = (
                "HULL 7/7"
            )


            self.terminal_text = ""

            return


        # =================================================
        # JUMP
        # =================================================

        match = re.fullmatch(

            r"jump to level (1[0-4]|[1-9])",

            command
        )


        if match:

            target = int(
                match.group(1)
            )


            self.run_progress.discover(
                target
            )


            self.jump_target = (
                target
            )


            self.exit_reason = (
                "jump"
            )


            self.terminal_open = (
                False
            )

            self.paused = (
                False
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
    # SECRET ROUTE
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

            self.show_message(
                "NO HIDDEN ROUTE DETECTED"
            )

            return


        target = (
            route[
                "target"
            ]
        )


        if (
            self.run_progress
            .is_discovered(
                target
            )
        ):

            self.show_message(
                "ROUTE ALREADY KNOWN"
            )

            return


        if (
            self.run_progress
            .nav_chips <= 0
        ):

            self.show_message(
                "FORBIDDEN NAV CHIP REQUIRED"
            )

            return


        self.run_progress.nav_chips -= 1


        self.run_progress.discover(
            target
        )


        self.secret_target = (
            target
        )


        self.exit_reason = (
            "secret_route"
        )


        self.show_message(
            route[
                "message"
            ]
        )


        self.start_level_exit(
            force=True
        )


    # =====================================================
    # SHAKE
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
            self.boss_spawned

            and not self.boss_defeated
        ):

            return


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


        enemy = Enemy(

            image=
            self.enemy_images[
                enemy_id
            ],

            shot_image=
            self.enemy_shot_image,

            config=
            ENEMY_TYPES[
                enemy_id
            ]
        )


        enemy.is_boss = (
            False
        )


        self.enemies.add(
            enemy
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


        boss.is_boss = (
            True
        )


        self.enemies.add(
            boss
        )


        self.boss_sprite = (
            boss
        )


        self.boss_spawned = (
            True
        )


        for enemy in list(
            self.enemies
        ):

            if (
                enemy is not boss
            ):

                enemy.kill()


        self.boss_threat_text = (
            boss_config[
                "threat"
            ]
        )


        self.boss_threat_timer = (
            BOSS_THREAT_TIME
        )


    # =====================================================
    # CORE
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


        x = random.randint(
            180,
            SCREEN_WIDTH - 180
        )


        y = int(
            PLAY_AREA_BOTTOM
            * 0.45
        )


        piece = NavCorePiece(
            (
                x,
                y
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

            if not (
                piece.rect
                .colliderect(
                    self.player.hitbox
                )
            ):

                continue


            piece.kill()


            self.core_piece_collected = (
                True
            )


            self.run_progress.nav_core_parts = max(

                self.run_progress
                .nav_core_parts,

                self.core_piece_number
            )


            if (
                self.run_progress
                .nav_core_parts >= 3
            ):

                self.show_message(
                    (
                        "FINALLY! I DID IT! "
                        "THE CORE IS COMPLETE!"
                    ),
                    4.0
                )


            else:

                self.show_message(
                    "CORE COMPONENT ACQUIRED",
                    NAV_CORE_MESSAGE_TIME
                )


            self.sound.play(
                "pickup"
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
    # DESTROY ENEMY
    # =====================================================

    def destroy_enemy(
        self,
        enemy
    ):

        if not enemy.alive():

            return


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


        self.enemies_destroyed += 1


        if is_boss:

            self.boss_defeated = (
                True
            )


            self.show_message(
                "BOSS DESTROYED"
            )

            return


        self.spawn_drop(
            center
        )


    # =====================================================
    # DROP
    # =====================================================

    def spawn_drop(
        self,
        center
    ):

        if (
            self.level_number >= 3

            and random.random()
            < NAV_CHIP_DROP_CHANCE
        ):

            self.pickups.add(

                Pickup(
                    pickup_type=
                    "nav_chip",

                    center=
                    center
                )
            )

            return


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


        roll = random.uniform(
            0,
            total_weight
        )


        accumulated = 0


        for item in (
            COMMON_DROPS
        ):

            accumulated += (
                item[
                    "weight"
                ]
            )


            if (
                roll
                <= accumulated
            ):

                self.pickups.add(

                    Pickup(

                        pickup_type=
                        item[
                            "type"
                        ],

                        center=
                        center,

                        value=
                        item[
                            "value"
                        ]
                    )
                )

                break


    # =====================================================
    # COLLECT
    # =====================================================

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


            if (
                pickup.pickup_type
                == "credits"
            ):

                self.player.money += (
                    pickup.value
                )


                self.show_message(
                    (
                        f"+{pickup.value} "
                        "CREDITS"
                    )
                )


            elif (
                pickup.pickup_type
                == "health"
            ):

                if (
                    self.player.hp
                    < self.player.max_hp
                ):

                    self.player.heal(
                        1
                    )


                    self.show_message(
                        "+1 HULL"
                    )


                else:

                    self.show_message(
                        "HULL FULL"
                    )


            elif (
                pickup.pickup_type
                == "nav_chip"
            ):

                if (
                    self.run_progress
                    .nav_chips < 7
                ):

                    self.run_progress.nav_chips += 1


                    self.show_message(
                        "FORBIDDEN NAV CHIP"
                    )


                else:

                    self.show_message(
                        "CHIP STORAGE FULL"
                    )


            pickup.kill()


            self.sound.play(
                "pickup"
            )


    # =====================================================
    # PROJECTILE HIT
    # =====================================================

    def handle_player_projectile_hit(
        self,
        projectile,
        enemy
    ):

        if not (
            projectile.can_hit(
                enemy
            )
        ):

            return


        if (
            projectile.kind
            == "plasma_bomb"
        ):

            center = (
                projectile.rect.center
            )


            projectile.kill()


            self.detonate_plasma_bomb(

                center,

                projectile.damage,

                projectile.blast_radius
            )

            return


        projectile.register_hit(
            enemy
        )


        self.create_hit_spark(
            projectile.rect.center
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

            self.destroy_enemy(
                enemy
            )


    # =====================================================
    # PLASMA BOMB
    # =====================================================

    def detonate_plasma_bomb(
        self,
        center,
        damage,
        radius
    ):

        center_vector = (
            pygame.Vector2(
                center
            )
        )


        self.create_explosion(
            center
        )


        for enemy in list(
            self.enemies
        ):

            distance = (
                pygame.Vector2(
                    enemy.rect.center
                ).distance_to(
                    center_vector
                )
            )


            if distance > radius:

                continue


            self.create_hit_spark(
                enemy.rect.center
            )


            destroyed = (
                enemy.take_damage(
                    damage
                )
            )


            if destroyed:

                self.destroy_enemy(
                    enemy
                )


    # =====================================================
    # SECONDARY
    # =====================================================

    def use_secondary(
        self
    ):

        if not (
            self.player
            .can_use_secondary()
        ):

            return


        secondary = (
            self.player.secondary
        )


        kind = (
            secondary[
                "kind"
            ]
        )


        activated = (
            False
        )


        # =================================================
        # MISSILE
        # =================================================

        if (
            kind
            == "missile"
        ):

            if not self.enemies:

                return


            target = min(

                self.enemies,

                key=lambda enemy:

                    pygame.Vector2(
                        enemy.rect.center
                    ).distance_to(
                        self.player.rect.center
                    )
            )


            projectile = Projectile(

                image=
                self.player
                .get_secondary_shot_image(),

                center=
                self.player.rect.midtop,

                velocity=(
                    0,
                    -secondary[
                        "speed"
                    ]
                ),

                damage=
                secondary[
                    "damage"
                ],

                owner=
                "player",

                kind=
                "missile",

                target=
                target
            )


            self.player_shots.add(
                projectile
            )


            activated = (
                True
            )


        # =================================================
        # PLASMA BOMB
        # =================================================

        elif (
            kind
            == "plasma_bomb"
        ):

            projectile = Projectile(

                image=
                self.player
                .get_secondary_shot_image(),

                center=
                self.player.rect.midtop,

                velocity=(
                    0,
                    -secondary[
                        "speed"
                    ]
                ),

                damage=
                secondary[
                    "damage"
                ],

                owner=
                "player",

                kind=
                "plasma_bomb",

                blast_radius=
                secondary[
                    "radius"
                ]
            )


            self.player_shots.add(
                projectile
            )


            activated = (
                True
            )


        # =================================================
        # EMP
        # =================================================

        elif (
            kind
            == "emp"
        ):

            player_pos = (
                pygame.Vector2(
                    self.player.rect.center
                )
            )


            for enemy in list(
                self.enemies
            ):

                distance = (
                    pygame.Vector2(
                        enemy.rect.center
                    ).distance_to(
                        player_pos
                    )
                )


                if (
                    distance
                    > secondary[
                        "radius"
                    ]
                ):

                    continue


                enemy.stun(
                    secondary[
                        "stun_time"
                    ]
                )


                self.create_hit_spark(
                    enemy.rect.center
                )


                destroyed = (
                    enemy.take_damage(
                        secondary[
                            "damage"
                        ]
                    )
                )


                if destroyed:

                    self.destroy_enemy(
                        enemy
                    )


            activated = (
                True
            )


        # =================================================
        # DEFENSE BURST
        # =================================================

        elif (
            kind
            == "defense_burst"
        ):

            self.player.activate_defense_burst()


            self.show_message(
                "DEFENSE BURST"
            )


            activated = (
                True
            )


        # =================================================
        # CHAIN LIGHTNING
        # =================================================

        elif (
            kind
            == "chain_lightning"
        ):

            if not self.enemies:

                return


            player_pos = (
                pygame.Vector2(
                    self.player.rect.center
                )
            )


            candidates = [

                enemy

                for enemy
                in self.enemies

                if pygame.Vector2(
                    enemy.rect.center
                ).distance_to(
                    player_pos
                )
                <= secondary[
                    "radius"
                ]
            ]


            if not candidates:

                return


            candidates.sort(

                key=lambda enemy:

                    pygame.Vector2(
                        enemy.rect.center
                    ).distance_to(
                        player_pos
                    )
            )


            targets = (
                candidates[
                    :
                    secondary[
                        "targets"
                    ]
                ]
            )


            for enemy in targets:

                self.create_hit_spark(
                    enemy.rect.center
                )


                destroyed = (
                    enemy.take_damage(
                        secondary[
                            "damage"
                        ]
                    )
                )


                if destroyed:

                    self.destroy_enemy(
                        enemy
                    )


            self.show_message(
                "CHAIN LIGHTNING"
            )


            activated = (
                True
            )


        if activated:

            self.player.consume_secondary_cooldown()


            self.sound.play(
                "shot_player"
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

            self.show_message(
                "GET THE NAV CORE PIECE!"
            )

            return


        if (
            not force

            and self.should_have_boss

            and not self.boss_defeated
        ):

            self.show_message(
                "DESTROY THE BOSS!"
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

        self.run_progress.money = (
            self.player.money
        )


        self.run_progress.max_hp = (
            self.player.max_hp
        )


        # =================================================
        # REPLAY EARLY EXIT
        # =================================================
        #
        # Faz animação bonita,
        # mas não salva farm incompleto.
        #
        # =================================================

        if (
            self.exit_reason
            == "replay_exit"
        ):

            self.game.progress = (
                self.entry_progress
                .clone()
            )


            self.game.show_map()

            return


        # =================================================
        # SECRET ROUTE
        # =================================================

        if (
            self.exit_reason
            == "secret_route"
        ):

            self.run_progress.next_level = (
                self.level_number
            )


            self.game.progress = (
                self.run_progress
                .clone()
            )


            self.game.show_map()

            return


        # =================================================
        # ADMIN JUMP
        # =================================================

        if (
            self.exit_reason
            == "jump"
        ):

            self.run_progress.discover(
                self.jump_target
            )


            self.run_progress.next_level = (
                self.jump_target
            )


            self.game.progress = (
                self.run_progress
                .clone()
            )


            self.game.show_map()

            return


        # =================================================
        # NORMAL COMPLETION
        # =================================================

        first_clear = (
            not self.run_progress
            .is_completed(
                self.level_number
            )
        )


        self.run_progress.mark_completed(
            self.level_number
        )


        self.run_progress.discover(
            self.level_number
        )


        next_main = (
            NEXT_MAINLINE.get(
                self.level_number
            )
        )


        if next_main:

            self.run_progress.discover(
                next_main
            )


        self.run_progress.next_level = (
            self.level_number
        )


        self.game.progress = (
            self.run_progress
            .clone()
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


        if (
            self.shake_timer > 0
        ):

            self.shake_timer -= (
                dt
            )

        else:

            self.shake_strength = 0


        # =================================================
        # INTRO
        # =================================================

        if (
            self.state
            == "intro"
        ):

            self.state_timer += (
                dt
            )


            if (
                self.state_timer
                >= LEVEL_INTRO_DURATION
            ):

                self.state = (
                    "playing"
                )


            return


        # =================================================
        # PLAYING
        # =================================================

        if (
            self.state
            == "playing"
        ):

            self.level_timer += (
                dt
            )


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


            # =================================================
            # CORE
            # =================================================

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


            # =================================================
            # BOSS
            # =================================================

            if (
                self.should_have_boss

                and self.level_timer
                >= self.config[
                    "duration"
                ] * 0.75
            ):

                self.spawn_boss()


            # =================================================
            # FIRE
            # =================================================

            mouse = (
                pygame.mouse.get_pressed()
            )


            if mouse[0]:

                projectiles = (
                    self.player.shoot()
                )


                for projectile in (
                    projectiles
                ):

                    self.player_shots.add(
                        projectile
                    )


                if projectiles:

                    self.sound.play(
                        "shot_player"
                    )


            if mouse[2]:

                self.use_secondary()


            # =================================================
            # SPAWN
            # =================================================

            self.spawn_timer -= (
                dt
            )


            if (
                self.spawn_timer <= 0
            ):

                self.spawn_enemy()


                self.spawn_timer = (
                    random.uniform(
                        1.5,
                        3.0
                    )
                )


            # =================================================
            # ENEMY FIRE
            # =================================================

            for enemy in list(
                self.enemies
            ):

                if enemy.can_shoot():

                    projectile = (
                        enemy.shoot()
                    )


                    self.enemy_shots.add(
                        projectile
                    )


                    self.sound.play(
                        "shot_enemy"
                    )


            # =================================================
            # PLAYER SHOT x ENEMY
            # =================================================

            for projectile in list(
                self.player_shots
            ):

                if not projectile.alive():

                    continue


                for enemy in list(
                    self.enemies
                ):

                    if not projectile.alive():

                        break


                    if not enemy.alive():

                        continue


                    if not (
                        projectile.rect
                        .colliderect(
                            enemy.rect
                        )
                    ):

                        continue


                    self.handle_player_projectile_hit(
                        projectile,
                        enemy
                    )


            # =================================================
            # ENEMY SHOT x PLAYER
            # =================================================

            for projectile in list(
                self.enemy_shots
            ):

                if not (
                    projectile.rect
                    .colliderect(
                        self.player.hitbox
                    )
                ):

                    continue


                projectile.kill()


                damaged = (
                    self.player.take_damage(
                        projectile.damage
                    )
                )


                if damaged:

                    self.create_hit_spark(
                        self.player.rect.center
                    )


                    self.sound.play(
                        "player_hit"
                    )


                    self.add_shake(
                        SHAKE_PLAYER_HIT,
                        0.18
                    )


            # =================================================
            # ENEMY x PLAYER
            # =================================================

            for enemy in list(
                self.enemies
            ):

                if not (
                    enemy.rect
                    .colliderect(
                        self.player.hitbox
                    )
                ):

                    continue


                damaged = (
                    self.player.take_damage(
                        1
                    )
                )


                is_boss = (
                    getattr(
                        enemy,
                        "is_boss",
                        False
                    )
                )


                if not is_boss:

                    center = (
                        enemy.rect.center
                    )


                    enemy.kill()


                    self.create_explosion(
                        center
                    )


                    self.sound.play(
                        "explosion"
                    )


                if damaged:

                    self.sound.play(
                        "player_hit"
                    )


                    self.add_shake(
                        SHAKE_PLAYER_HIT,
                        0.18
                    )


            # =================================================
            # DEATH
            # =================================================

            if (
                self.player.is_dead()
            ):

                self.create_explosion(
                    self.player.rect.center
                )


                self.state = (
                    "dying"
                )


                self.death_timer = 0


                self.player_shots.empty()

                self.enemy_shots.empty()


                return


            # =================================================
            # COMPLETE TIMER
            # =================================================

            if (
                self.level_timer
                >= self.config[
                    "duration"
                ]
            ):

                self.start_level_exit()

                return


        # =================================================
        # DYING
        # =================================================

        elif (
            self.state
            == "dying"
        ):

            self.death_timer += (
                dt
            )


            if (
                self.death_timer >= 1.0
            ):

                self.game.change_scene(

                    GameOverScene(

                        self.game,

                        self.entry_progress,

                        self.level_number
                    )
                )


        # =================================================
        # EXIT
        # =================================================

        elif (
            self.state
            == "ending"
        ):

            self.player.position.y -= (
                650
                * dt
            )


            self.player.rect.center = (

                round(
                    self.player.position.x
                ),

                round(
                    self.player.position.y
                )
            )


            if (
                self.player.rect.bottom
                < 0
            ):

                self.finish_level()


    # =====================================================
    # DRAW BACKGROUND
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
    # DRAW PAUSE
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
                180
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


        hint = (
            self.terminal_font.render(
                "CTRL+T",
                True,
                (
                    90,
                    115,
                    105
                )
            )
        )


        screen.blit(
            hint,
            hint.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    470
                )
            )
        )


    # =====================================================
    # DRAW TERMINAL
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

        world = pygame.Surface(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
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


        if (
            self.state
            != "dying"
        ):

            draw_player = (
                True
            )


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


        # =================================================
        # INTRO
        # =================================================

        if (
            self.state
            == "intro"
        ):

            level_name = (
                self.config[
                    "name"
                ]
            )


            text = (
                self.medium_font.render(
                    (
                        f"LEVEL {self.level_number}"
                        " - "
                        f"{level_name}"
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


        # =================================================
        # HUD
        # =================================================

        if self.state in (
            "playing",
            "ending"
        ):

            self.hud.draw(

                screen,

                self.player,

                self.level_number,

                self.run_progress
                .nav_core_parts,

                self.run_progress
                .nav_chips
            )


        # =================================================
        # MESSAGE
        # =================================================

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


            # Caso seja muito grande,
            # reduz automaticamente.
            max_width = (
                SCREEN_WIDTH - 40
            )


            if (
                text.get_width()
                > max_width
            ):

                scale = (

                    max_width
                    / text.get_width()
                )


                new_width = (
                    max_width
                )


                new_height = max(

                    1,

                    int(
                        text.get_height()
                        * scale
                    )
                )


                text = (
                    pygame.transform.smoothscale(
                        text,
                        (
                            new_width,
                            new_height
                        )
                    )
                )


            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        100
                    )
                )
            )


        # =================================================
        # BOSS THREAT
        # =================================================

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
                        150
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