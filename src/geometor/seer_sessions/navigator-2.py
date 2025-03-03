# arc_visualizer.py

import asyncio
import random
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Header, Footer, Static, Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from io import BytesIO

class GridRenderer:
    """Handles rendering grids using Matplotlib."""

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))  # Adjust figure size as needed
        self.canvas = FigureCanvasAgg(self.fig)

    def render_grid(self, grid_data):
        """Renders a given grid."""
        self.ax.clear()  # Clear previous plot
        self.ax.imshow(grid_data, cmap='tab10', interpolation='nearest')  # Use a colormap
        self.ax.set_xticks(np.arange(grid_data.shape[1]))
        self.ax.set_yticks(np.arange(grid_data.shape[0]))
        self.ax.set_xticklabels([])  # Hide tick labels
        self.ax.set_yticklabels([])
        self.ax.tick_params(length=0) # Hide tick marks
        self.ax.grid(color='black', linewidth=1)  # Optional: Add grid lines


        # Render to a buffer
        buf = BytesIO()
        self.canvas.print_png(buf)
        buf.seek(0)
        return buf.read()

    def close(self):
      """closes the matplotlib window"""
      plt.close(self.fig)

class ImageDisplay(Static):
    """Widget to display the rendered image."""
    def __init__(self):
        super().__init__("")
        self.image_data = None

    def update_image(self, image_data):
        """Updates the displayed image."""
        self.image_data = image_data
        self.refresh() #important to repaint

    def render(self) -> str:  # Use Textual's render system (more efficient)
        if self.image_data:
            # Very basic "rendering" -- just indicates image is present.
            #  For true rendering, we'd need a terminal that supports image protocols (like iTerm2 or Kitty).
            return "[Image Present]"
        return "[No Image]"



class ARCVisualizerApp(App):
    """Textual app for visualizing ARC grids."""

    CSS_PATH = "arc_visualizer.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("q", "quit", "Quit"),
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer = GridRenderer()
        self.image_display = ImageDisplay()


    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        with Horizontal():
            with Vertical(id="button-panel"):
                yield Button("Grid 1", id="grid1")
                yield Button("Grid 2", id="grid2")
                yield Button("Random Grid", id="random_grid")
            yield self.image_display
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        grid_data = None

        if event.button.id == "grid1":
            grid_data = np.array([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ])
        elif event.button.id == "grid2":
            grid_data = np.array([
                [9, 8, 7],
                [6, 5, 4],
                [3, 2, 1]
            ])
        elif event.button.id == "random_grid":
            size = random.randint(3, 10)  # Vary grid size
            grid_data = np.random.randint(0, 10, size=(size, size))

        if grid_data is not None:
            image_data = self.renderer.render_grid(grid_data)
            self.image_display.update_image(image_data)  # Update through the widget

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_quit(self) -> None:
      self.renderer.close()
      self.exit()

    async def on_shutdown_request(self) -> None:
        """Ensure matplotlib resources are released."""
        self.renderer.close()


if __name__ == "__main__":
    app = ARCVisualizerApp()
    app.run()
