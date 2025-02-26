from typing import Any

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, OptionList, Label, Checkbox, Pretty, Input
from textual.widgets.option_list import Option
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical
from artifex.auto_caption import mp3_to_srt

import tkinter as tk
from tkinter import filedialog

#Global Variables
file_path = ""
class SubScreen(ModalScreen):
    DEFAULT_CSS = """
        SubScreen {
            background: $panel;
            border: solid $boost;
        }
    """

class Auto_Editor(ModalScreen):

    def compose(self) -> ComposeResult:
        yield Label("Buy a car!")
        yield Label("Lots of car-oriented widgets here I guess!")
        yield Button("Buy!", id="buy")
        yield Button("Cancel", id="cancel")

    @on(Button.Pressed, "#buy")
    def buy_it(self) -> None:
        self.dismiss({
            "options": "everything -- really we'd ask"
        })

    @on(Button.Pressed, "#cancel")
    def cancel_purchase(self) -> None:
        self.dismiss({})

class Auto_Caption(ModalScreen):

    def compose(self) -> ComposeResult:
        # Here we compose up the question screen for a bike.
        yield Label("Auto Caption generates accurate SRT files by transcribing speech from MP3 audio, making it easy to add captions to your videos.\n",id="label")
        with Vertical():
            yield Label("Number of chars per subtitle line:")
            yield Input(type="integer",id="subtitle_size")
        with Vertical():
            yield Label("Select the mp3 file:")
            yield Button("No file selected",id="file_select")
        with Horizontal():
            yield Button("Start Automation", id="auto_caption")
            yield Button("Back", id="back")

    @on(Button.Pressed, "#auto_caption")
    def start_auto_caption(self) -> None:
        # This function start the automation for the auto caption
        self.query_one("#label").update(f"The automation has started")
        mp3_to_srt(file_path,int(self.query_one('#subtitle_size').value))
        self.query_one("#label").update(f"Finished!")

    @on(Button.Pressed, "#file_select")
    def file_selection(self) -> None:
        # This function start the automation for the auto caption
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        self.query_one("#label").update(f"the file is in {file_path}")
        root.destroy()
        return

    @on(Button.Pressed, "#back")
    def cancel_purchase(self) -> None:
        # Cancel was pressed. So here we'll return no-data.
        self.dismiss({})

class VehiclePurchaseApp(App[None]):
    CSS_PATH = 'styles.css'
    # Here you could create a structure of all of the types of vehicle, with
    # their names and the screen that asks the questions.
    AUTOMATION: dict[str, tuple[str, type[ModalScreen]]] = {
        "smart_editor": ("Smart Editor", Auto_Editor),
        "auto_caption": ("Auto Caption", Auto_Caption)
    }

    def compose(self) -> ComposeResult:
        # This builds the initial option list from the vehicles listed above.
        yield Label("Select the automation")
        yield OptionList(
            *[Option(name, identifier) for identifier, (name, _) in self.AUTOMATION.items()]
        )
        # The `Pretty` is just somewhere to show the result. See
        # selection_made below.
        yield Pretty("")

    def selection_made(self, selection: dict[str, Any]) -> None:
        # This is the method that receives the selection after the user has
        # asked to buy the vehicle. For now I'm just dumping the selection
        # into a `Pretty` widget to show it.
        self.query_one(Pretty).update(selection)

    @on(OptionList.OptionSelected)
    def next_screen(self, event: OptionList.OptionSelected) -> None:
        # If the ID of the option that was selected is known to us...
        if event.option_id in self.AUTOMATION:
            # ...create an instance of the screen associated with it, push
            # it and set up the callback.
            self.push_screen(self.AUTOMATION[event.option_id][1](), callback=self.selection_made)

if __name__ == "__main__":
    VehiclePurchaseApp().run()