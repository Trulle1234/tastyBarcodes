from typing import Sequence
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

def menu(
    title: str | Sequence[str],
    options: list[str] | tuple[str, ...],
    cursor_color: str = "green",
    title_color: str = "cyan",
    options_color: str = "white",
    initial_cursor_position: int = 0,
) -> str:

    index = initial_cursor_position
    result = {"choice": None}

    def get_text():
        lines = []

        # Title
        if isinstance(title, str):
            lines.append((f"class:title", title))
        else:
            for line in title:
                lines.append(("class:title", line))

        lines.append(("", ""))

        # Options
        for i, option in enumerate(options):
            if i == index:
                lines.append(("class:cursor", f"> {option}"))
            else:
                lines.append(("class:option", f"  {option}"))

        return lines

    kb = KeyBindings()

    @kb.add("up")
    def move_up(event):
        nonlocal index
        index = (index - 1) % len(options)
        event.app.invalidate()

    @kb.add("down")
    def move_down(event):
        nonlocal index
        index = (index + 1) % len(options)
        event.app.invalidate()

    @kb.add("enter")
    def select(event):
        result["choice"] = options[index]
        event.app.exit()

    style = Style.from_dict({
        "title": title_color,
        "option": options_color,
        "cursor": cursor_color,
    })

    root = HSplit([
        Window(
            content=FormattedTextControl(get_text),
            always_hide_cursor=True
        )
    ])

    app = Application(
        layout=Layout(root),
        key_bindings=kb,
        style=style,
        full_screen=True
    )

    app.run()
    return result["choice"]
