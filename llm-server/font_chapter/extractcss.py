import re 

from .cssparser import parse_css
from .exceptions import CSSParsingException
from .prompts import breakdown_to_html, style_extraction_prompt
from .skeleton import messages

def css_extractor(images: list[dict[str, str]], gpt4o, gpt4o_encoder): 
    css_rules: list[dict[str, str]] = []
    font_combinations: list[dict[str, int| str]] = []
    token_count: int = 0 

    for idx, image in enumerate(images):
        messages[1]["content"][0]["text"] = breakdown_to_html
        messages[1]["content"][1]["image_url"]["url"] = (
            f"data:image/jpeg;base64,{image['img_b64']}")

        completions = gpt4o.chat.completions.create(
            messages = messages,
            model = "gpt-4o-mini",
            temperature=0.01
        )

        html_response: str = completions.choices[0].message.content
        token_count += len(gpt4o_encoder.encode(html_response)) 

        if re.findall(r"```html(.*?)```", html_response, re.DOTALL):
            html_content: str = re.findall(r"```html(.*?)```", html_response, re.DOTALL)[0]

        prompt: str = style_extraction_prompt.format(html_content)
        messages[1]["content"][0]["text"] = prompt
        messages[1]["content"][1]["image_url"]["url"] = (
            f"data:image/jpeg;base64,{image['img_b64']}")

        completions = gpt4o.chat.completions.create(
            messages = messages,
            model = "gpt-4o-mini",
            temperature=0.01
        )

        css_response: str = completions.choices[0].message.content
        token_count += len(gpt4o_encoder.encode(css_response)) 
        if re.findall(r"```css(.*?)```", css_response, re.DOTALL):
            css_content: str = re.findall(r"```css(.*?)```", css_response, re.DOTALL)[0]
            try: 
                css_dict = parse_css(css_content)
            except CSSParsingException as cssError: 
                raise CSSParsingException(message=cssError.message)

        css_rules.extend(css_dict)
        font_combinations.append({
            "index": idx,
            "style": css_dict,
        })
    
    return font_combinations, css_rules, token_count 
