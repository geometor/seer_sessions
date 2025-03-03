from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Button

# Define a color palette mapping for grid values (0-9) to colors
COLOR_PALETTE = {
    0: "black",
    1: "red",
    2: "green",
    3: "yellow",
    4: "blue",
    5: "magenta",
    6: "cyan",
    7: "white",
    8: "#ff8800",  # orange
    9: "#00ffff",  # cyan variant
}

# Example ARC-style grid data (each number corresponds to a color in COLOR_PALETTE)
GRID_DATA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 1, 1, 4, 3, 2, 1],
    [1, 2, 3, 4, 1, 1, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class BaseGrid(Static):
    """Base widget class for rendering the colored grid."""
    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

class ImageGrid(BaseGrid):
    """Grid rendered using an image-based approach via rich-pixels (requires PIL and rich-pixels)."""
    def on_mount(self):
        # Import PIL and rich-pixels inside the method to avoid requiring them if not using this mode.
        try:
            from PIL import Image
            from rich_pixels import Pixels
        except ImportError:
            # If dependencies are not installed, show a message instead of the image.
            self.update("Image rendering requires 'Pillow' and 'rich-pixels' libraries.")
            return

        # Determine cell pixel size for the image to maintain a good resolution.
        # Each grid cell will be a square block of pixels in the image.
        cell_pixel_size = 10  # pixels per grid cell side (adjust for resolution)
        img_width = self.cols * cell_pixel_size
        img_height = self.rows * cell_pixel_size

        # Create a new image with a black background
        image = Image.new("RGB", (img_width, img_height), COLOR_PALETTE.get(0, "black"))
        # Fill the image with the grid's colors
        for r in range(self.rows):
            for c in range(self.cols):
                color = COLOR_PALETTE.get(self.grid[r][c], "black")
                # Convert color to an RGB tuple (Pillow accepts color names or hex, but ensure consistency)
                rgb_color = Image.new("RGB", (1, 1), color).getpixel((0, 0))
                # Fill the rectangular region for this cell
                for y in range(r * cell_pixel_size, (r+1) * cell_pixel_size):
                    for x in range(c * cell_pixel_size, (c+1) * cell_pixel_size):
                        image.putpixel((x, y), rgb_color)
        # Create a Pixels renderable from the PIL image
        pixels = Pixels.from_image(image)
        # Update the widget content with the Pixels renderable (Rich renderable)&#8203;:contentReference[oaicite:2]{index=2}
        self.update(pixels)
    
    def on_resize(self, event):
        """Regenerate the image when the widget is resized to adjust scaling."""
        try:
            from PIL import Image
            from rich_pixels import Pixels
        except ImportError:
            return  # If libraries are missing, skip regeneration
        if self.cols == 0 or self.rows == 0:
            return

        new_width, new_height = event.size  # available size in terminal cells
        # Calculate a new pixel size per cell based on available space (simple heuristic)
        factor_x = max(1, new_width // self.cols)
        factor_y = max(1, new_height // self.rows)
        cell_pixel_size = min(factor_x, factor_y) * 2  # use *2 for more detail in cells
        img_width = self.cols * cell_pixel_size
        img_height = self.rows * cell_pixel_size

        image = Image.new("RGB", (img_width, img_height), COLOR_PALETTE.get(0, "black"))
        for r in range(self.rows):
            for c in range(self.cols):
                color = COLOR_PALETTE.get(self.grid[r][c], "black")
                rgb_color = Image.new("RGB", (1, 1), color).getpixel((0, 0))
                for y in range(r * cell_pixel_size, (r+1) * cell_pixel_size):
                    for x in range(c * cell_pixel_size, (c+1) * cell_pixel_size):
                        image.putpixel((x, y), rgb_color)
        pixels = Pixels.from_image(image)
        self.update(pixels)

class UnicodeBlockGrid(BaseGrid):
    """Grid rendered using colored Unicode blocks (using colored spaces or block characters)."""
    def render(self):
        # Create a Rich Text object with colored blocks for each cell
        from rich.text import Text
        text = Text()
        # Determine cell width (in characters) to approximate a square.
        cell_width = 2  # default to 2 spaces per cell for better aspect ratio
        if hasattr(self, "size"):
            avail_width = self.size.width
            # If not enough width for 2 chars per cell, use 1 char per cell
            if avail_width and avail_width < self.cols * 2:
                cell_width = 1
        # Build each line of the grid
        for i, row in enumerate(self.grid):
            for value in row:
                color = COLOR_PALETTE.get(value, "black")
                # Use space characters with background color to represent a cell
                text.append(" " * cell_width, style=f"on {color}")
            if i != self.rows - 1:
                text.append("\n")  # newline after each row except the last
        return text

class HalfBlockGrid(BaseGrid):
    """Grid rendered by combining two rows into one using half-block characters."""
    def render(self):
        from rich.text import Text
        text = Text()
        # Pair up rows and use '▀' (upper half block) for each cell pair
        for r in range(0, self.rows, 2):
            if r < self.rows - 1:
                top_row = self.grid[r]
                bottom_row = self.grid[r+1]
                for c in range(self.cols):
                    top_color = COLOR_PALETTE.get(top_row[c], "black")
                    bottom_color = COLOR_PALETTE.get(bottom_row[c], "black")
                    # '▀' character: foreground color fills top half, background color fills bottom half
                    text.append("▀", style=f"{top_color} on {bottom_color}")
                text.append("\n")
        # If an odd number of rows, render the last row on its own (full block for each cell)
        if self.rows % 2 == 1:
            last_row = self.grid[-1]
            for c in range(self.cols):
                val_color = COLOR_PALETTE.get(last_row[c], "black")
                # Use '▀' with same color for fg and bg to render a full block of that color
                text.append("▀", style=f"{val_color} on {val_color}")
        return text

class ARCGridApp(App):
    """Textual Application to display the ARC-style grid with switchable rendering modes."""
    CSS = """
    Screen {
        align: center middle;
    }
    """  # Center content on screen (optional)
    def compose(self) -> ComposeResult:
        # Create a horizontal container of buttons for mode selection
        button_bar = Horizontal(
            Button("Image", id="mode_image"),
            Button("Unicode", id="mode_unicode"),
            Button("Half-Block", id="mode_half"),
            id="button_bar"
        )
        # Initialize each rendering widget with the grid data
        self.image_grid = ImageGrid(GRID_DATA, id="image_grid")
        self.unicode_grid = UnicodeBlockGrid(GRID_DATA, id="unicode_grid")
        self.halfblock_grid = HalfBlockGrid(GRID_DATA, id="halfblock_grid")
        # Hide all but one mode initially (show Unicode mode by default here)
        self.image_grid.styles.display = "none"
        self.halfblock_grid.styles.display = "none"
        # Yield the widgets to build the UI
        yield button_bar
        yield self.image_grid
        yield self.unicode_grid
        yield self.halfblock_grid

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Callback when a mode switch button is pressed."""
        # Hide all rendering widgets
        self.image_grid.styles.display = "none"
        self.unicode_grid.styles.display = "none"
        self.halfblock_grid.styles.display = "none"
        # Show the selected widget based on button ID
        if event.button.id == "mode_image":
            self.image_grid.styles.display = "block"
        elif event.button.id == "mode_unicode":
            self.unicode_grid.styles.display = "block"
        elif event.button.id == "mode_half":
            self.halfblock_grid.styles.display = "block"
        # Refresh the layout to apply the visibility changes&#8203;:contentReference[oaicite:3]{index=3}
        self.refresh()

# Run the application
if __name__ == "__main__":
    app = ARCGridApp()
    app.run()

