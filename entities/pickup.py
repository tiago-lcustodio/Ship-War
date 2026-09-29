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
        value=0,
        route_item=None
    ):

        super().__init__()


        self.pickup_type = (
            pickup_type
        )


        self.value = (
            value
        )


        self.route_item = (
            route_item
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
            self.load_image()
        )


        self.rect = (
            self.image.get_rect(
                center=center
            )
        )


    # =====================================================
    # IMAGE
    # =====================================================

    def load_image(
        self
    ):

        if (
            self.pickup_type
            == "credits"
        ):

            filename = (
                "pickup_credit.png"
            )


        elif (
            self.pickup_type
            == "health"
        ):

            filename = (
                "pickup_health.png"
            )


        elif (
            self.pickup_type
            == "route_item"
        ):

            filename = (
                f"{self.route_item}.png"
            )


        else:

            filename = (
                "pickup_unknown.png"
            )


        path = (
            ASSETS_DIR
            / "items"
            / filename
        )


        if path.exists():

            image = (
                pygame.image.load(
                    str(path)
                ).convert_alpha()
            )


            return (
                pygame.transform.smoothscale(
                    image,
                    (
                        34,
                        34
                    )
                )
            )


        # ==================================
        # FALLBACK
        # ==================================

        image = (
            pygame.Surface(
                (
                    34,
                    34
                ),
                pygame.SRCALPHA
            )
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

        elif (
            self.pickup_type
            == "health"
        ):

            color = (
                90,
                240,
                130
            )

        else:

            color = (
                90,
                220,
                240
            )


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


        if (
            self.pickup_type
            == "health"
        ):

            pygame.draw.line(
                image,
                color,
                (
                    17,
                    9
                ),
                (
                    17,
                    25
                ),
                3
            )


            pygame.draw.line(
                image,
                color,
                (
                    9,
                    17
                ),
                (
                    25,
                    17
                ),
                3
            )


        elif (
            self.pickup_type
            == "route_item"
        ):

            pygame.draw.polygon(
                image,
                color,
                [
                    (17, 6),
                    (28, 17),
                    (17, 28),
                    (6, 17)
                ],
                2
            )


        else:

            font = (
                pygame.font.SysFont(
                    "couriernew",
                    18,
                    bold=True
                )
            )


            text = (
                font.render(
                    "$",
                    True,
                    color
                )
            )


            image.blit(
                text,
                text.get_rect(
                    center=(
                        17,
                        17
                    )
                )
            )


        return image


    # =====================================================
    # UPDATE
    # =====================================================

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