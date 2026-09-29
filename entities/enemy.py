import math
import random
import pygame

from settings import (
    SCREEN_WIDTH,
    PLAY_AREA_BOTTOM,
    ENEMY_HIT_FLASH_TIME
)

from entities.projectile import (
    Projectile
)

from entities.movement import (
    MOVEMENT_PATTERNS
)


class Enemy(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        image,
        shot_image,
        config,
        player_ref=None,
        spawn_x=None,
        spawn_y=-60,
        movement_phase=None
    ):

        super().__init__()


        # =====================================================
        # CONFIG
        # =====================================================

        self.config = (
            config
        )


        self.player_ref = (
            player_ref
        )


        # =====================================================
        # IMAGE
        # =====================================================

        self.normal_image = (
            image.copy()
        )


        self.image = (
            self.normal_image.copy()
        )


        self.flash_image = (
            self.create_flash_image(
                self.normal_image
            )
        )


        self.shot_image = (
            shot_image
        )


        # =====================================================
        # STATS
        # =====================================================

        self.hp = (
            config[
                "hp"
            ]
        )


        self.damage = (
            config[
                "damage"
            ]
        )


        self.reward = (
            config[
                "reward"
            ]
        )


        # =====================================================
        # POSITION
        # =====================================================

        if spawn_x is None:

            spawn_x = (
                random.randint(
                    70,
                    SCREEN_WIDTH - 70
                )
            )


        self.position = (
            pygame.Vector2(
                spawn_x,
                spawn_y
            )
        )


        self.base_x = (
            self.position.x
        )


        self.rect = (
            self.image.get_rect(
                center=self.position
            )
        )


        # =====================================================
        # MOVEMENT
        # =====================================================

        self.vertical_speed = (
            random.uniform(
                config[
                    "min_speed"
                ],
                config[
                    "max_speed"
                ]
            )
        )


        self.horizontal_speed = (
            config.get(
                "horizontal_speed",
                random.uniform(
                    80,
                    140
                )
            )
        )


        self.horizontal_direction = (
            random.choice(
                [-1, 1]
            )
        )


        self.movement_time = (
            0
        )


        if (
            movement_phase is None
        ):

            movement_phase = (
                random.uniform(
                    0,
                    math.tau
                )
            )


        self.movement_phase = (
            movement_phase
        )


        # STRAFE
        self.strafe_timer = 0


        # DIVE
        self.dive_started = False

        self.dive_velocity = (
            pygame.Vector2()
        )


        # =====================================================
        # FIRE
        # =====================================================

        self.fire_timer = (
            self.get_fire_delay()
        )


        self.burst_remaining = 0

        self.burst_timer = 0


        # =====================================================
        # STATUS
        # =====================================================

        self.flash_timer = 0

        self.stun_timer = 0


        self.is_boss = False


    # =====================================================
    # FLASH IMAGE
    # =====================================================

    def create_flash_image(
        self,
        image
    ):

        flash = (
            image.copy()
        )


        flash.fill(
            (
                180,
                180,
                180,
                0
            ),
            special_flags=
            pygame.BLEND_RGBA_ADD
        )


        return flash


    # =====================================================
    # FIRE DELAY
    # =====================================================

    def get_fire_delay(
        self
    ):

        return random.uniform(

            self.config[
                "min_fire_time"
            ],

            self.config[
                "max_fire_time"
            ]
        )


    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt
    ):

        self.movement_time += (
            dt
        )


        # =================================================
        # HIT FLASH
        # =================================================

        if (
            self.flash_timer > 0
        ):

            self.flash_timer -= (
                dt
            )


            self.image = (
                self.flash_image
            )


        else:

            self.image = (
                self.normal_image
            )


        # =================================================
        # FIRE TIMERS
        # =================================================

        self.fire_timer -= (
            dt
        )


        self.burst_timer = max(
            0,
            self.burst_timer - dt
        )


        # =================================================
        # STUN
        # =================================================

        if (
            self.stun_timer > 0
        ):

            self.stun_timer -= (
                dt
            )


            self.rect.center = (

                round(
                    self.position.x
                ),

                round(
                    self.position.y
                )
            )


            return


        # =================================================
        # MOVEMENT
        # =================================================

        movement_name = (
            self.config.get(
                "movement",
                "horizontal"
            )
        )


        movement_function = (
            MOVEMENT_PATTERNS.get(
                movement_name
            )
        )


        if (
            movement_function
            is not None
        ):

            movement_function(
                self,
                dt
            )


        else:

            self.position.y += (
                self.vertical_speed
                * dt
            )


        self.rect.center = (

            round(
                self.position.x
            ),

            round(
                self.position.y
            )
        )


        # =================================================
        # OFFSCREEN
        # =================================================

        margin = 120


        if (
            self.rect.top
            > PLAY_AREA_BOTTOM
            + margin

            or self.rect.right < -margin

            or self.rect.left
            > SCREEN_WIDTH + margin
        ):

            self.kill()


    # =====================================================
    # CAN SHOOT
    # =====================================================

    def can_shoot(
        self
    ):

        if (
            self.stun_timer > 0
        ):

            return False


        if (
            self.rect.bottom <= 0

            or self.rect.top
            >= PLAY_AREA_BOTTOM
        ):

            return False


        # Burst já iniciado.
        if (
            self.burst_remaining > 0
        ):

            return (
                self.burst_timer <= 0
            )


        return (
            self.fire_timer <= 0
        )


    # =====================================================
    # PLAYER TARGET
    # =====================================================

    def get_player_center(
        self
    ):

        if (
            self.player_ref
            is None
        ):

            return pygame.Vector2(
                self.rect.centerx,
                PLAY_AREA_BOTTOM
            )


        return pygame.Vector2(
            self.player_ref
            .rect.center
        )


    # =====================================================
    # AIM VECTOR
    # =====================================================

    def aimed_velocity(
        self,
        speed,
        angle_offset=0
    ):

        start = pygame.Vector2(
            self.rect.midbottom
        )


        target = (
            self.get_player_center()
        )


        direction = (
            target
            - start
        )


        if (
            direction.length_squared()
            == 0
        ):

            direction = (
                pygame.Vector2(
                    0,
                    1
                )
            )

        else:

            direction = (
                direction.normalize()
            )


        if angle_offset != 0:

            direction = (
                direction.rotate(
                    angle_offset
                )
            )


        return (
            direction
            * speed
        )


    # =====================================================
    # CREATE SHOT
    # =====================================================

    def create_shot(
        self,
        velocity,
        offset_x=0,
        offset_y=0
    ):

        return Projectile(

            image=
            self.shot_image,

            center=(
                self.rect.centerx
                + offset_x,

                self.rect.bottom
                + offset_y
            ),

            velocity=
            velocity,

            damage=
            self.damage,

            owner=
            "enemy",

            kind=
            "enemy"
        )


    # =====================================================
    # SHOOT
    # =====================================================
    #
    # Sempre retorna uma LISTA.
    #
    # Isso permite:
    #
    # straight -> [1 tiro]
    # double   -> [2 tiros]
    # spread   -> [3 tiros]
    #
    # =====================================================

    def shoot(
        self
    ):

        pattern = (
            self.config.get(
                "shot_pattern",
                "straight"
            )
        )


        speed = (
            self.config[
                "shot_speed"
            ]
        )


        shots = []


        # =================================================
        # BURST EM ANDAMENTO
        # =================================================

        if (
            self.burst_remaining > 0
        ):

            shots.append(

                self.create_shot(
                    self.aimed_velocity(
                        speed
                    )
                )
            )


            self.burst_remaining -= 1


            if (
                self.burst_remaining > 0
            ):

                self.burst_timer = (
                    self.config.get(
                        "burst_interval",
                        0.14
                    )
                )


            else:

                self.fire_timer = (
                    self.get_fire_delay()
                )


            return shots


        # =================================================
        # STRAIGHT
        # =================================================

        if (
            pattern
            == "straight"
        ):

            shots.append(

                self.create_shot(
                    (
                        0,
                        speed
                    )
                )
            )


            self.fire_timer = (
                self.get_fire_delay()
            )


        # =================================================
        # AIMED
        # =================================================

        elif (
            pattern
            == "aimed"
        ):

            shots.append(

                self.create_shot(
                    self.aimed_velocity(
                        speed
                    )
                )
            )


            self.fire_timer = (
                self.get_fire_delay()
            )


        # =================================================
        # DOUBLE
        # =================================================

        elif (
            pattern
            == "double"
        ):

            shots.append(

                self.create_shot(
                    (
                        0,
                        speed
                    ),
                    offset_x=-10
                )
            )


            shots.append(

                self.create_shot(
                    (
                        0,
                        speed
                    ),
                    offset_x=10
                )
            )


            self.fire_timer = (
                self.get_fire_delay()
            )


        # =================================================
        # SPREAD
        # =================================================

        elif (
            pattern
            == "spread"
        ):

            angle = (
                self.config.get(
                    "spread_angle",
                    18
                )
            )


            shots.append(

                self.create_shot(
                    self.aimed_velocity(
                        speed,
                        -angle
                    )
                )
            )


            shots.append(

                self.create_shot(
                    self.aimed_velocity(
                        speed,
                        0
                    )
                )
            )


            shots.append(

                self.create_shot(
                    self.aimed_velocity(
                        speed,
                        angle
                    )
                )
            )


            self.fire_timer = (
                self.get_fire_delay()
            )


        # =================================================
        # BURST
        # =================================================

        elif (
            pattern
            == "burst"
        ):

            count = max(
                1,
                self.config.get(
                    "burst_count",
                    3
                )
            )


            # Primeiro tiro agora.
            shots.append(

                self.create_shot(
                    self.aimed_velocity(
                        speed
                    )
                )
            )


            self.burst_remaining = (
                count - 1
            )


            if (
                self.burst_remaining > 0
            ):

                self.burst_timer = (
                    self.config.get(
                        "burst_interval",
                        0.14
                    )
                )


            else:

                self.fire_timer = (
                    self.get_fire_delay()
                )


        else:

            # Fallback.
            shots.append(

                self.create_shot(
                    (
                        0,
                        speed
                    )
                )
            )


            self.fire_timer = (
                self.get_fire_delay()
            )


        return shots


    # =====================================================
    # STUN
    # =====================================================

    def stun(
        self,
        duration
    ):

        self.stun_timer = max(

            self.stun_timer,

            duration
        )


    # =====================================================
    # DAMAGE
    # =====================================================

    def take_damage(
        self,
        amount
    ):

        self.hp -= (
            amount
        )


        self.flash_timer = (
            ENEMY_HIT_FLASH_TIME
        )


        return (
            self.hp <= 0
        )