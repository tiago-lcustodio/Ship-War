import math
import pygame

from settings import ASSETS_DIR


class NavCorePiece(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        center
    ):

        super().__init__()


        path = (
            ASSETS_DIR
            / "items"
            / "nav_core_piece.png"
        )


        if path.exists():

            image = pygame.image.load(
                str(path)
            ).convert_alpha()


            self.image = (
                pygame.transform.smoothscale(
                    image,
                    (
                        48,
                        48
                    )
                )
            )

        else:

            # Fallback temporário.
            self.image = pygame.Surface(
                (
                    48,
                    48
                ),
                pygame.SRCALPHA
            )


            pygame.draw.circle(
                self.image,
                (
                    80,
                    230,
                    220,
                    100
                ),
                (
                    24,
                    24
                ),
                22
            )


            pygame.draw.polygon(
                self.image,
                (
                    190,
                    255,
                    245
                ),
                [
                    (24, 5),
                    (42, 24),
                    (24, 43),
                    (6, 24)
                ]
            )


        self.base_position = (
            pygame.Vector2(
                center
            )
        )


        self.position = (
            self.base_position.copy()
        )


        self.time = 0


        self.rect = (
            self.image.get_rect(
                center=center
            )
        )


    def update(
        self,
        dt
    ):

        self.time += dt


        # Flutuação suave.
        self.position.y = (
            self.base_position.y
            + math.sin(
                self.time * 3
            ) * 10
        )


        self.rect.center = (
            round(
                self.position.x
            ),
            round(
                self.position.y
            )
        )