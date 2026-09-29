import random
import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
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


        self.config = config


        self.normal_image = image


        # Imagem clara usada ao tomar dano.
        self.flash_image = (
            image.copy()
        )


        self.flash_image.fill(
            (
                130,
                130,
                130,
                0
            ),
            special_flags=
            pygame.BLEND_RGBA_ADD
        )


        self.image = (
            self.normal_image
        )


        self.rect = (
            self.image.get_rect()
        )


        self.shot_image = (
            shot_image
        )


        self.hp = (
            config["hp"]
        )


        self.reward = (
            config["reward"]
        )


        self.hit_flash_timer = 0


        self.movement_name = (
            config["movement"]
        )


        self.direction = (
            random.choice(
                [-1, 1]
            )
        )


        self.speed = (
            random.uniform(
                config[
                    "min_speed"
                ],
                config[
                    "max_speed"
                ]
            )
        )


        self.vertical_speed = (
            random.uniform(
                -30,
                30
            )
        )


        y = random.randint(
            90,
            int(
                SCREEN_HEIGHT
                * 0.60
            )
        )


        if self.direction == 1:

            x = (
                -self.rect.width
            )

        else:

            x = (
                SCREEN_WIDTH
                + self.rect.width
            )


        self.position = (
            pygame.Vector2(
                x,
                y
            )
        )


        self.rect.center = (
            self.position
        )


        self.fire_timer = (
            random.uniform(
                config[
                    "min_fire_time"
                ],
                config[
                    "max_fire_time"
                ]
            )
        )


    def update(
        self,
        dt
    ):

        movement = (
            MOVEMENT_PATTERNS[
                self.movement_name
            ]
        )


        movement(
            self,
            dt
        )


        self.fire_timer -= dt


        if (
            self.hit_flash_timer
            > 0
        ):

            self.hit_flash_timer -= (
                dt
            )


            self.image = (
                self.flash_image
            )

        else:

            self.image = (
                self.normal_image
            )


        if (
            self.direction == 1
            and self.rect.left
            > SCREEN_WIDTH
        ):

            self.kill()


        elif (
            self.direction == -1
            and self.rect.right
            < 0
        ):

            self.kill()


    def can_shoot(
        self
    ):

        return (
            self.fire_timer <= 0
        )


    def shoot(
        self
    ):

        self.fire_timer = (
            random.uniform(
                self.config[
                    "min_fire_time"
                ],
                self.config[
                    "max_fire_time"
                ]
            )
        )


        return Projectile(

            image=
            self.shot_image,

            x=
            self.rect.centerx,

            y=
            self.rect.bottom,

            velocity_x=0,

            velocity_y=
            self.config[
                "shot_speed"
            ],

            damage=
            self.config[
                "damage"
            ],

            owner=
            "enemy"
        )


    def take_damage(
        self,
        damage
    ):

        self.hp -= damage


        self.hit_flash_timer = (
            ENEMY_HIT_FLASH_TIME
        )


        return (
            self.hp <= 0
        )