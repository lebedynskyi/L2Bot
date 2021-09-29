import wmi
import cv2


class UserDeathLogic:
    def __init__(self, death_parser, player):
        self.death_parser = death_parser
        self.player = player

    def on_tick(self, screenshot_image, current_time):
        is_dead = self.death_parser.parse_image(screenshot_image)
        if is_dead:
            print("DeadParser: Player dead")
            cv2.imwrite("output/last_death.png", screenshot_image)
            self.player.play_warning()
            self.kill_game()

    def kill_game(self):
        f = wmi.WMI()
        for process in f.Win32_Process():
            name = process.name
            print(name)
            if name == "l2.exe":
                process.Terminate()
                print("DeadParser: Game killed")
                exit(1)
                break
        else:
            print("DeadParser: Game not found")
