from app.parser.base import BaseParser


class TemplateExist(BaseParser):
    def __init__(self, template, show_match):
        super().__init__(show_match)
        self.template = template

    def parse_image(self, rgb, grey, *args, **kwargs):
        return self.match_template(grey, self.template) is not None
