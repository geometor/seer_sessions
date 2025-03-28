import numpy as np
from typing import List, Tuple, Dict, Set

"""
Transformation Rule:

1.  **Identify Target:** Locate the single non-white pixel (target_color) below row 1. Its position becomes the center (center_pos) for the output structure.
2.  **Analyze Top Row:**
    a.  Find the rightmost non-white pixel in row 0 (frame_color, frame_col).
    b.  Collect all non-white pixels in row 0 to the left of frame_col (sequence_colors).
3.  **Determine Layer Colors:** Create an ordered list `layer_colors` by:
    a. Starting with target_color.
    b. Appending the unique colors from sequence_colors, sorted numerically.
    c. Appending frame_color.
    d. Remove duplicates while preserving this order.
4.  **Modify Top Row (Conditional):** If the pixel at (0, frame_col - 1) in the input is white (0) and frame_col > 0, change the pixel at (0, frame_col) in the output to the color below it in the input (which is gray, 5).
5.  **Construct Concentric Structure:**
    a.  Initialize the output grid as a copy of the input.
    b.  Set the pixel at center_pos in the output to the first color in `layer_colors`.
    c.  For each subsequent color in `layer_colors` at index `i` (starting i=1):
        i.  Draw a hollow square frame of size (2*i + 1) x (2*i + 1) centered at center_pos using the current color.
        ii. The frame consists of pixels exactly `i` distance (Manhattan or Chebyshev) away from the center pixel.
"""

def find_target_pixel(grid: np.ndarray) -> Tuple[int, Tuple[int, int]]:
    """Finds the single non-white pixel below row 1."""
    height, width = grid.shape
    for r in range(2, height):
        for c in range(width):
            if grid[r, c] != 0:
                return grid[r, c], (r, c)
    # Should not happen based on task description, but good practice
    raise ValueError("Target pixel not found below row 1")

def analyze_top_row(grid: np.ndarray) -> Tuple[int, int, List[int]]:
    """Analyzes row 0 to find frame color/column and sequence colors."""
    width = grid.shape[1]
    frame_color = 0
    frame_col = -1
    sequence_colors = []

    # Find rightmost non-white pixel (frame_color, frame_col)
    for c in range(width - 1, -1, -1):
        if grid[0, c] != 0:
            frame_color = grid[0, c]
            frame_col = c
            break

    if frame_col == -1:
         # Handle case where top row is all white (unlikely based on examples)
         return 0, -1, []

    # Collect sequence colors to the left of frame_col
    for c in range(frame_col):
        if grid[0, c] != 0:
            sequence_colors.append(grid[0, c])

    return frame_color, frame_col, sequence_colors

def determine_layer_colors(target_color: int, sequence_colors: List[int], frame_color: int) -> List[int]:
    """Determines the ordered list of unique colors for the concentric layers."""
    unique_sequence_colors = sorted(list(set(sequence_colors)))
    # Combine in the specified order: target, sorted unique sequence, frame
    combined_colors = [target_color] + unique_sequence_colors + [frame_color]

    # Remove duplicates while preserving the established order
    layer_colors = []
    seen: Set[int] = set()
    for color in combined_colors:
        if color not in seen:
            layer_colors.append(color)
            seen.add(color)
    return layer_colors

def draw_hollow_square(grid: np.ndarray, center_r: int, center_c: int, layer_index: int, color: int):
    """Draws a hollow square frame for a given layer index."""
    height, width = grid.shape
    top = center_r - layer_index
    bottom = center_r + layer_index
    left = center_c - layer_index
    right = center_c + layer_index

    # Draw top row
    if 0 <= top < height:
        for c in range(max(0, left), min(width, right + 1)):
            grid[top, c] = color
    # Draw bottom row
    if 0 <= bottom < height:
        for c in range(max(0, left), min(width, right + 1)):
             grid[bottom, c] = color
    # Draw left column (excluding corners already drawn)
    if 0 <= left < width:
        for r in range(max(0, top + 1), min(height, bottom)):
             grid[r, left] = color
    # Draw right column (excluding corners already drawn)
    if 0 <= right < width:
        for r in range(max(0, top + 1), min(height, bottom)):
            grid[r, right] = color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the identified rules:
    - Identifies a target pixel and a color sequence from the top row.
    - Creates concentric squares around the target pixel using colors derived from the sequence.
    - Conditionally modifies a pixel in the top row.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Identify Target
    try:
        target_color, center_pos = find_target_pixel(input_np)
        center_r, center_c = center_pos
    except ValueError as e:
        print(f"Error: {e}. Returning input grid.") # Or handle appropriately
        return input_grid

    # 2. Analyze Top Row
    frame_color, frame_col, sequence_colors = analyze_top_row(input_np)

    # 3. Determine Layer Colors
    if frame_col != -1: # Only proceed if a frame color was found
        layer_colors = determine_layer_colors(target_color, sequence_colors, frame_color)
    else:
        # If no frame color, maybe just draw the target pixel? Or depends on spec.
        # Based on examples, this case doesn't occur. Let's assume layers require a frame_color.
        layer_colors = [target_color] # Default to just the target color if top row analysis fails


    # 4. Modify Top Row (Conditional)
    if frame_col > 0: # Check if there's a pixel to the left
        modifier_pixel_color = input_np[0, frame_col - 1]
        if modifier_pixel_color == 0:
            replacement_color = input_np[1, frame_col] # Color from row below
            output_np[0, frame_col] = replacement_color

    # 5. Construct Concentric Structure
    # Clear the area where the structure will be drawn? No, examples show only drawing the structure pixels.
    # The target pixel might be overwritten by the drawing loop, so set it first.
    # Set center pixel (layer 0)
    if len(layer_colors) > 0:
         if 0 <= center_r < height and 0 <= center_c < width:
              output_np[center_r, center_c] = layer_colors[0]

    # Draw subsequent layers (frames)
    for i in range(1, len(layer_colors)):
        color = layer_colors[i]
        draw_hollow_square(output_np, center_r, center_c, i, color)


    # Convert back to list of lists for the expected output format
    return output_np.tolist()