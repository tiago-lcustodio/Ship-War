import pygame

from settings import (
    ASSETS_DIR
)


class SoundManager:

    def __init__(
        self
    ):

        self.enabled = False

        self.sounds = {}


        self.sound_files = {

            "shot_player":
            "shot_player.wav",

            "shot_enemy":
            "shot_enemy.wav",

            "hit":
            "hit.wav",

            "explosion":
            "explosion.wav",

            "player_hit":
            "player_hit.wav",

            "pickup":
            "pickup.wav",

            "level_start":
            "level_start.wav",

            "level_complete":
            "level_complete.wav"
        }


        try:

            if not (
                pygame.mixer.get_init()
            ):

                pygame.mixer.init()


            self.enabled = True


        except pygame.error:

            self.enabled = False

            return


        self.load_sounds()


    def load_sounds(
        self
    ):

        if not self.enabled:

            return


        folder = (
            ASSETS_DIR
            / "sounds"
        )


        for (
            name,
            filename
        ) in self.sound_files.items():

            path = (
                folder
                / filename
            )


            if not path.exists():

                continue


            try:

                self.sounds[name] = (
                    pygame.mixer.Sound(
                        str(path)
                    )
                )

            except pygame.error:

                pass


    def play(
        self,
        name
    ):

        if not self.enabled:

            return


        sound = (
            self.sounds.get(
                name
            )
        )


        if sound:

            sound.play()