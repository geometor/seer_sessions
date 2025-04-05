```python
import numpy as np
from collections import Counter

def _find_dominant_color(grid_np):
    """Finds the non-zero color with the highest frequency."""
    # Flatten the grid and filter out the background color (0)
    non_zero_colors = grid_np[grid_np != 0]

    # Handle cases with no non-zero colors
    if non_zero_colors.size == 0:
        return None

    # Count frequencies
    color_counts = Counter(non_zero_colors)

    # Find the color with the maximum count
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def _has_dominant_neighbor(grid_np, r, c, dominant_color):
    """Checks if a cell has an orthogonally adjacent neighbor with the dominant color."""
    rows, cols = grid_np.shape
    # Define orthogonal neighbor offsets
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for nr, nc in neighbors:
        # Check if neighbor is within grid bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if the neighbor has the dominant color
            if grid_np[nr, nc] == dominant_color:
                return True
    return False

def transform(input_grid):
    """
    Filters a grid based on color dominance and connectivity.

    1. Identifies the most frequent non-zero color (dominant color).
    2. Removes all other non-zero colors (minority colors).
    3. Removes dominant color cells that do not have at least one
       orthogonally adjacent neighbor also containing the dominant color.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output_grid with zeros (background color)
    output_grid_np = np.zeros_like(input_np)

    # Find the dominant color
    dominant_color = _find_dominant_color(input_np)

    # If there's no dominant color (e.g., all zeros input), return the zero grid
    if dominant_color is None:
        return output_grid_np.tolist() # Convert back to list of lists

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_np[r, c]

            # Check if the current cell contains the dominant color
            if current_color == dominant_color:
                # Check if this cell has at least one orthogonal neighbor with the dominant color
                if _has_dominant_neighbor(input_np, r, c, dominant_color):
                    # If it has a dominant neighbor, keep the dominant color in the output grid
                    output_grid_np[r, c] = dominant_color
            # Cells with minority colors or isolated dominant colors remain 0 (background)

    # Convert the result back to a list of lists before returning
    return output_grid_np.tolist()
```