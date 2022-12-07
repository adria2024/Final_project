import arcade
import random
from arcade import load_texture, Window
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
intro_music = arcade.load_sound("Game_sounds/dramatic-horror-cinematic-epic-trailer-action-intro-opener-115496.mp3")

temp_sound = arcade.play_sound(intro_music)


class InstructionView(arcade.View):

    def on_draw(self):
        background = arcade.load_texture("redmoon.jpg")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, background)
        arcade.draw_text("Welcome to DESTINATION: SAFETY ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200, font_size=30,
                         anchor_x="center")

        arcade.draw_text("The instructions for the game are simple. The game will provide you with three potential"
                         " paths in which you will click the text box with your mouse and answer the question then"
                         " press the start button throughout the game to continue. Your score will be the amount of"
                         " time you took to win the game. And the difficulty will be random. You must choose"
                         " a path and face the dangers ahead of you to get out of the forest and to somewhere safe."
                         " You will have many options that determine whether you live or die in the game, so choose"
                         " wisely. Since you choose the path, the game's direction is entirely up to you. I wish you"
                         " good luck, traveler. May God be with you.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 75,
                         font_size=14, anchor_x="center", multiline=True, width=SCREEN_WIDTH - 100)

        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 175, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyWindow()
        game_view.setup()
        self.window.show_view(game_view)


class MyWindow(arcade.View):
    path_counter = -1
    total_time = 0.0

    def __init__(self):
        super().__init__()

        self.random_run = None
        self.random = None
        self.name = None
        self.input_area = None
        self.manager = None
        self.v_box = None
        self.timer_text = arcade.Text(text="00:00:00", start_x=SCREEN_WIDTH // 2 + 40, start_y=SCREEN_HEIGHT // 2 - 25,
                                      font_size=14, anchor_x="center")
        self.text = "Would you like to start your adventure?(yes/no)"

        self.creaky_door = arcade.load_sound("Game_sounds/big-door-creak-103900.mp3")
        self.crow = arcade.load_sound("Game_sounds/2crows-in-cherry-tree-25228.mp3")
        self.i_c_u = arcade.load_sound("Game_sounds/peekaboo-i-see-you-104504.mp3")
        self.zombie = arcade.load_sound("Game_sounds/zombie-moans-29924.mp3")
        self.storm = arcade.load_sound("Game_sounds/mixkit-heavy-rain-storm-1257.wav")
        self.whispers = arcade.load_sound("Game_sounds/whisper-trail-2ogg-14429.mp3")
        self.footsteps = arcade.load_sound("Game_sounds/mixkit-footsteps-on-tall-grass-532 (1).wav")
        self.icu = arcade.load_sound("Game_sounds/peekaboo-i-see-you-104504.mp3")
        self.dying_help_me = arcade.load_sound("Game_sounds/help-me-74320.mp3")
        self.leg = arcade.load_sound("Game_sounds/man-scream-121085.mp3")
        self.slam_door = arcade.load_sound("Game_sounds/door-slam-79889.mp3")
        self.locked_door = arcade.load_sound("Game_sounds/door-slam-locked79889.mp3")
        self.screaming_man = arcade.load_sound("Game_sounds/screamer-test-103648.mp3")
        self.wolves = arcade.load_sound("Game_sounds/wood-of-wolves-in-the-rain-72869.mp3")
        self.zom_broadcast = arcade.load_sound("Game_sounds/zombie-news-am-radio-35057.mp3")
        self.tunnel_steps = arcade.load_sound("Game_sounds/mixkit-footsteps-in-a-tunnel-loop-543.wav")
        self.coughing_man = arcade.load_sound("Game_sounds/adult-male-coughing-45593.mp3")
        self.chainsaw = arcade.load_sound("Game_sounds/chainsaw-05.wav")

    def setup(self):

        self.manager = UIManager()
        self.manager.enable()

        # Create Text Area
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        text_area = UITextArea(x=100,
                               y=200,
                               width=200,
                               height=300,
                               text=self.text,
                               text_color=(0, 0, 0, 255))

        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )

        # Text input area
        self.input_area = UIInputText(x=340, y=200, width=200)
        self.manager.add(
            UITexturePane(
                self.input_area,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            ))

        # Buttons
        # Create a BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        reload_button = arcade.gui.UIFlatButton(text="Start", width=200)
        self.v_box.add(reload_button.with_space_around(bottom=20))

        reload_button.on_click = self.on_click_reload

        end_button = arcade.gui.UIFlatButton(text="Ending Button", width=200)
        self.v_box.add(end_button.with_space_around(bottom=20))

        end_button.on_click = self.on_click_end

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box)
        )

    def on_click_reload(self, event):
        print("My Start:", event)
        self.text = self.game(self.input_area.text)
        self.setup()

    def on_click_end(self, event):
        print("My Start:", event)
        end_view = EndingView()
        self.window.show_view(end_view)

    def on_draw(self):
        background = arcade.load_texture("redforrest.jpg")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, background)

        self.manager.draw()
        self.timer_text.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        # Accumulate the total time
        self.total_time += delta_time

        MyWindow.total_time = self.total_time

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Calculate 100s of a second
        seconds_100s = int((self.total_time - seconds) * 100)

        # Use string formatting to create a new text string for our timer
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

    def game(self, response):

        if self.random_run == 0:
            self.random_run = random.randint(0, 0)

        elif response == "yes" and self.path_counter == -1:
            self.path_counter = 0
            # scene 1
            arcade.stop_sound(temp_sound)
            te = arcade.play_sound(self.crow)
            self.crow.set_volume(1.0, te)
            st = arcade.play_sound(self.storm)
            self.storm.set_volume(.5, st)

            return "You find yourself deep in the forrest. You hear crows cawing in the distance which startles you. " \
                   "It's cold you can see your breath in the air as you exhale. BOOM! CLASH! Out of nowhere it" \
                   "starts" \
                   "to rain hard. You're scared that if you say outside long you'll die of hypothermia.\nWould you " \
                   "like to continue ? (yes/no) "

        elif response == "no" and self.path_counter == 0:
            self.path_counter = 1
            return "You die of hyperthermia. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "yes" and self.path_counter == 0:
            self.path_counter = 1
            self.random = random.randint(1, 3)
            arcade.play_sound(self.zombie)
            return "You see a person stumbling far behind you." "You yell, are you alright but all you hear back is " \
                   "groaning." "As you get closer, you realize it's not a person, it's a zombie. The zombie begins " \
                   "to chase you. There are 3 paths: left, right, and forward. Which direction will you take? "

        elif self.path_counter == 1 and self.random == 1:
            self.path_counter = 2
            arcade.play_sound(self.zombie)
            return "You trip and fall. The zombie bites you on the arm but you manage to escape. You feel like you've " \
                   "been running for miles, the adrenaline wears off and you start to feel immense pain. You see a " \
                   "cabin, you're hoping there will be medical supplies in there. Go in the cabin? (yes/no)"

        elif response == "no" and self.path_counter == 2:
            self.path_counter = 3
            arcade.play_sound(self.footsteps)
            return "You stay outside wander around for hours and eventually die from bleeding out." \
                   "\nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START."

        elif response == "yes" and self.path_counter == 2:
            self.path_counter = 3
            arcade.play_sound(self.zom_broadcast)
            return "You open the door. You see a family facing the t.v, they didn't seem to notice " \
                   "you coming in. You introduce yourself they don't even move an inch. You walk in front " \
                   "of the t.v and see the skeletons of the people who lived here. The t.v plays the latest news. " \
                   "Search the cabin? (yes/no)"

        elif response == "yes" and self.path_counter == 3:
            self.path_counter = 4
            return "You open some doors and find nothing of use. There is one more door. This may be your " \
                   "last hope. Open the door? (yes/no)"

        elif response == "no" and self.path_counter == 3:
            self.path_counter = 4
            arcade.play_sound(self.zombie)
            return "You turn into a zombie. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "yes" and self.path_counter == 4:
            self.path_counter = 5
            return "A zombie dog runs out and eats you alive. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "no" and self.path_counter == 4:
            self.path_counter = 5
            arcade.play_sound(self.zombie)
            return "You turn into a zombie. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        #######################################################################################################

        elif self.path_counter == 1 and self.random == 2:
            self.path_counter = 6
            arcade.play_sound(self.wolves)
            return "You run deeper into the forest. You're lost, cold, hungry and scared. As you keep walking you " \
                   "find yourself at a cozy looking cottage, it seems safe. Go inside the cottage? (yes/no) "

        elif response == "no" and self.path_counter == 6:
            self.path_counter = 7
            return "You were eaten by a werewolf. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "yes" and self.path_counter == 6:
            self.path_counter = 7
            return "You go into the cottage and notice there is a fire lit. You choose to ignore it and look for " \
                   "food. You managed to find a can of beans. You sit by the fire and eat it. After that, you feel " \
                   "very tired. Take a nap? (yes/no)"

        elif response == "yes" and self.path_counter == 7:
            self.path_counter = 8
            arcade.play_sound(self.zombie)
            return "You wake up well rested. You look outside and it is still dark out, no sign of the sun " \
                   "anywhere. That's strange you say. You open a door to see if you can find anything of use and a " \
                   "zombie comes out of nowhere killing you. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "no" and self.path_counter == 7:
            self.path_counter = 8
            return "You hear the door open. when you looked to see who it was everything went black. " \
                   "You wake up in a unfamiliar place, chained to a pole. A person walks in unchains you and " \
                   "forces you into a walk-in freezer. Try to get out? (yes) "

        elif response == "yes" and self.path_counter == 8:
            self.path_counter = 9
            arcade.play_sound(self.locked_door)

            return "You tried to get out but your efforts failed you. You see containers labeled human meat. " \
                   "You look to your left and see a head " \
                   "in a jar. After hours of yelling for help you give up. There is no way out. You froze " \
                   "to death. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        ############################################################################################################

        elif self.path_counter == 1 and self.random == 3:
            self.path_counter = 10
            arcade.play_sound(self.whispers)
            return "You run towards a mansion. The mansion door is unlocked. " \
                   "You go inside and everything is dark." \
                   " Luckily, you find the light switch." \
                   "There is dust and cobwebs everywhere. There is a door on your left which is covered in blood and " \
                   "the door on your right you hear whispers. You swear you heard your name. Which door do you choose? "

        elif response == "left" and self.path_counter == 10:
            self.path_counter = 11
            te = arcade.play_sound(self.creaky_door)
            self.creaky_door.set_volume(0.3, te)
            st = arcade.play_sound(self.dying_help_me)
            self.dying_help_me.set_volume(2.0, st)
            return "You open the door slowly, afraid something will jump out and kill you, but " \
                   "nothing does. You walk in to see a man on the floor in pain. He has a bite size " \
                   "chunk taken out of his leg. He's pleading for help. Do you help him? (yes/no) "

        elif response == "yes" and self.path_counter == 11:
            self.path_counter = 12
            arcade.play_sound(self.leg)
            return "You look for something to slow the bleeding. You find a towel and belt. You put the towel " \
                   "on his leg and tell him to put pressure on it. you take the belt and put it just above " \
                   "his wound. You look for a sharp object and you use it to amputate the leg hopefully stopping " \
                   "the infection but only time will tell. You tell him that you will come back for him and " \
                   "leave the room.You explore the main room and discover a secret passage way. It " \
                   " might be a way out. Go into the tunnel? (yes). "

        elif response == "yes" and self.path_counter == 12:
            arcade.play_sound(self.slam_door)
            self.path_counter = 13
            return "You step into the tunnel and walk down the path, the tunnel entrance slams close! Go to the " \
                   "tunnel entrance? (yes/no) "

        elif response == "yes" and self.path_counter == 13:
            self.path_counter = 14
            arcade.play_sound(self.locked_door)
            return "You walk back to the tunnel entrance, it seems to be locked from the outside. There no getting " \
                   "out that way. You walk down the tunnel again and think you've been going in circles. This place " \
                   "is like a maze, how am I ever going to get out?! Just then you see hundreds of zombies " \
                   "hibernating. You try to tip toe past them but you tripped and fell awaking the zombie " \
                   "horde. You try to outrun them but you to into a dead end with no way out. You " \
                   "were killed by 12 zombies. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "no" and self.path_counter == 11:
            self.path_counter = 12
            arcade.play_sound(self.screaming_man)
            return "Nice acting but i'm not falling for it. You'll jump me and take all I have! You walk " \
                   "out the door still hearing his screams for help. You explore the main room and discover " \
                   "a secret passage way. It might be a way out. Go into the tunnel? (yes) "

        elif response == "yes" and self.path_counter == 13:
            self.path_counter = 14
            arcade.play_sound(self.tunnel_steps)

            return "You walk down the tunnel and think you've been going in circles. This place " \
                   " is like a maze, how am I ever going to get out?! You take a couple more turns and " \
                   " find a door labeled Lab. Go into door? (yes/no) "

        elif (response == "yes" or "no") and self.path_counter == 14:
            self.path_counter = 15
            return "You go in and discover hundreds of serums one of them says zombie. It's green " \
                   "and it could be a cure or the virus? Take the serum? (yes/no) "

        elif response == "yes" and self.path_counter == 15:
            self.path_counter = 16
            arcade.play_sound(self.zombie)
            return "You take the serum and start to feel immense pain. You can feel yourself turning. " \
                   "You are now a zombie. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "no" and self.path_counter == 15:
            self.path_counter = 16
            arcade.play_sound(self.coughing_man)
            return "You decide not to mess with it and you put it down. You walk around and " \
                   "accidentally step on a vial, it breaks and oozes out a mysterious liquid. You start " \
                   "coughing uncontrollably. You suddenly can't beathe. Try and get out? (yes/no) "

        elif response == "yes" and self.path_counter == 16:
            self.path_counter = 17
            return "You run to the door, but someone shuts it and locks you in. There is no way out. It wasn't " \
                   "long until you lie lifeless on the floor. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "no" and self.path_counter == 16:
            self.path_counter = 17
            return "You give up. You see a video camera on a self, you grab it and begin to tell your story " \
                   "of what happened to you until you die. hoping someone will eventually find it. \nPLEASE " \
                   "TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        #######################################################################################################
        elif response == "right" and self.path_counter == 10:
            self.path_counter = 24
            st = arcade.play_sound(self.whispers)
            self.whispers.set_volume(.5, st)
            st = arcade.play_sound(self.icu)
            self.icu.set_volume(1.0, st)
            return "You open the door that leads into a basement. It's dark. You walk down the stairs and the " \
                   "whispers " \
                   " become louder and louder and then they suddenly stop. It's silent until you hear someone say: " \
                   " I see you. It sounded like it came directly behind you. Do you go left or forward? "

        elif response == "left" and self.path_counter == 24:
            self.path_counter = 25
            return "You get so scared to start running around in the dark. You find what looks like a door and " \
                   "you see a bright light. Go into the bright light? (yes/no) "

        elif response == "yes" and self.path_counter == 25:
            self.path_counter = 26
            return "You died from fright and went to heaven. PLEASE TYPE oh " \
                   "no IN THE TEXT BOX THEN PRESS START. "

        elif response == "no" and self.path_counter == 25:
            self.path_counter = 26
            return "The man in the dark caught you and you died by strangulation. \nPLEASE TYPE oh no IN THE TEXT " \
                   " BOX THEN PRESS START. "

        elif response == "forward" and self.path_counter == 24:
            self.path_counter = 27
            arcade.play_sound(self.chainsaw)
            return "You hear what seems to be a chainsaw. You hear someone in front of you say bye " \
                   "bye and then try kill you with the chain saw. They somehow miss you. What do you want from " \
                   "me you cry. Blood he screams. Do you want to respond? (yes) "

        elif response == "yes" and self.path_counter == 27:
            self.path_counter = 28
            return "You find a rock and a sharp object. You say then I've got news for you buddy the only " \
                   "blood that is going to be spilt here is yours. You threw the rock and wait until he " \
                   "investigates. You then you stab him in the neck and run back upstairs locking the door behind you. " \
                   " Do you want to hide? (yes/no) "

        elif response == "no" and self.path_counter == 28:
            self.path_counter = 29
            arcade.play_sound(self.screaming_man)
            return "He bursts through the door. Your fear won't allow you to move. He drags you back down " \
                   "to the basement where you die slowly by torcher. \nPLEASE TYPE oh no IN THE TEXT BOX. " \
                   "THEN PRESS START "

        elif response == "yes" and self.path_counter == 28:
            self.path_counter = 29
            return "You hide behind furniture. He burst through the door and you can see from the light " \
                   "that he wasn't all human. He was half human and half zombie. A potential cure you said " \
                   "softly. He heard you. Try to reason with him (yes/no) "

        elif response == "no" and self.path_counter == 29:
            self.path_counter = 30
            "He punches you and you hit your head on the corner of a table. You can't move, he approaches " \
                "and eats you alive.\nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START "

        elif response == "yes" and self.path_counter == 29:
            self.path_counter = 30
            return "He starts to walk towards you. You say hold on, wait, you could be a potential " \
                   " cure for human kind. Why would I want that? I love this new world. I am the ruler, " \
                   " the zombies see me as their king. You tried to reason with him but he is to far gone. " \
                   "Take a risk? (yes/no) "

        elif response == "yes" and self.path_counter == 30:
            self.path_counter = 31
            return "There is a sword hanging on the wall as a decoration. You're hoping it's real and it is. " \
                   "Fight the monster? (yes/no) "

        elif response == "no" and self.path_counter == 30:
            self.path_counter = 31
            return "He kills out so fast out of rage and you didn't even have time to " \
                   "scream. \nPLEASE TYPE oh no IN THE TEXT BOX THEN PRESS START. "

        elif response == "yes" and self.path_counter == 31:
            self.path_counter = 32
            return "You grab the sword you only have one shot at this. You don't know whether to strike the heart " \
                   " or decapitate the head because he's not fully alive but not fully dead either. " \
                   " Type yes for stabbing the heart or no for decapitation. (yes/no) "

        elif response == "no" and self.path_counter == 32:
            self.path_counter = 33
            self.random = random.randint(1, 2)
            if self.random == 1:
                return "You chose to decapitate the head. You woke up in a sweat, noticing it was " \
                       "just a nightmare and you've been safe the whole time. CONGRATS YOU BEAT THE GAME! "
# win screen not working

        elif response == "yes" and self.path_counter == 32:
            self.path_counter = 33
            self.random = random.randint(1, 2)
            if self.random == 1:
                return "You chose to stab the heart. You woke up in a sweat, noticing it was just" \
                       " a nightmare and you've been safe the whole time. CONGRATS YOU BEAT THE GAME! "
# win screen not working
            else:
                return "GAME OVER! YOU DIED! \nPLEASE TYPE oh no IN THE TEXT BOX. " \
                   "THEN PRESS START"

        elif response == "oh no":
            dead_view = DeadView()
            self.window.show_view(dead_view)

        elif response == "complete":
            wining_view = WinView()
            self.window.show_view(wining_view)

        else:
            return "wrong input, please try again "


class EndingView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("You ended the game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, font_size=50, anchor_x="center")

        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.exit()


class DeadView(arcade.View):

    def __init__(self, win_dow: Window = None):
        super().__init__(win_dow)
        self.time = MyWindow.total_time
        self.game_over = arcade.load_sound("Game_sounds/game-over-26662.mp3")
        arcade.play_sound(self.game_over, 2.0)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        display_time = "You're score is: " + str(round(self.time, 2))
        arcade.draw_text("GAME OVER! YOU DIED!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, font_size=20,
                         anchor_x="center")
        arcade.draw_text("Click X TO EXIT", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, font_size=15, anchor_x="center")
        arcade.draw_text(display_time, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         font_size=13, anchor_x="center")


class WinView(arcade.View):

    def __init__(self, win_dow: Window = None):
        super().__init__(win_dow)
        self.time = MyWindow.total_time

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        display_time = "You're score is: " + str(round(self.time, 2))
        arcade.draw_text("CONGRATULATIONS! YOU WON!", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 + 100, font_size=15, anchor_x="center")
        arcade.draw_text("CLICK X TO EXIT", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, font_size=15, anchor_x="center")
        arcade.draw_text(display_time, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         font_size=13, anchor_x="center")


window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Horror Game")
instruction_view = InstructionView()
window.show_view(instruction_view)
arcade.run()
