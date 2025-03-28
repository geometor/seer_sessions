```python
import numpy as np
from typing import List, Tuple, Dict, Set

"""
Transformation Rule:

1.  **Initialize Output:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Target:** Locate the single non-white pixel (`target_color`) in the input grid at or below row 2. Record its position (`center_r`, `center_c`).
3.  **Analyze Top Row (Row 0):**
    a.  Find the rightmost non-white pixel. Record its color (`frame_color`) and column index (`frame_col`). This column index defines the maximum radius (`max_radius`) of the structure to be drawn.
    b.  Collect the colors of all non-white pixels in row 0 located to the left of `frame_col`. Record these as `sequence_colors`.
4.  **Determine Layer Colors:** Construct an ordered list of unique colors (`layer_colors`) for the concentric structure:
    a.  Start with `target_color`.
    b.  Append the unique colors from `sequence_colors`, sorted numerically (by color value).
    c.  Append `frame_color`.
    d.  Remove any duplicate colors from this combined list while preserving the relative order established in steps a-c. Let the final number of unique colors be `num_layers`.
5.  **Modify Top Row (Conditional):** Check if `frame_col` is greater than 0 and if the pixel at `(0, frame_col - 1)` in the *input* grid is white (0).
    a.  If both conditions are true, change the color of the pixel at `(0, frame_col)` in the *output* grid to the color of the pixel directly below it in the *input* grid (i.e., the color at `(1, frame_col)`).
6.  **Construct Concentric Structure:**
    a.  Set the pixel at the center position (`center_r`, `center_c`) in the output grid to the first color in `layer_colors` (`layer_colors[0]`).
    b.  Iterate through radii `r` from 1 up to `max_radius` (inclusive):
        i.  Determine the color for the current radius `r`: If `r` is less than `num_layers`, use the color `layer_colors[r]`. Otherwise (if `r` is greater than or equal to `num_layers`), use the last color in the list, `layer_colors[num_layers - 1]`.
        ii. Draw a hollow square frame using this determined color. The frame consists of all pixels that are exactly at a Chebyshev distance of `r` from the center position (`center_r`, `center_c`). Ensure the drawing stays within the grid boundaries. Pixels drawn overwrite any existing colors at those locations in the output grid.
"""

def find_target_pixel(grid: np.ndarray) -> Tuple[int, Tuple[int, int]]:
    """Finds the single non-white pixel at or below row 2."""
    height, width = grid.shape
    for r in range(2, height):
        for c in range(width):
            if grid[r, c] != 0:
                return grid[r, c], (r, c)
    # Should not happen based on task examples, but raise error if no target found
    raise ValueError("Target pixel not found at or below row 2")

def analyze_top_row(grid: np.ndarray) -> Tuple[int, int, List[int]]:
    """Analyzes row 0 to find frame color, frame column (max radius), and sequence colors."""
    width = grid.shape[1]
    frame_color = 0
    frame_col = -1 # Represents max_radius
    sequence_colors = []

    # Find rightmost non-white pixel (frame_color, frame_col)
    for c in range(width - 1, -1, -1):
        if grid[0, c] != 0:
            frame_color = grid[0, c]
            frame_col = c
            break

    if frame_col == -1:
         # Handle case where top row is all white (or no non-white pixel found)
         # Based on examples, this shouldn't happen. If it did, structure size is undefined.
         # Returning -1 for frame_col allows the caller to handle this.
         return 0, -1, []

    # Collect sequence colors to the left of frame_col
    for c in range(frame_col):
        if grid[0, c] != 0:
            sequence_colors.append(grid[0, c])

    return frame_color, frame_col, sequence_colors

def determine_layer_colors(target_color: int, sequence_colors: List[int], frame_color: int) -> List[int]:
    """Determines the ordered list of unique colors for the concentric layers."""
    # Get unique sequence colors and sort them numerically
    unique_sequence_colors = sorted(list(set(sequence_colors)))
    
    # Combine in the specified order: target, sorted unique sequence, frame
    combined_colors = [target_color] + unique_sequence_colors + [frame_color]

    # Remove duplicates while preserving the established order
    layer_colors: List[int] = []
    seen: Set[int] = set()
    for color in combined_colors:
        if color not in seen:
            layer_colors.append(color)
            seen.add(color)
            
    # Filter out white (0) if it somehow got included, shouldn't happen with non-white logic
    layer_colors = [c for c in layer_colors if c != 0] 
            
    return layer_colors

def draw_hollow_square_frame(grid: np.ndarray, center_r: int, center_c: int, radius: int, color: int):
    """Draws a hollow square frame (perimeter) at a given radius (Chebyshev distance) from the center."""
    height, width = grid.shape
    # Calculate boundaries
    top = center_r - radius
    bottom = center_r + radius
    left = center_c - radius
    right = center_c + radius

    # Draw top row of the frame
    if 0 <= top < height:
        for c in range(max(0, left), min(width, right + 1)):
            grid[top, c] = color
    # Draw bottom row of the frame
    if 0 <= bottom < height:
        for c in range(max(0, left), min(width, right + 1)):
             grid[bottom, c] = color
    # Draw left column (excluding corners already drawn by top/bottom)
    if 0 <= left < width:
        for r in range(max(0, top + 1), min(height, bottom)):
             grid[r, left] = color
    # Draw right column (excluding corners already drawn by top/bottom)
    if 0 <= right < width:
        for r in range(max(0, top + 1), min(height, bottom)):
            grid[r, right] = color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Initialize Output: Create a copy of the input grid
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 2. Identify Target
    try:
        target_color, center_pos = find_target_pixel(input_np)
        center_r, center_c = center_pos
    except ValueError as e:
        # If no target pixel is found (violates problem assumption), return the original grid
        print(f"Error: {e}. Returning input grid unchanged.") 
        return input_grid

    # 3. Analyze Top Row (Row 0)
    frame_color, max_radius, sequence_colors = analyze_top_row(input_np)

    # Check if top row analysis was successful (max_radius != -1)
    if max_radius == -1:
        print("Warning: No frame pixel found in top row. Cannot determine structure size. Returning input grid.")
        # Or potentially just draw the target pixel? Returning copy for now.
        if 0 <= center_r < height and 0 <= center_c < width:
             output_np[center_r, center_c] = target_color # At least place the target?
        return output_np.tolist()

    # 4. Determine Layer Colors
    layer_colors = determine_layer_colors(target_color, sequence_colors, frame_color)
    num_layers = len(layer_colors) # Number of unique colors available including center

    if num_layers == 0: # Should not happen if target_color is non-zero
        print("Warning: No layer colors determined. Returning input grid.")
        return output_np.tolist()

    # 5. Modify Top Row (Conditional)
    # Check if there's a pixel to the left (max_radius > 0) and if it's white
    if max_radius > 0 and input_np[0, max_radius - 1] == 0:
        # Check bounds for the pixel below
        if 1 < height: # Ensure row 1 exists
             replacement_color = input_np[1, max_radius] # Color from row below
             output_np[0, max_radius] = replacement_color
        # Else: row 1 doesn't exist, do nothing

    # 6. Construct Concentric Structure
    # a. Set the center pixel (radius 0)
    if 0 <= center_r < height and 0 <= center_c < width:
        output_np[center_r, center_c] = layer_colors[0]

    # b. Iterate through radii r from 1 up to max_radius
    for r in range(1, max_radius + 1):
        # i. Determine the color for the current radius r
        if r < num_layers:
            # Use the color specified for this layer index (r)
            color_for_radius = layer_colors[r]
        else:
            # If radius exceeds available unique colors, reuse the last available color
            color_for_radius = layer_colors[num_layers - 1]
            
        # ii. Draw the hollow square frame for this radius
        draw_hollow_square_frame(output_np, center_r, center_c, r, color_for_radius)

    # Convert back to list of lists for the expected output format
    return output_np.tolist()
```