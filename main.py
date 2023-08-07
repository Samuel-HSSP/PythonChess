from kivy.uix.image import Image
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.behaviors import DragBehavior, ToggleButtonBehavior, ButtonBehavior, FocusBehavior
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ColorProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import string
import chess
import time
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.clock import Clock
from network import Network
from kivymd.uix.snackbar import Snackbar
from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons
#    texture: Gradient.horizontal(get_color_from_hex("E91E63"), get_color_from_hex("FCE4EC"))
Window.size = (720, 400)


LabelBase.register(name='Minecraft-Regular',
                   fn_regular='Fonts/minecraft-3-cufonfonts/1_MinecraftRegular1.otf')

class Player(GridLayout):
    color = ColorProperty([.9, .9, .9, 1])

class Board(GridLayout):
    theme_black_color = ColorProperty()
    theme_white_color = ColorProperty()

class FromMessage(GridLayout):
    message_width = NumericProperty()
    bg_color = ColorProperty()
    text_color = ColorProperty()
    message = StringProperty()
    sender = StringProperty()

class ToMessage(GridLayout):
    message_width = NumericProperty()
    bg_color = ColorProperty()
    text_color = ColorProperty()
    message = StringProperty()


class Competitor(BoxLayout):
    color = BooleanProperty()
    player_name = StringProperty()

class MainMenuButton(MDCard, FocusBehavior, ButtonBehavior):
    text = StringProperty()

class ChessApp(MDApp):
    # horizontal chess labels
    chess_letters = reversed(string.ascii_lowercase[:8])
    FROM = None
    TO = None

    # murdered pieces
    killed_whites = "QRRPPP"
    killed_blacks = ""

    # names of players
    white_player_name = "Ronaldo"
    black_player_name = "SamuelHSSP"

    # theme names
    theme_names = ['dark-choco', 'brown-one', 'brown-two', 'brown-three', 'brown-four', 'almost-black', 'black', 'green', 'blue', 'wine']
    # all themes
    themes = {'dark-choco': [[255/255, 244/255, 226/255, 1], [66/255, 46/255, 47/255, 1]],
              'brown-one': [[240/255, 217/255, 181/255, 1], [181/255, 136/255, 99/255, 1]],
              'brown-two': [[248/255, 224/255, 176/255, 1], [164/255, 111/255, 67/255, 1]],
              'brown-three': [[255/255, 248/255, 238/255, 1], [158/255, 97/255, 50/255, 1]],
              'brown-four': [[255/255, 248/255, 238/255, 1], [153/255, 93/255, 82/255, 1]],
              'almost-black': [[1, 1, 1, 1], [74/255, 72/255, 60/255, 1]],
              'black': [[1, 1, 1, 1], [29/255, 30/255, 24/255, 1]],
              'green': [[1, 1, 1, 1], [54/255, 155/255, 95/255, 1]],
              'blue': [[1, 1, 1, 1], [54/255, 169/255, 188/255, 1]],
              'wine': [[255/255, 252/255, 237/255, 1], [128/255, 35/255, 45/255, 1]],
            }
    # current theme, an element of theme_names
    current_theme = 'brown-three'

    # theme colors
    white = themes[current_theme][0]
    black = themes[current_theme][1]
    
    # background music
    sound = SoundLoader.load('Sounds/cottagecore.mp3')
    sound.loop = True
    # when user clicks a UI button
    ui_btn_click = SoundLoader.load('Sounds/fantasy_ui_button.mp3')

    # whether the white has moved or the game has started
    game_started = False

    # play background music
    if sound:
        sound.volume = 0.5
        sound.play()
    else:
        print("Aber warum")

    # main chess board
    BOARD = chess.Board()
    board_positions = [i for i in range(79, 8, -1) if i not in (71, 62, 53, 44, 35, 26, 17)]
    square_positions = [i for i in range(56, 64)]+[i for i in range(48, 56)]+[i for i in range(40, 48)]+[i for i in range(32, 40)]+\
                       [i for i in range(24, 32)]+[i for i in range(16, 24)]+[i for i in range(8, 16)]+[i for i in range(8)]

    board_fen = BOARD.fen().split()[0].split("/")
    board_places = []
    # connection
    # n = Network()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("main.kv")

    def build(self):
        # draw the grid   
        for index, letter in enumerate(self.chess_letters):
            self.screen.ids.layout.add_widget(ChessLabel(text=f"{letter}"))
        self.screen.ids.layout.add_widget(ChessLabel(text=""))

        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.white))
            self.screen.ids.layout.add_widget(Place(color=self.black))
        self.screen.ids.layout.add_widget(ChessLabel(text="1"))

        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.black))
            self.screen.ids.layout.add_widget(Place(color=self.white))
        self.screen.ids.layout.add_widget(ChessLabel(text="2"))

        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.white))
            self.screen.ids.layout.add_widget(Place(color=self.black))
        self.screen.ids.layout.add_widget(ChessLabel(text="3"))

        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.black))
            self.screen.ids.layout.add_widget(Place(color=self.white))
        self.screen.ids.layout.add_widget(ChessLabel(text="4"))

        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.white))
            self.screen.ids.layout.add_widget(Place(color=self.black))
        self.screen.ids.layout.add_widget(ChessLabel(text="5"))

        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.black))
            self.screen.ids.layout.add_widget(Place(color=self.white))
        self.screen.ids.layout.add_widget(ChessLabel(text="6"))
        
        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.white))
            self.screen.ids.layout.add_widget(Place(color=self.black))
        self.screen.ids.layout.add_widget(ChessLabel(text="7"))
        
        for i in range(4):
            self.screen.ids.layout.add_widget(Place(color=self.black))
            self.screen.ids.layout.add_widget(Place(color=self.white))
        self.screen.ids.layout.add_widget(ChessLabel(text="8"))

        self.draw_board()

        # startPos = self.read_pos(n.getPos())
        # p2Move = n.send()
        return self.screen

    def draw_board(self):
        self.positions = self.screen.ids.layout.children
        self.positions.reverse()

        for row in self.board_fen:
            if row.isalpha():
                # filled square
                self.board_places = self.board_places+list(row)
            elif row.isnumeric():
                # empty square
                self.board_places.extend(['0' for i in range(int(row))])

        for index, piece in enumerate(self.board_places):
            if piece.isalpha() and piece.islower():
                self.positions[self.board_positions[index]].add_widget(Piece(source=f'Pieces/Chess_{piece}dt60.png', piece_type=chess.BLACK))
            elif piece.isalpha() and piece.isupper():
                self.positions[self.board_positions[index]].add_widget(Piece(source=f'Pieces/Chess_{piece.lower()}lt60.png', piece_type=chess.WHITE))
            else:
                self.positions[self.board_positions[index]].add_widget(Piece(empty=True, source=""))

        # print(self.positions)
        # print(self.board_places, self.board_fen, self.board_positions)

    def chess_board_height(self):
        container = self.screen.ids.container.height
        toolbar = self.screen.ids.toolbar.height
        player_1 = self.screen.ids.player_white.height
        player_2 = self.screen.ids.player_black.height
        height = container - (toolbar+player_1+player_2)
        return height

    # def read_pos(self, str):
    #     str = "12, 12".split(",")
    #     return int(str[0]), int(str[1])

    # def make_pos(self, tup):
    #     return str(tup[0]) + "," + str(tup[1])

    def get_color(self, normal, selected, legal, moved, check, capturable):
        if selected and not legal:
            return [255/255, 158/255, 68/255, 1]
        elif legal and not selected or not capturable and not check:
            return [186/255, 202/255, 68/255, 1]
        elif legal and selected:
            return normal
        # elif legal and capturable:
        #     return [255/255, 158/255, 68/255, 1]
        # elif moved:
        #     return [255/255, 233/255, 197/255, 1]
        elif check:
            return [181/255, 55/255, 55/255, 1]


    def change_theme(self):
        old_white = self.white
        old_black = self.black
        print(old_white, old_black)

        if self.theme_names.index(self.current_theme) < len(self.theme_names)-1:
            self.current_theme = self.theme_names[self.theme_names.index(self.current_theme)+1]
            self.white = self.themes[self.current_theme][0]
            self.black = self.themes[self.current_theme][1]

            self.screen.ids.layout.theme_black_color = self.black
            self.screen.ids.layout.theme_white_color = self.white

            for place in self.screen.ids.layout.children:
                print(place.color)
                if place.color == old_white:
                    place.color = self.white
                elif place.color == old_black:
                    place.color = self.black
        else:
            self.current_theme = self.theme_names[0]
            self.white = self.themes[self.current_theme][0]
            self.black = self.themes[self.current_theme][1]
            for place in self.screen.ids.layout.children:
                if place.color == old_white:
                    place.color = self.white
                elif place.color == old_black:
                    place.color = self.black
        
        print(self.current_theme, self.white, self.black)

    def back_home(self):
        self.screen.previous()
    
    def settings_screen(self):
        self.screen.current = "settings"

    def ui_btn_clicked(self):
        if self.ui_btn_click:
            self.ui_btn_click.play()

    def draw_player_name(self, name, pieces_killed):
        killed = ""
        for i in pieces_killed.upper():
            if i == "P":
                killed += "{}"+killed.format("{mdicons['chess-pawn']}")
            elif i == "N":
                killed += "{}"+killed.format("{mdicons['chess-knight']}")
            # elif i == "B":
            #     killed += "{}"+"{mdicons['chess-bishop']}"
            # elif i == "R":
            #     killed += "{mdicons['chess-rook']}"
            # elif i == "Q":
            #     killed += "{mdicons['chess-queen']}"
        text = f"[b]{name}[/b]{' '*25}[size=30][font={fonts[-1]['fn_regular']}]{killed}[/font][/size]"
        print()
        return text

    def send_message(self, message):
        self.screen.ids.ingame_messages.add_widget(
            ToMessage(
                message = message,
                message_width = self.screen.ids.game_info.width/4,
                bg_color = [1, 1, 1, 0],
                text_color = self.screen.ids.layout.theme_black_color
            )
        )
        self.screen.ids.msg.text = ""








app = ChessApp()

class ChessLabel(MDLabel):
    pass

class Piece(ToggleButtonBehavior, Image):
    empty = BooleanProperty(False)
    piece_type = BooleanProperty()
    event = None

    if app.sound:
        move_sound = SoundLoader.load('Sounds/move-self.mp3')
        capture_sound = SoundLoader.load('Sounds/capture.mp3')
        male_grunt = SoundLoader.load('Sounds/gruntsound.mp3')
        female_grunt = SoundLoader.load('Sounds/grunt-female.mp3')
        gun_cock = SoundLoader.load('Sounds/pistol-cock.mp3')
        gunshot = SoundLoader.load('Sounds/shotgun-firing.mp3')
        
        # winning or losing sounds
        checkmate = SoundLoader.load('Sounds/Checkmate_Sound.mp3')
        pawn_transform = SoundLoader.load('Sounds/pwn-transform.mp3')
        winner = SoundLoader.load('Sounds/gewonnen.mp3')
        loser = SoundLoader.load('Sounds/verloren.mp3')
        
        stalemate = SoundLoader.load('Sounds/stalemate-me.mp3')
        # timeout = SoundLoader.load('Sounds/timeout.mp3')
        # resignation = SoundLoader.load('Sounds/resignation.mp3')
        # agreement = SoundLoader.load('Sounds/agreement.mp3')
        # fifty_moves = SoundLoader.load('Sounds/50-moves.mp3')
        # seventy_five_moves = SoundLoader.load('Sounds/75-moves.mp3')
        # tf_repetition = SoundLoader.load('Sounds/three-fold-rep.mp3')
        # ff_repetition = SoundLoader.load('Sounds/five-fold-rep.mp3')
        # insufficient_mat = SoundLoader.load('Sounds/insufficient-material.mp3')
    
    def __init__(self, **kwargs):
        super(Piece, self).__init__(**kwargs)
        self.group = 'x'
        self.GRID = self.parent

    def on_state(self, widget, value):
        if value == 'down':
            # print("Piece selected, Empty: ", self.empty)

            # reset the chess board
            for board_pos in app.board_positions:
                self.parent.parent.children[board_pos].legal = False
                self.parent.parent.children[board_pos].moved = False
                self.parent.parent.children[board_pos].capturable = False
                self.parent.parent.children[board_pos].check = False
            
            legal_moves = app.BOARD.legal_moves
            specific_legals = []

            print(self.empty, self.piece_type)
            if not self.empty and self.piece_type == app.BOARD.turn:
                self.parent.selected = True
                app.FROM = self.parent.parent.children.index(self.parent)
                print("FROM: ", app.FROM)
            
            elif not app.game_started and self.piece_type != app.BOARD.turn:
                return
            elif not app.game_started and self.empty and app.FROM == None:
                return
            # elif not app.game_started and "lt" not in self.source:
            #     return

            # elif not self.empty and self.piece_type != app.BOARD.turn and self.parent.parent.children[app.FROM].children[0].piece_type != self.piece_type:
            #     print("Not your turn")
            #     return

            from_square = app.square_positions[app.board_positions.index(app.FROM)]

            for legal in legal_moves:
                # print(legal.to_square)
                try:
                    move = app.BOARD.find_move(from_square, legal.to_square)
                    specific_legals.append(move.to_square)
                    specific_legals = list(set(specific_legals))
                except:
                    pass
        
            for square in specific_legals:
                to_s = app.board_positions[app.square_positions.index(square)]
                # print(to_s)
                if self.parent.parent.children[to_s].children[0].source == "":
                    self.parent.parent.children[to_s].legal = True
                else:
                    self.parent.parent.children[to_s].legal = True
                    self.parent.parent.children[to_s].capturable = True

            if self.parent.legal and self.parent.parent.children[app.FROM].children[0].piece_type == app.BOARD.turn:
                app.TO = self.parent.parent.children.index(self.parent)
                print("TO: ", app.TO)
                self.move(app.FROM, app.TO)
            # index = self.parent.parent.children.index(self.parent)
            # squares = self.parent.parent.children

                 
        else:
            self.parent.selected = False
            # print("Piece unselected")

    def get_piece_name(self, source):
        piece = source.split("/")[-1]
        if "dt" in piece:
            piece = piece.replace("Chess_", "").replace("60.png", "")
            # print("Piece", piece)
            return piece
        else:
            piece = piece.replace("Chess_", "").replace("60.png", "").upper()
            # print("Piece", piece)
            return piece

    def update_outcome_anim(self, *args):
        self.outcome_text = app.screen.ids.outcome
        
        anim = Animation(sizing=150, d=1)
        anim += Animation(sizing=50, d=1)
        anim.repeat = True
        anim.start(self.outcome_text)

    def update_kills(self, killer):
        if killer == "W":
            app.screen.ids.player_white.text = f"{app.draw_player_name(app.white_player_name, app.killed_blacks)}"
        else:
            app.screen.ids.player_black.text = f"{app.draw_player_name(app.black_player_name, app.killed_whites)}"

    def move(self, from_index, to_index):
        # print("FROM: ", from_index, "TO: ", to_index)
        from_square = app.square_positions[app.board_positions.index(from_index)]
        to_square = app.square_positions[app.board_positions.index(to_index)]
        
        move = chess.Move(from_square, to_square)
        # move on the board
        place = self.parent
        source = app.screen.ids.layout.children[from_index]
        piece_type = source.children[0].source
        destination = app.screen.ids.layout.children[to_index]
        opp = destination.children[0].source
        # print(source, destination, piece_type)

        playing_piece = self.get_piece_name(source.children[0].source)
        opponent = self.get_piece_name(destination.children[0].source)

        source.children[0].empty, destination.children[0].empty = True, False
        source.children[0].source, destination.children[0].source = "", piece_type
        # print("Piece Types: ", source.children[0].piece_type, destination.children[0].piece_type)
        destination.children[0].piece_type = source.children[0].piece_type
        source.moved = True

        for board_pos in app.board_positions:
            app.screen.ids.layout.children[board_pos].legal = False
            app.screen.ids.layout.children[board_pos].capturable = False
        
        app.BOARD.push(move)
        print(app.BOARD)

        # send to server
        # p = app.n.getP()
        # p2 = app.n.send(p)

        print("Player: ", playing_piece, ", Opponent: ", opponent)
        # print(app.BOARD.is_capture(move), move)
        if "P" in opponent.upper():
            print("That was a pawn capture")
            if playing_piece.isupper():
                app.killed_blacks += "p"
                # self.update_kills('W')
            else:
                app.killed_whites += "P"
                # self.update_kills('b')
            if self.capture_sound:
                self.capture_sound.volume = 1
                self.capture_sound.play()
        elif "B" in opponent.upper():
            print("That was a bishop capture")
            if playing_piece.isupper():
                app.killed_blacks += "b"
                # self.update_kills('W')
            else:
                app.killed_whites += "B"
                # self.update_kills('b')
        elif "N" in opponent.upper():
            print("That was a knight capture")
            if playing_piece.isupper():
                app.killed_blacks += "n"
                # self.update_kills('W')
            else:
                app.killed_whites += "N"
                # self.update_kills('b')
            
            if self.male_grunt:
                self.male_grunt.volume = 1
                self.male_grunt.play()
        elif "R" in opponent.upper():
            print("That was a rook capture")
            if playing_piece.isupper():
                app.killed_blacks += "r"
                # self.update_kills('W')
            else:
                app.killed_whites += "R"
                # self.update_kills('b')
        elif "Q" in opponent.upper():
            print("That was a Queen capture")
            if playing_piece.isupper():
                app.killed_blacks += "q"
                # self.update_kills('W')
            else:
                app.killed_whites += "Q"
                # self.update_kills('b')
            if self.female_grunt:
                self.female_grunt.volume = 1
                self.female_grunt.play()

        else:
            # play move sound
            if self.move_sound:
                self.move_sound.volume = 1
                self.move_sound.play()

        if app.BOARD.is_checkmate():
            print("Checkmate!")
            if self.gunshot:
                self.gunshot.volume = 0.6
                self.gunshot.play()         
            time.sleep(2)
            app.sound.stop()
            if app.BOARD.outcome().winner == True: # white wins
                if "LT" in playing_piece: # the player is the winner
                    if self.winner:
                        self.winner.volume = 1
                        self.winner.play()
                else: # the player lost
                    if self.loser:
                        self.loser.volume = 1
                        self.loser.play()
            else:
                if "dt" in playing_piece: # the player is the winner
                    if self.winner:
                        self.winner.volume = 1
                        self.winner.play()
                else: # the player lost
                    if self.loser:
                        self.loser.volume = 1
                        self.loser.play()             

            # display checkmate message
            app.screen.ids.outcome.text = "Checkmate!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()

            if self.checkmate:
                self.checkmate.volume = 1
                self.checkmate.play()

            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None         

        elif app.BOARD.is_stalemate():
            print("Stalemate!")
            # display stalemate message
            app.screen.ids.outcome.text = "Stalemate!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()
            time.sleep(2)
            if self.stalemate:
                self.stalemate.volume = 1
                self.stalemate.play()
            
            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None



        elif app.BOARD.can_claim_threefold_repetition():
            print("Three-Fold Repetition!")
            # display stalemate message
            app.screen.ids.outcome.text = "Three-Fold Repetition!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()
            time.sleep(2)
            if self.tf_repetition:
                self.tf_repetition.volume = 1
                self.tf_repetition.play()
            
            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None


        elif app.BOARD.is_fivefold_repetition():
            print("Five-Fold Repetition!")
            # display stalemate message
            app.screen.ids.outcome.text = "Five-Fold Repetition!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()
            time.sleep(2)
            if self.ff_repetition:
                self.ff_repetition.volume = 1
                self.ff_repetition.play()
            
            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None


        elif app.BOARD.is_insufficient_material():
            print("Insufficient Material!")
            # display stalemate message
            app.screen.ids.outcome.text = "Insufficient Material!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()
            time.sleep(2)
            if self.insufficient_mat:
                self.insufficient_mat.volume = 1
                self.insufficient_mat.play()
            
            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None

        elif app.BOARD.can_claim_fifty_moves():
            print("Fifty Moves!")
            # display stalemate message
            app.screen.ids.outcome.text = "Fifty Moves!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()
            time.sleep(2)
            if self.fifty_moves:
                self.fifty_moves.volume = 1
                self.fifty_moves.play()
            
            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None

        elif app.BOARD.is_seventyfive_moves():
            print("Seventy-Five Moves!")
            # display stalemate message
            app.screen.ids.outcome.text = "Seventy-Five Moves!"
            app.screen.ids.outcome.text_color = app.black
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, .7]
            self.event = Clock.schedule_interval(self.update_outcome_anim, 2)
            self.event()
            time.sleep(2)
            if self.seventy_five_moves:
                self.seventy_five_moves.volume = 1
                self.seventy_five_moves.play()
            
            app.screen.ids.outcome.text = "Game Over!"
            app.screen.ids.outcome.text_color = [0, 0, 0, 0]
            app.screen.ids.outcome_container.md_bg_color = [1, 1, 1, 0]
            self.event.cancel()
            self.event = None

        elif app.BOARD.is_check():
            checkers = app.BOARD.checkers()
            print("Check!")
            opp_k = 10
            self.snackbar = Snackbar(text="Check", bg_color=app.black, duration=1)
            self.snackbar.open()
            board_fen = ''.join(app.BOARD.fen().split()[0].split("/"))
            board_places = []

            for place in board_fen:
                if place.isalpha():
                    # filled square
                    board_places.append(place)
                elif place.isnumeric():
                    # empty square
                    board_places.extend(['0' for i in range(int(place))])

            print(board_places)
            # white just played
            if "LT" in playing_piece:
                print(app.board_positions[board_places.index('k')])
                
                self.parent.parent.children[app.board_positions[board_places.index("k")]].check = True
                print(self.parent.parent.children[app.board_positions[board_places.index("k")]].legal, self.parent.parent.children[app.board_positions[board_places.index("k")]].capturable,
                self.parent.parent.children[app.board_positions[board_places.index("k")]].moved,
                self.parent.parent.children[app.board_positions[board_places.index("k")]].selected,
                )
            # black just played
            # else:
            #     opp_k = self.parent.parent.children[app.board_positions[board_places.index("K")]]
            #     opp_k.check = True
            #     print(opp_k)


            if self.gun_cock:
                self.gun_cock.volume = 1
                self.gun_cock.play()
            # self.parent.parent.children[opp_k].check = True

        # if app.screen.ids.player_one.color == app.black:
            # app.screen.ids.player_one.color = app.black if app.screen.ids.player_one.color != app.black else [.9, .9, .9, 1]
        # app.screen.ids.player_two.color = app.white if app.screen.ids.player_one.color != app.white else [.9, .9, .9, 1]
        app.game_started = True



class OutPiece(Image):
    pass

class Place(BoxLayout):
    color = ColorProperty()
    selected_color = ColorProperty((1, 1, 0, 1))
    selected = BooleanProperty(False)
    legal = BooleanProperty(False)
    moved = BooleanProperty(False)
    check = BooleanProperty(False)
    capturable = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Place, self).__init__(**kwargs)

app.run()