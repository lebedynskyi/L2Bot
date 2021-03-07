import re

prog = re.compile('[+\-*=\s^/]|[0-9]+')


class CaptchaSolver:
    def __init__(self):
        pass

    def is_ariphmetic(self, text):
        math_chars = prog.findall(text)
        return len(math_chars) >= 5 and "=" in text

    def solve_math(self, text):
        phrase = self._extract_math_phrase(text)

        # print("Solver: Math phrase > %s" % phrase)
        # parts = phrase.partition("=")
        # print("Solver parts > %s" % "'".join(parts))
        # math_result = eval(parts[0])
        # print("Solver math answer > %s" % math_result)
        pass

    def solve_logic(self, text):
        print("Solver: Logic phrase > %s" % text)
        pass

    def _extract_math_phrase(self, text):
        equals_index = text.index("=")
        left = []
        right = []
        for i in reversed(range(1, equals_index)):
            char = text[i]
            result = prog.match(char)
            if result is not None:
                left.append(char)
            else:
                break

        for i in range(equals_index + 1, len(text)):
            char = text[i]
            result = prog.match(char)
            if result is not None:
                right.append(char)
            else:
                break

        left_part = "".join(reversed(left)).strip()
        right_part = "".join(right).strip()
        eval_result = str(eval(left_part))
        print(f"Solver: Left part > {left_part}, right part > {right_part}, eval > {eval_result}, result > {eval_result == right_part}")
        return left_part, right_part
