"""Main module."""

from .python_live import PythonLiveMarkdown


def render(text: str) -> str:
    """Renders a string with the PythonLiveMarkdown renderer.

    Args:
        text: The text to render.

    Returns:
        The rendered HTML.
    """
    with PythonLiveMarkdown(text) as renderer:
        return renderer.render()
