import pygame

from settings import (
    EXPLOSION_FRAME_TIME
)


class Explosion(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        frames,
        center
    ):

        super().__init__()


        self.frames = frames

        self.current_frame = 0

        self.timer = 0


        self.image = (
            self.frames[0]
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

        self.timer += dt


        if (
            self.timer
            >= EXPLOSION_FRAME_TIME
        ):

            self.timer = 0

            self.current_frame += 1


            if (
                self.current_frame
                >= len(self.frames)
            ):

                self.kill()

                return


            center = (
                self.rect.center
            )


            self.image = (
                self.frames[
                    self.current_frame
                ]
            )


            self.rect = (
                self.image.get_rect(
                    center=center
                )
            )