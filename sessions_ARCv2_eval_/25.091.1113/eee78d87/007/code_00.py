"""
Transforms an input grid into a 16x16 output grid.
The process involves:
1. Analyzing the input grid to find the dominant color (D) and, if present, a single minority color (M).
2. Creating a 16x16 background grid pattern based on D and M:
   - If M is 3 (Green) or the input is monochromatic (M is None), the pattern uses white (0) for grid lines (r%3==0 or c%3==0) and D elsewhere.
   - If M is 1 (Blue), the pattern uses D for grid lines and white (0) elsewhere.
   - If M is 6 (Magenta), the pattern alternates between the Green/Monochromatic pattern and the Blue pattern based on whether the column block index (c//3) is even or odd.
3. If the input grid was not monochromatic, a fixed maroon (9) 'H' shape is overlaid onto the background grid.
4. The final 16x16 grid is returned.
"""

import numpy as np
from collections import Counter

def analyze_input_colors(grid_np):
    """
    Analyzes the input numpy grid to find dominant and minority colors.

    Args:
        grid_np: The input grid as a numpy array.

    Returns:
        A tuple: (dominant_color, minority_color, is_monochromatic)
        minority_color is None if the grid is monochromatic.
    """
    counts = Counter(grid_np.flatten())
    most_common = counts.most_common()

    dominant_color = None
    minority_color = None
    is_monochromatic = True

    if not most_common:
        # Handle empty grid case, default to white dominant, monochromatic
        dominant_color = 0
        minority_color = None
        is_monochromatic = True
        return dominant_color, minority_color, is_monochromatic

    # Determine dominant color
    dominant_color = most_common[0][0]

    # Check for minority color
    if len(most_common) > 1:
        is_monochromatic = False
        # Find the first color that is not the dominant one.
        # Assumes only one minority color type based on examples.
        all_colors = list(counts.keys())
        for color in all_colors:
            if color != dominant_color:
                minority_color = color
                break
    
    # Ensure colors are standard ints, not numpy types which can cause issues later
    dominant_color = int(dominant_color)
    if minority_color is not None:
        minority_color = int(minority_color)

    return dominant_color, minority_color, is_monochromatic

def create_background_grid(rows, cols, dominant_color, minority_color):
    """
    Creates the base 16x16 output grid with the appropriate pattern
    based on the minority color.

    Args:
        rows: Number of rows for the output grid (16).
        cols: Number of columns for the output grid (16).
        dominant_color: The dominant color from the input.
        minority_color: The minority color from the input (or None).

    Returns:
        A 16x16 numpy array representing the background grid.
    """
    grid = np.zeros((rows, cols), dtype=int)

    # Determine which pattern function to use based on minority color
    if minority_color == 1: # Blue minority color -> Pattern B
        pattern_func = lambda r, c, D: D if r % 3 == 0 or c % 3 == 0 else 0
    elif minority_color == 6: # Magenta minority color -> Pattern C (Alternating)
        pattern_func = lambda r, c, D: (0 if r % 3 == 0 or c % 3 == 0 else D) if (c // 3) % 2 == 0 else (D if r % 3 == 0 or c % 3 == 0 else 0)
    else: # Default pattern (Green: 3, or Monochromatic: None, or any other minority) -> Pattern A
        pattern_func = lambda r, c, D: 0 if r % 3 == 0 or c % 3 == 0 else D

    # Apply the selected pattern to fill the grid
    for r in range(rows):
        for c in range(cols):
            grid[r, c] = pattern_func(r, c, dominant_color)

    return grid

def overlay_h_shape(grid_np):
    """
    Overlays the fixed 'H' shape in maroon (9) onto the grid.
    Modifies the grid in place.

    Args:
        grid_np: The numpy grid (16x16) to modify.
    """
    # Coordinates for the 'H' shape
    h_coords = [
        (5, 6), (5, 9),
        (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
        (7, 6), (7, 9),
        (8, 6), (8, 9),
        (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10),
        (10, 6), (10, 9),
    ]
    # Set the specified coordinates to maroon (9)
    for r, c in h_coords:
        # Bounds check is good practice, though fixed 16x16 output makes it less critical here
        if 0 <= r < grid_np.shape[0] and 0 <= c < grid_np.shape[1]:
             grid_np[r, c] = 9 # maroon
    # The grid_np is modified in place, no explicit return needed but Python passes mutable objects by reference

def transform(input_grid):
    # Convert input list of lists to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    output_rows, output_cols = 16, 16

    # Step 1: Analyze input colors to find dominant (D), minority (M), and if monochromatic
    dominant_color, minority_color, is_monochromatic = analyze_input_colors(input_np)

    # Step 2: Create the background grid based on the determined colors and pattern rules
    output_grid_np = create_background_grid(output_rows, output_cols, dominant_color, minority_color)

    # Step 3: Overlay the fixed 'H' shape if the input was not monochromatic
    if not is_monochromatic:
        overlay_h_shape(output_grid_np) # Modifies output_grid_np in place

    # Step 4: Convert the final numpy grid back to list of lists for the required output format
    return output_grid_np.tolist()