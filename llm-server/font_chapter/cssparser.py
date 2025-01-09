import cssutils
from .exceptions import CSSParsingException 

def parse_css(css_text: str) -> list[dict[str, str]]:
    css_style_sheet = cssutils.parseString(css_text)
    css_rules: list[dict[str, str]] = []

    for rule in css_style_sheet:
        selector: str = rule.selectorText
        styles: list[str] = rule.style.cssText.split(";")

        css_sheet: dict = {"selector": selector}
        for style in styles:
            if len(style.strip().split(":")) == 2:
                param, value = style.strip().split(":")
            else:
                raise CSSParsingException(message=style)

            css_sheet[param] = value.strip()
        css_rules.append(css_sheet)

    return css_rules