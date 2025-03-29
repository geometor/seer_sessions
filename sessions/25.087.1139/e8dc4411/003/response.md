```python
import numpy as np
from collections import Counter

"""
The transformation rule identifies a unique 'source' pixel in the input grid, distinguished by its color being neither the predominant background color nor white (0). Based on the color of this source pixel, a specific predefined pattern of relative coordinates is selected. This pattern is then applied relative to the source pixel's location, changing the pixels in the output grid at the calculated target coordinates to the source pixel's color. The background and other elements like white pixels remain unchanged unless overwritten by the pattern application.
"""

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid, ignoring white (0)."""
    # Flatten the grid to easily count colors
    colors = grid.flatten()
    # Count occurrences of each color, excluding white (0)
    color_counts = Counter(c for c in colors if c != 0)
    # Handle cases where no non-white colors exist (e.g., all white grid)
    if not color_counts:
        # If the grid might be entirely white or empty, return 0 as default background
        # In ARC, typically a dominant background exists.
        # If only white, returning 0 seems reasonable.
        all_counts = Counter(colors)
        if all_counts:
            return all_counts.most_common(1)[0][0] # Return most frequent overall (likely 0)
        else:
            return 0 # Default for empty grid
    # Return the most frequent non-white color
    return color_counts.most_common(1)[0][0]

def find_source_pixel(grid, background_color):
    """Finds the unique pixel that is not the background color and not white (0)."""
    source_pixel_info = None
    found_count = 0
    # Iterate through each pixel in the grid
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            # Check if the pixel color is neither background nor white
            if color != background_color and color != 0:
                # Store the found pixel's info
                source_pixel_info = {'row': r, 'col': c, 'color': color}
                found_count += 1
    # Validate that exactly one source pixel was found
    if found_count == 1:
         return source_pixel_info
    else:
        # Log a warning or raise an error if 0 or >1 source pixels are found
        # This indicates the assumption of a unique source pixel is violated.
        print(f"Warning/Error: Found {found_count} source pixels. Expected exactly 1.")
        return None # Indicate failure to find a unique source

def transform(input_grid):
    """
    Applies a color-specific pattern anchored at a unique source pixel.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # 1. Initialize: Create a copy of the input grid for the output
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 2. Identify Background: Find the most common color, ignoring white
    background_color = find_most_frequent_color(grid)

    # 3. Find Source Pixel: Locate the unique pixel that's not background and not white
    source_pixel = find_source_pixel(grid, background_color)

    # Proceed only if a unique source pixel was successfully found
    if source_pixel is None:
        print("Error: Could not find a unique source pixel. Returning original grid.")
        # If no unique source, return the unchanged copy
        return output_grid.tolist()

    source_row = source_pixel['row']
    source_col = source_pixel['col']
    source_color = source_pixel['color']

    # 4. Define Color Patterns: Map source colors to sets of relative (dr, dc) coordinates
    # Corrected pattern for green (3) based on Example 1 analysis
    patterns = {
        3: {(0, 0), (1, -1), (1, 0), (1, 1), (2, -2), (2, 0), (3, -3), (3, -2), (3, -1), (4, -4), (4, -2), (5, -4), (5, -3)}, # Green (Corrected)
        2: {(0, 0), (1, -1), (1, 1), (2, 0), (2, 2), (3, 1), (3, 3), (4, 2), (4, 4), (5, 3), (5, 5), (6, 4), (6, 6)}, # Red
        8: {(-4, 0), (-4, 1), (-4, 3), (-4, 4), (-3, 0), (-3, 1), (-3, 3), (-3, 4), (-2, 2), (-1, 0), (-1, 1), (-1, 3), (-1, 4), (0, 0), (0, 1), (0, 3), (0, 4)}  # Azure
    }

    # 5. Select Pattern: Get the pattern corresponding to the source pixel's color
    selected_pattern = patterns.get(source_color)

    # Proceed only if a pattern is defined for the source color
    if selected_pattern is None:
        print(f"Warning: No pattern defined for source color {source_color}. Returning original grid.")
        # If no pattern exists for this color, return the unchanged copy
        return output_grid.tolist()

    # 6. Apply Pattern: Iterate through each offset in the selected pattern
    for dr, dc in selected_pattern:
        # 7. Calculate Target Coordinates: Add offset to source location
        target_row = source_row + dr
        target_col = source_col + dc

        # 8. Update Output Grid: Check bounds and apply the source color
        # Check if the calculated target coordinates are within the grid boundaries
        if 0 <= target_row < rows and 0 <= target_col < cols:
            # Change the color of the pixel at the target location in the output grid
            output_grid[target_row, target_col] = source_color

    # 9. Finalize: Convert the NumPy array back to a list of lists and return
    return output_grid.tolist()
```