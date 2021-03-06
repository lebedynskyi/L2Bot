import re


class CaptchaSolver:
    def __init__(self):
        pass

    def is_ariphmetic(self, text):
        math_phrase = re.findall('[+\-*=^/()]|[0-9.]+', text)
        if len(math_phrase) >= 5:
            return "".join(math_phrase)
        else:
            return None

    def solve_math(self, math):
        print("Solver: Math phrase > %s" % math)
        pass

    def solve_logic(self, text):
        print("Solver: Logic phrase > %s" % text)
        pass
