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
        config
    ):

        super().__init__()


        self.normal_image = (
            image
        )


        self.image = (
            image.copy()
        )


        self.shot_image = (
            shot_image
        )


        self.config = (
            config
        )


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


        self.position = (
            pygame.Vector2(

                random.randint(
                    60,
                    SCREEN_WIDTH - 60
                ),

                -60
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
            random.uniform(
                80,
                150
            )
        )


        self.horizontal_direction = (
            random.choice(
                [-1, 1]
            )
        )


        self.movement_time = (
            random.random()
            * 10
        )


        self.fire_timer = (
            self.get_fire_delay()
        )


        self.flash_timer = 0

        self.stun_timer = 0


        self.is_boss = False


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


    def update(
        self,
        dt
    ):

        if self.flash_timer > 0:

            self.flash_timer -= dt


        if self.stun_timer > 0:

            self.stun_timer -= dt

            return


        self.position.y += (
            self.vertical_speed
            * dt
        )


        pattern = (
            MOVEMENT_PATTERNS.get(
                self.config[
                    "movement"
                ]
            )
        )


        if pattern:

            pattern(
                self,
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


        self.fire_timer -= (
            dt
        )


        if (
            self.rect.top
            > PLAY_AREA_BOTTOM
            + 70
        ):

            self.kill()


    def can_shoot(
        self
    ):

        return (

            self.stun_timer <= 0

            and self.fire_timer <= 0

            and self.rect.top > 0

            and self.rect.bottom
            < PLAY_AREA_BOTTOM
        )


    def shoot(
        self
    ):

        self.fire_timer = (
            self.get_fire_delay()
        )


        return Projectile(

            image=
            self.shot_image,

            center=
            self.rect.midbottom,

            velocity=(
                0,
                self.config[
                    "shot_speed"
                ]
            ),

            damage=
            self.damage,

            owner=
            "enemy"
        )


    def stun(
        self,
        duration
    ):

        self.stun_timer = max(

            self.stun_timer,

            duration
        )


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