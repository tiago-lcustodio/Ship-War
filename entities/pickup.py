import math
import random
import pygame

from settings import (
    ASSETS_DIR,
    SCREEN_WIDTH,
    PLAY_AREA_BOTTOM
)


class Pickup(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        pickup_type,
        center,
        value=0
    ):

        super().__init__()


        self.pickup_type = (
            pickup_type
        )


        self.value = (
            value
        )


        self.position = (
            pygame.Vector2(
                center
            )
        )


        self.base_x = (
            self.position.x
        )


        self.time = (
            random.random()
            * 10
        )


        self.velocity_y = (
            random.uniform(
                12,
                28
            )
        )


        self.drift = (
            random.uniform(
                8,
                20
            )
        )


        self.image = (
            self.create_image()
        )


        self.rect = (
            self.image.get_rect(
                center=center
            )
        )


    def create_image(
        self
    ):

        image = pygame.Surface(
            (
                34,
                34
            ),
            pygame.SRCALPHA
        )


        if (
            self.pickup_type
            == "credits"
        ):

            color = (
                245,
                210,
                70
            )

            text = "$"


        elif (
            self.pickup_type
            == "health"
        ):

            color = (
                90,
                240,
                130
            )

            text = "+"


        else:

            # Navigation chip.
            color = (
                80,
                220,
                250
            )

            text = "N"


        pygame.draw.circle(
            image,
            color,
            (
                17,
                17
            ),
            13,
            2
        )


        font = (
            pygame.font.SysFont(
                "couriernew",
                17,
                bold=True
            )
        )


        rendered = (
            font.render(
                text,
                True,
                color
            )
        )


        image.blit(
            rendered,
            rendered.get_rect(
                center=(
                    17,
                    17
                )
            )
        )


        return image


    def update(
        self,
        dt
    ):

        self.time += dt


        self.position.y += (
            self.velocity_y
            * dt
        )


        self.position.x = (

            self.base_x

            + math.sin(
                self.time * 2
            )

            * self.drift
        )


        self.position.x = max(

            20,

            min(
                SCREEN_WIDTH - 20,
                self.position.x
            )
        )


        self.rect.center = (

            round(
                self.position.x
            ),

            round(
                self.position.y
            )
        )


        if (
            self.rect.top
            > PLAY_AREA_BOTTOM
        ):

            self.kill()