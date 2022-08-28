import re


class PatternMatcher:

    @staticmethod
    def match(pattern, text):
        return re.match(pattern, text)
