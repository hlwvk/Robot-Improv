import Tkinter as tk # python 2
from PIL import Image, ImageTk
import qi
import sys
import argparse
import random
import datetime
import os


class Service:
    def __init__(self, session):

        self.behavior_mng_service = session.service("ALBehaviorManager")
        self.posture_service = session.service("ALRobotPosture")
        self.posture_service.goToPosture("StandInit", 1.0)
        self.motion_service = session.service("ALMotion")

        self.head_behaviors = ["behavior_look_center_slow", "behavior_look_center_fast",
                     "behavior_look_left_slow", "behavior_look_left_fast",
                     "behavior_look_right_slow", "behavior_look_right_fast",
                     "behavior_look_down_slow", "behavior_look_down_fast",
                     "behavior_look_up_slow", "behavior_look_up_fast",
                     "behavior_look_up_left_slow", "behavior_look_up_left_fast",
                     "behavior_look_up_right_slow", "behavior_look_up_right_fast",
                     "behavior_look_down_left_slow", "behavior_look_down_left_fast",
                     "behavior_look_down_right_slow", "behavior_look_down_right_fast"]

        self.base_behaviors = ["behavior_move_down_slow", "behavior_move_down_fast", "behavior_move_up_slow",
                               "behavior_move_up_fast", "behavior_turn_toward", "behavior_turn_back"]
        self.inward_behaviors = ["behavior_inward_left_1", "behavior_inward_1", "behavior_inward_right_1",
                                 "behavior_outward_left_1", "behavior_outward_1", "behavior_outward_right_1",
                                 "behavior_inward_left_2", "behavior_inward_2", "behavior_inward_right_2",
                                 "behavior_outward_left_2", "behavior_outward_2", "behavior_outward_right_2",
                                 "behavior_move_up_fast", "behavior_move_down_fast", "behavior_move_left_fast",
                                 "behavior_move_right_fast"]

        self.fractionMaxSpeed = 0.3
        self.last_behavior = None
        self.is_turned = False
        self.last_random = None
        self.last_random_int = None
        self.half_finished = True

        # turn off all autonomous abilties
        self.life_service = session.service("ALAutonomousLife")
        self.life_service.setAutonomousAbilityEnabled("AutonomousBlinking", False)
        self.life_service.setAutonomousAbilityEnabled("BackgroundMovement", False)
        self.life_service.setAutonomousAbilityEnabled("BasicAwareness", False)
        self.life_service.setAutonomousAbilityEnabled("ListeningMovement", False)
        self.life_service.setAutonomousAbilityEnabled("SpeakingMovement", False)

    # motion service
    def motion_service_rest(self):
        self.motion_service.rest()

    def motion_service_wake_up(self):
        self.motion_service.wakeUp()

    def motion_service_stop_move(self):
        self.motion_service.stopMove()

    def go_to_init(self):
        self.start_behavior_func("behavior_default")

    def check_if_idle(self):
        print("Running behaviors: ", self.behavior_mng_service.getRunningBehaviors())

    def stop_last_behavior(self):
        print("stopping", self.last_behavior)
        self.behavior_mng_service.stopBehavior(self.last_behavior)
        print("Running behaviors: ", self.behavior_mng_service.getRunningBehaviors())

    def stop_all_behaviors(self):
        names = self.behavior_mng_service.getRunningBehaviors()
        print("stop all behaviors\n", "running: ", names)
        self.behavior_mng_service.stopAllBehaviors()
        names = self.behavior_mng_service.getRunningBehaviors()
        print("stopped all behaviors\n", "running: ", names)

    def get_installed_behaviors(self):
        names = self.behavior_mng_service.getInstalledBehaviors()
        print("Installed: ", names)

    def look_random(self, button):
        random_int = self.pick_random_nr(a=0, b=len(self.head_behaviors)-1)
        while random_int == self.last_random_int:
            random_int = self.pick_random_nr(a=0, b=len(self.head_behaviors) - 1)
        self.last_random_int = random_int
        behavior = self.head_behaviors[random_int]

        current_time = datetime.datetime.now()
        s = "logfile_random.txt"
        with open(s, 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s," % str(button))
            f.write("%s," % str(behavior))
            f.write("%s," % "Task 1")
            f.write("%s\n" % "Random")

        self.start_behavior_func(behavior)

    def pick_random_nr(self, a, b):
        random_int = random.randint(a, b)
        return random_int

    def move_random(self, button):
        # pick random number
        random_int = self.pick_random_nr(a=0, b=4)
        # while identical to last number, pick again
        while random_int == self.last_random_int:
            random_int = self.pick_random_nr(a=0, b=4)
        self.last_random_int = random_int

        current_time = datetime.datetime.now()
        s = "logfile_random.txt"
        with open(s, 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s," % str(button))
            f.write("%s," % "behavior")
            f.write("%s," % "Task 2")
            f.write("%s\n" % "Random")

        if random_int == 0:
            self.backward_slow()
        if random_int == 1:
            self.backward_fast()
        if random_int == 2:
            self.forward_slow()
        if random_int == 3:
            self.forward_fast()
        if random_int == 4:
            self.turn()

    def inward_random(self, button):
        random_int = self.pick_random_nr(a=0, b=len(self.inward_behaviors)-1)
        while random_int == self.last_random_int:
            random_int = self.pick_random_nr(a=0, b=len(self.inward_behaviors) - 1)
        self.last_random_int = random_int
        behavior = self.inward_behaviors[random_int]

        current_time = datetime.datetime.now()
        s = "logfile_random.txt"

        with open(s, 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s," % str(button))
            f.write("%s," % str(behavior))
            f.write("%s," % "Task 3")
            f.write("%s\n" % "Random")

        self.start_behavior_func(behavior)

    def start_behavior_func(self, name):
        current_time = datetime.datetime.now()
        with open('logfile.txt', 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s\n" % name)

        with open('logfile2.txt', 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s\n" % name)

        # may select project directly with "untitled_4-434e99/" + name
        behavior_path = ".lastUploadedChoregrapheBehavior/" + name

        # stop last behavior
        if self.last_behavior is not None:
            self.behavior_mng_service.stopBehavior(self.last_behavior)
        # stop behavior if already running
        if self.behavior_mng_service.isBehaviorRunning(behavior_path):
            self.behavior_mng_service.stopBehavior(behavior_path)
        self.last_behavior = behavior_path
        # run async with start, sync with run
        self.behavior_mng_service.startBehavior(behavior_path)
        #self.behavior_mng_service.runBehavior(behavior_path)

    def inward(self):
        random_int = random.randint(1, 2)
        name = "behavior_inward_" + str(random_int)
        self.start_behavior_func(name)

    def inward_left(self):
        random_int = random.randint(1, 2)
        name = "behavior_inward_left_" + str(random_int)
        self.start_behavior_func(name)

    def inward_right(self):
        random_int = random.randint(1, 2)
        name = "behavior_inward_right_" + str(random_int)
        self.start_behavior_func(name)

    def outward(self):
        random_int = random.randint(1, 2)
        name = "behavior_outward_" + str(random_int)
        self.start_behavior_func(name)

    def outward_left(self):
        random_int = random.randint(1, 2)
        name = "behavior_outward_left_" + str(random_int)
        self.start_behavior_func(name)

    def outward_right(self):
        random_int = random.randint(1, 2)
        name = "behavior_outward_right_" + str(random_int)
        self.start_behavior_func(name)

    def random_inward_outward(self):
        random_int = random.randint(0, 9)
        if random_int == 0:
            self.inward()
        if random_int == 1:
            self.inward_left()
        if random_int == 2:
            self.inward_right()
        if random_int == 3:
            self.outward()
        if random_int == 4:
            self.outward_left()
        if random_int == 5:
            self.outward_right()
        if random_int == 6:
            self.forward_slow()
        if random_int == 7:
            self.forward_fast()
        if random_int == 8:
            self.backward_slow()
        if random_int == 9:
            self.backward_fast()

    def turn(self):
        if self.is_turned is False:
            self.is_turned = True
            name = "behavior_turn_back"
            self.start_behavior_func(name)
        else:
            self.is_turned = False
            name = "behavior_turn_toward"
            self.start_behavior_func(name)

    def turn_back(self):
        name = "behavior_turn_toward"
        self.start_behavior_func(name)

    def forward_fast(self):
        name = "behavior_move_up_fast"
        if self.is_turned is True:
            name = "behavior_move_down_fast"
        self.start_behavior_func(name)

    def forward_slow(self):
        name = "behavior_move_up_slow"

        if self.is_turned is True:
            name = "behavior_move_down_slow"

        self.start_behavior_func(name)

        current_time = datetime.datetime.now()
        with open('logfile.txt', 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s\n" % name)

    def backward_fast(self):
        name = "behavior_move_down_fast"
        if self.is_turned is True:
            name = "behavior_move_up_fast"
        self.start_behavior_func(name)

    def backward_slow(self):
        name = "behavior_move_down_slow"

        if self.is_turned is True:
            name = "behavior_move_up_slow"

        current_time = datetime.datetime.now()
        with open('logfile.txt', 'a') as f:
            f.write("%s," % str(current_time))
            f.write("%s\n" % name)

        self.start_behavior_func(name)


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        service.go_to_init()
        service.is_turned = False
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        t = tk.Label(self, text="HOME MENU")
        t.place(x=0, y=0)

        t = tk.Label(self, text="Condition 1: Improv (I)")
        t.place(x=100, y=100)
        t = tk.Label(self, text="Condition 2: Random (R)")
        t.place(x=100, y=150)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Task 1 (A)")
        label.pack(side="top", fill="both", expand=True)
        t = tk.Label(self, text="TASK 1: HEAD MOTION (IMPROV)")
        t.place(x=0, y=0)
        w1 = 10
        h1 = 10

        # colors
        c1 = "dark green"
        c2 = "light green"
        c3 = "cyan"

        h_axis = 10
        v_axis = 30

        w1 = 120
        h1 = 120

        p = os.getcwd() + "images/arrow_up_left_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_up_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "images/arrow_up_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_up_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 500
        w1 = 120
        h1 = 120

        p = os.getcwd() + "/images/arrow_up_right_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_up_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 100
        v_axis = 120
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_up_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_up_left_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_up.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_up_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 450
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_up_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_up_right_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        # left to right
        w1 = 80
        h1 = 160

        h_axis = 0
        v_axis = 260

        p = os.getcwd() + "/images/arrow_left_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 90

        p = os.getcwd() + "/images/arrow_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_left_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 470

        p = os.getcwd() + "/images/arrow_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_right_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 560

        p = os.getcwd() + "/images/arrow_right_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        # center
        h_axis = 190
        v_axis = 230

        h1 = 23
        w1 = 35

        button = tk.Button(self, text='center slow', bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_center_slow"))
        button.place(x=h_axis, y=v_axis)

        h1 = 8
        w1 = 12

        button = tk.Button(self, text='CENTER FAST', bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_center_fast"))
        button.place(x=h_axis + 80, y=v_axis + 75)

        # bottom left to right
        h_axis = 10
        v_axis = 570
        w1 = 130
        h1 = 130

        p = os.getcwd() + "/images/arrow_down_left_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_down_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_down_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_down_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis+35)

        h_axis = 500
        w1 = 130
        h1 = 130

        p = os.getcwd() + "/images/arrow_down_right_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_down_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 100
        v_axis = 500
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_down_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_down_left_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_down.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_down_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 450
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_down_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_look_down_right_slow"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        # center button
        t = tk.Label(self, text="CENTER SLOW", bg=c2)
        t.place(x=290, y=450)


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        t = tk.Label(self, text="TASK 1: HEAD MOTION (RANDOM)")
        t.place(x=0, y=0)

        # colors
        c1 = "#08458a"
        c2 = "#0078ff"

        h_axis = 10
        v_axis = 30

        w1 = 120
        h1 = 120

        p = os.getcwd() + "/images/arrow_up_left_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_up_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_up_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_up_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 500
        w1 = 120
        h1 = 120

        p = os.getcwd() + "/images/arrow_up_right_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_up_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 100
        v_axis = 120
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_up_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_up_left"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_up.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_up"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 450
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_up_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_up_right"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        # left to right
        w1 = 80
        h1 = 160

        h_axis = 0
        v_axis = 260

        p = os.getcwd() + "/images/arrow_left_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 90

        p = os.getcwd() + "/images/arrow_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_left"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 470

        p = os.getcwd() + "/images/arrow_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_right"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 560

        p = os.getcwd() + "/images/arrow_right_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        # center
        h_axis = 190
        v_axis = 230

        h1 = 23
        w1 = 35

        button = tk.Button(self, text='center slow', bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("center_slow"))
        button.place(x=h_axis, y=v_axis)

        h1 = 8
        w1 = 12

        button = tk.Button(self, text='CENTER FAST', bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("center_fast"))
        button.place(x=h_axis + 80, y=v_axis + 75)

        # bottom left to right
        h_axis = 10
        v_axis = 570
        w1 = 130
        h1 = 130

        p = os.getcwd() + "/images/arrow_down_left_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_down_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_down_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_down_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis+35)

        h_axis = 500
        w1 = 130
        h1 = 130

        p = os.getcwd() + "/images/arrow_down_right_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_down_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 100
        v_axis = 500
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_down_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_down_left"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 250
        w1 = 150
        h1 = 100

        p = os.getcwd() + "/images/arrow_down.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_down"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 450
        w1 = 100
        h1 = 100

        p = os.getcwd() + "/images/arrow_down_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.look_random("arrow_down_right"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        # center button
        t = tk.Label(self, text="CENTER SLOW", bg=c2)
        t.place(x=290, y=450)


class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        t = tk.Label(self, text="TASK 2: BASE MOTION (IMPROV)")
        t.place(x=0, y=0)

        h1 = 130
        w1 = 130

        # colors
        c1 = "dark green"
        c2 = "light green"
        c3 = "cyan"

        h_axis = 100
        v_axis = 50

        p = os.getcwd() + "/images/arrow_up_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.forward_fast())
        button.image = img
        button.place(x=h_axis, y=v_axis)

        v_axis = 190

        p = os.getcwd() + "/images/arrow_up.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.forward_slow())
        button.image = img
        button.place(x=h_axis, y=v_axis)

        v_axis = 380

        p = os.getcwd() + "/images/arrow_down.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.backward_slow())
        button.image = img
        button.place(x=h_axis, y=v_axis)

        v_axis = 520

        p = os.getcwd() + "/images/arrow_down_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.backward_fast())
        button.image = img
        button.place(x=h_axis, y=v_axis)

        t = tk.Label(self, text="TOWARD HUMAN")
        t.place(x=120, y=35)

        w1 = 25
        h1 = 15

        toggle_button = tk.Button(self, text="TURN 180", width=w1, height=h1, command=lambda: service.turn(), bg=c3)
        toggle_button.place(x=350, y=300)


class Page5(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        t = tk.Label(self, text="TASK 2: BASE MOTION (RANDOM)")
        t.place(x=0, y=0)

        h1 = 130
        w1 = 130

        # colors
        c2 = "#0078ff"
        c1 = "#08458a"
        c3 = "cyan"

        h_axis = 100
        v_axis = 50

        p = os.getcwd() + "/images/arrow_up_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.move_random("arrow_up_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        v_axis = 190

        p = os.getcwd() + "/images/arrow_up.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.move_random("arrow_up"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        v_axis = 380

        p = os.getcwd() + "/images/arrow_down.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c2, width=w1, height=h1,
                           command=lambda: service.move_random("arrow_down"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        v_axis = 520

        p = os.getcwd() + "/images/arrow_down_fast.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c1, width=w1, height=h1,
                           command=lambda: service.move_random("arrow_down_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        t = tk.Label(self, text="TOWARD HUMAN")
        t.place(x=120, y=35)

        w1 = 25
        h1 = 15

        toggle_button = tk.Button(self, text="TURN 180", width=w1, height=h1, command=lambda: service.move_random("turn"), bg=c3)
        toggle_button.place(x=350, y=300)


class Page6(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        w1 = 12
        h1 = 8
        c1 = "light green"
        c2 = "dark green"
        c3 = "cyan"
        w2 = 40
        h2 = 15

        h_axis = 20
        v_axis = 50

        t = tk.Label(self, text="TASK 3: INWARD & OUTWARD MOTION (IMPROV)")
        t.place(x=0, y=0)

        button = tk.Button(self, text='OUTWARD LEFT', bg=c2, width=w2, height=h2,
                           command=lambda: service.outward_left())
        button.place(x=h_axis, y=v_axis)
        button = tk.Button(self, text='INWARD LEFT', bg=c1, width=w1, height=h1,
                           command=lambda: service.inward_left())
        button.place(x=h_axis + 100, y=v_axis + 35)

        v_axis = 300

        button = tk.Button(self, text='OUTWARD BOTH', bg=c2, width=w2, height=h2,
                           command=lambda: service.outward())
        button.place(x=h_axis, y=v_axis)

        button = tk.Button(self, text='INWARD BOTH', bg=c1, width=w1, height=h1,
                           command=lambda: service.inward())
        button.place(x=h_axis + 100, y=v_axis + 35)

        v_axis = 550

        button = tk.Button(self, text='OUTWARD RIGHT', bg=c2, width=w2, height=h2,
                           command=lambda: service.outward_right())
        button.place(x=h_axis, y=v_axis)

        button = tk.Button(self, text='INWARD RIGHT', bg=c1, width=w1, height=h1,
                           command=lambda: service.inward_right())
        button.place(x=h_axis + 100, y=v_axis + 35)

        t = tk.Label(self, text="OUTWARD LEFT", bg=c2)
        t.place(x=130, y=200)
        t = tk.Label(self, text="OUTWARD BOTH", bg=c2)
        t.place(x=130, y=450)
        t = tk.Label(self, text="OUTWARD RIGHT", bg=c2)
        t.place(x=130, y=700)

        h_axis = 450
        v_axis = 240
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_up.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.forward_fast())
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 370
        v_axis = 350
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_move_left_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 510
        v_axis = 350
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.start_behavior_func("behavior_move_right_fast"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 450
        v_axis = 460
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_down.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.backward_fast())
        button.image = img
        button.place(x=h_axis, y=v_axis)

        t = tk.Label(self, text="BASE MOTION")
        t.place(x=460, y=220)


class Page7(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        t = tk.Label(self, text="TASK 3: INWARD & OUTWARD MOTION (RANDOM)")
        t.place(x=0, y=0)

        # colors
        c2 = "#0078ff"
        c1 = "#08458a"
        c3 = "cyan"

        w1 = 12
        h1 = 8
        w2 = 40
        h2 = 15

        h_axis = 20
        v_axis = 50

        t = tk.Label(self, text="TASK 3: INWARD & OUTWARD MOTION")
        t.place(x=0, y=0)

        button = tk.Button(self, text='OUTWARD LEFT', bg=c2, width=w2, height=h2,
                           command=lambda: service.inward_random("out_l"))
        button.place(x=h_axis, y=v_axis)
        button = tk.Button(self, text='INWARD LEFT', bg=c1, width=w1, height=h1,
                           command=lambda: service.inward_random("in_l"))
        button.place(x=h_axis + 100, y=v_axis + 35)

        v_axis = 300

        button = tk.Button(self, text='OUTWARD BOTH', bg=c2, width=w2, height=h2,
                           command=lambda: service.inward_random("out_both"))
        button.place(x=h_axis, y=v_axis)

        button = tk.Button(self, text='INWARD BOTH', bg=c1, width=w1, height=h1,
                           command=lambda: service.inward_random("in_both"))
        button.place(x=h_axis + 100, y=v_axis + 35)

        v_axis = 550

        button = tk.Button(self, text='OUTWARD RIGHT', bg=c2, width=w2, height=h2,
                           command=lambda: service.inward_random("out_r"))
        button.place(x=h_axis, y=v_axis)

        button = tk.Button(self, text='INWARD RIGHT', bg=c1, width=w1, height=h1,
                           command=lambda: service.inward_random("in_r"))
        button.place(x=h_axis + 100, y=v_axis + 35)

        t = tk.Label(self, text="OUTWARD LEFT", bg=c2)
        t.place(x=130, y=200)
        t = tk.Label(self, text="OUTWARD BOTH", bg=c2)
        t.place(x=130, y=450)
        t = tk.Label(self, text="OUTWARD RIGHT", bg=c2)
        t.place(x=130, y=700)

        h_axis = 450
        v_axis = 240
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_up.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.inward_random("up"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 370
        v_axis = 350
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_left.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.inward_random("left"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 510
        v_axis = 350
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_right.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.inward_random("right"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        h_axis = 450
        v_axis = 460
        w1 = 120
        h1 = 100

        p = os.getcwd() + "/images/arrow_down.png"
        img = Image.open(p)
        img = img.resize((w1, h1))
        img = ImageTk.PhotoImage(img)
        button = tk.Button(self, image=img, bg=c3, width=w1, height=h1,
                           command=lambda: service.inward_random("down"))
        button.image = img
        button.place(x=h_axis, y=v_axis)

        t = tk.Label(self, text="BASE MOTION")
        t.place(x=460, y=220)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)
        p5 = Page5(self)
        p6 = Page6(self)
        p7 = Page7(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p7.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        bottomframe = tk.Frame(self)
        bottomframe.pack(side="bottom")

        w1 = 8
        h1 = 5
        c1 = "#33fc42"
        c2 = "#0087ff"
        c11 = "#5d0303"

        b1 = tk.Button(buttonframe, text="Main menu", command=p1.show, width=w1, height=h1, bg=c11)
        b2 = tk.Button(buttonframe, text="TASK 1 (I)", command=p2.show, width=w1, height=h1, bg=c1)
        b3 = tk.Button(buttonframe, text="TASK 1 (R)", command=p3.show, width=w1, height=h1, bg=c2)
        b4 = tk.Button(buttonframe, text="TASK 2 (I)", command=p4.show, width=w1, height=h1, bg=c1)
        b5 = tk.Button(buttonframe, text="TASK 2 (R)", command=p5.show, width=w1, height=h1, bg=c2)
        b6 = tk.Button(buttonframe, text="TASK 3 (I)", command=p6.show, width=w1, height=h1, bg=c1)
        b7 = tk.Button(buttonframe, text="TASK 3 (R)", command=p7.show, width=w1, height=h1, bg=c2)

        w1 = 15
        h1 = 5

        b1.pack(side="left")

        b2.pack(side="left")
        b4.pack(side="left")
        b6.pack(side="left")

        b7.pack(side="right")
        b5.pack(side="right")
        b3.pack(side="right")

        c1 = "#fc5743"

        button = tk.Button(bottomframe, text='STOP MOTION', bg=c1, width=w1, height=h1,
                           command=lambda: service.stop_all_behaviors())

        button.pack(side="left")

        button = tk.Button(bottomframe, text='DEFAULT POSITION', bg=c1, width=w1, height=h1,
                           command=lambda: service.go_to_init())

        button.pack(side="left")

        button = tk.Button(bottomframe, text='WAKE UP', bg=c1, width=w1, height=h1,
                           command=lambda: service.motion_service_wake_up())

        button.pack(side="left")

        button = tk.Button(bottomframe, text='GO TO REST', bg=c1, width=w1, height=h1,
                           command=lambda: service.motion_service_rest())

        button.pack(side="left")

        bottomframe2 = tk.Frame(self)
        bottomframe2.pack(side="bottom")

        t = tk.Label(bottomframe2, text="EMERGENCY BUTTONS")
        t.pack(side="left")
        p1.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.167",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()

    print("Connecting to ", args.ip)

    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["Robot", "--qi-url=" + connection_url])

    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port))
        sys.exit(1)

    app.start()
    session = app.session

    service = Service(session)

    with open('log.txt', 'w') as f:
        f.write("%s," % "Time")
        f.write("%s\n" % "Behavior")

    s = "logfile2.txt"
    if not os.path.exists(s):
        with open(s, 'w') as f:
            f.write("%s," % "Time")
            f.write("%s," % "Button")
            f.write("%s," % "Behavior")
            f.write("%s\n" % "Condition")

    root = tk.Tk()

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("650x900")
    root.mainloop()

