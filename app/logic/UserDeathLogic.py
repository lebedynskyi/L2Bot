import wmi


class UserDeathLogic:
    def __init__(self, death_parser, player):
        self.death_parser = death_parser
        self.player = player

    def check_is_dead(self, screenshot_image):
        is_dead = self.death_parser.parse_image(screenshot_image)
        if is_dead:
            print("DeadParser: Player dead")
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
                break
        else:
            print("DeadParser: Game not found")
