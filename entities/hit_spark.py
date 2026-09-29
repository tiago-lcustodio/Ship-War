import random
import math
import pygame

from settings import (
    HIT_SPARK_LIFETIME
)


class HitSpark(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        center
    ):

        super().__init__()


        self.lifetime = (
            HIT_SPARK_LIFETIME
        )

        self.age = 0


        self.size = 30


        self.original_image = (
            pygame.Surface(
                (
                    self.size,
                    self.size
                ),
                pygame.SRCALPHA
            )
        )


        middle = (
            self.size // 2
        )


        for _ in range(6):

            angle = random.uniform(
                0,
                math.pi * 2
            )


            length = random.randint(
                6,
                13
            )


            end_x = (
                middle
                + math.cos(angle)
                * length
            )


            end_y = (
                middle
                + math.sin(angle)
                * length
            )


            pygame.draw.line(
                self.original_image,
                (
                    255,
                    240,
                    170
                ),
                (
                    middle,
                    middle
                ),
                (
                    end_x,
                    end_y
                ),
                2
            )


        pygame.draw.circle(
            self.original_image,
            (
                255,
                255,
                220
            ),
            (
                middle,
                middle
            ),
            3
        )


        self.image = (
            self.original_image.copy()
        )


        self.rect = (
            self.image.get_rect(
                center=center
            )
        )


    def update(
        self,
        dt
    ):

        self.age += dt


        if (
            self.age
            >= self.lifetime
        ):

            self.kill()

            return


        remaining = (
            1
            - self.age
            / self.lifetime
        )


        alpha = int(
            255
            * remaining
        )


        self.image = (
            self.original_image.copy()
        )


        self.image.set_alpha(
            alpha
        )