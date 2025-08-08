import ast
import html
from io import StringIO
import sys

import air
import mistletoe
from mistletoe import block_token
from mistletoe.html_renderer import HtmlRenderer

from mdlive.utils import AirHTMLRenderer


class PythonLiveHtmlRenderer(AirHTMLRenderer):
    def render_block_code(self, token: block_token.BlockCode) -> str:
        template = "<pre><code{attr}>{inner}</code></pre>"
        if token.language == "python-live":
            code = token.content.strip()
            if not code:
                return ""

            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()

            try:
                exec(code)
                output = captured_output.getvalue()
                inner = self.escape_html_text(output)
                attr = ' class="language-python-live"'
                return template.format(attr=attr, inner=inner)
            except Exception as e:
                error_message = f"Error rendering python-live block: {e}"
                inner = self.escape_html_text(f"{code}\n\n{error_message}")
                attr = ' class="language-python-live-error"'
                return template.format(attr=attr, inner=inner)
            finally:
                sys.stdout = old_stdout

        return super().render_block_code(token)


class PythonLiveMarkdown(mistletoe.Document):
    def __init__(self, content):
        super().__init__(content)

    def __enter__(self):
        self.renderer = PythonLiveHtmlRenderer()
        return self

    def __exit__(self, *args):
        self.renderer = None
