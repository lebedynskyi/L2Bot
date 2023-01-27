import random
import re

regexp = re.compile('[+\-*=\s^/]|[0-9]+')


class CaptchaSolver:
    def __init__(self):
        pass

    def solve(self, captcha_text):
        if self._is_ariphmetic(captcha_text):
            result = self._solve_math(captcha_text)
        else:
            result = self._solve_logic(captcha_text)

        return result

    def _is_ariphmetic(self, text):
        math_chars = regexp.findall(text)
        return len(math_chars) >= 5 and "=" in text

    def _solve_math(self, text):
        phrase, answer, eval_answer = self._extract_math_phrase(text)
        # True - OK. False - Cancel
        click_action = self._extract_action(text)
        if eval_answer == answer:
            return click_action
        else:
            return not click_action

    def _solve_logic(self, text):
        return self._extract_action(text)

    def _extract_math_phrase(self, text):
        equals_index = text.index("=")
        left = []
        right = []
        for i in reversed(range(1, equals_index)):
            char = self._sanitize_math_char(text[i])
            result = regexp.match(char)
            if result is not None:
                left.append(char)
            else:
                break

        for i in range(equals_index + 1, len(text)):
            char = self._sanitize_math_char(text[i], right_part=True)
            result = regexp.match(char)
            if result is not None:
                right.append(char)
            else:
                break

        left_part = "".join(reversed(left)).strip()
        right_part = "".join(right).strip()
        eval_result = str(eval(left_part))
        print(
            f"Solver: Left part > {left_part}, right part > {right_part}, eval > {eval_result}, result > {eval_result == right_part}")
        return left_part, right_part, eval_result

    def _extract_action(self, text):
        words = text.lower().split()
        click_index = None

        for word in words:
            if word.find('click') != -1:
                click_index = words.index(word)
                break

        if click_index is None:
            random_bit = random.getrandbits(1)
            return bool(random_bit)

        action = "".join(words[click_index + 1:click_index + 2])
        print("Solver: dialog click action > %s" % action)
        return len(action) <= 4

    def _sanitize_math_char(self, char, right_part = False):
        mapping = {
            'D': '0',
            'A': '4',
            '?': '7'
        }

        # When condition like 1+7=8?
        # We need to keep '?' for preventing wrong result: 1+7=87
        if right_part and char == '?':
            return char

        return mapping.get(char, char)
