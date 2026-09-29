from password_system import (
    GameProgress
)

from game_data import (
    LEVELS
)

from systems.sound_manager import (
    SoundManager
)

from scenes.menu_scene import (
    MenuScene
)

from scenes.password_scene import (
    PasswordScene
)

from scenes.briefing_scene import (
    BriefingScene
)

from scenes.level_scene import (
    LevelScene
)

from scenes.market_scene import (
    MarketScene
)

from scenes.map_scene import (
    MapScene
)

from scenes.ending_choice_scene import (
    EndingChoiceScene
)

from scenes.ending_scene import (
    EndingScene
)


class Game:

    def __init__(
        self,
        screen
    ):

        self.screen = screen

        self.running = True


        self.sound = (
            SoundManager()
        )


        self.progress = (
            GameProgress()
        )


        self.current_scene = None


        self.show_menu()


    def change_scene(
        self,
        scene
    ):

        self.current_scene = (
            scene
        )


    # =====================================================
    # MENU
    # =====================================================

    def show_menu(
        self
    ):

        self.change_scene(
            MenuScene(
                self
            )
        )


    # =====================================================
    # NEW GAME
    # =====================================================

    def new_game(
        self
    ):

        self.progress = (
            GameProgress(

                next_level=1,

                money=0,

                max_hp=3,

                ship_id=0,

                nav_core_parts=0,

                completed_mask=0,

                discovered_mask=1,

                route_items_mask=0
            )
        )


        # Primeira missão ainda começa
        # diretamente pelo briefing.
        self.show_briefing(
            1
        )


    # =====================================================
    # MAP
    # =====================================================

    def show_map(
        self
    ):

        self.change_scene(
            MapScene(
                self
            )
        )


    # =====================================================
    # START LOCATION
    # =====================================================

    def start_location(
        self,
        level_number
    ):

        self.progress.next_level = (
            level_number
        )


        # Briefing apenas enquanto
        # a missão nunca foi completada.
        if (
            self.progress
            .is_completed(
                level_number
            )
        ):

            self.launch_level(
                level_number
            )

        else:

            self.show_briefing(
                level_number
            )


    # =====================================================
    # BRIEFING
    # =====================================================

    def show_briefing(
        self,
        level_number
    ):

        self.progress.next_level = (
            level_number
        )


        self.change_scene(

            BriefingScene(
                self,
                level_number
            )
        )


    # =====================================================
    # LEVEL
    # =====================================================

    def launch_level(
        self,
        level_number
    ):

        self.progress.next_level = (
            level_number
        )


        self.change_scene(

            LevelScene(

                game=self,

                progress=
                self.progress,

                level_config=
                LEVELS[
                    level_number
                ]
            )
        )


    # =====================================================
    # PASSWORD
    # =====================================================

    def show_password_screen(
        self
    ):

        self.change_scene(
            PasswordScene(
                self
            )
        )


    def resume_progress(
        self,
        progress
    ):

        self.progress = (
            progress
        )


        # Save recuperado vai direto
        # para o mapa.
        self.show_map()


    # =====================================================
    # MARKET
    # =====================================================

    def show_market(
        self,
        market_id
    ):

        self.change_scene(

            MarketScene(
                self,
                market_id
            )
        )


    # =====================================================
    # AFTER LEVEL
    # =====================================================

    def after_level_complete(
        self,
        completed_level,
        first_clear
    ):

        # A campanha principal continua
        # encerrando no Level 10.
        #
        # As fases extras não interferem.
        if (
            completed_level == 10
            and first_clear
        ):

            self.show_ending_choice()

            return


        self.show_map()


    # Compatibilidade com versões antigas
    # do LevelCompleteScene.
    def continue_after_level(
        self,
        completed_level,
        target_level=None
    ):

        self.show_map()


    # =====================================================
    # ENDINGS
    # =====================================================

    def show_ending_choice(
        self
    ):

        self.change_scene(

            EndingChoiceScene(
                self
            )
        )


    def show_ending(
        self,
        ending_type
    ):

        self.change_scene(

            EndingScene(
                self,
                ending_type
            )
        )


    # =====================================================
    # GENERAL
    # =====================================================

    def handle_event(
        self,
        event
    ):

        if self.current_scene:

            self.current_scene.handle_event(
                event
            )


    def update(
        self,
        dt
    ):

        if self.current_scene:

            self.current_scene.update(
                dt
            )


    def draw(
        self
    ):

        if self.current_scene:

            self.current_scene.draw(
                self.screen
            )