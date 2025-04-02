import numpy as np
import collections

"""
Identify a rectangular frame made of gray (5) pixels in the input grid.
Determine the background color ('bg') from inside the frame (e.g., top-left inner pixel).
Create an output grid matching the frame's dimensions.
Copy the gray frame to the output grid.
Fill the inside of the output frame with the background color 'bg'.
Define two possible 3x3 output pattern structures based on 'bg':
  - Structure A (if bg=8): [[fill, bg, fill], [fill, fill, fill], [fill, fill, fill]]
  - Structure D (if bg=1): [[bg, fill, fill], [bg, fill, fill], [bg, fill, bg]]
  (Assume Structure A for any bg other than 1 for potential generalization).
Define two sets of color mappings from input 'key_color' to output 'fill' color, based on 'bg':
  - Mapping 8 (if bg=8): {Green(3): Red(2), Blue(1): Yellow(4)}
  - Mapping 1 (if bg=1): {Red(2): Yellow(4), Magenta(6): Orange(7), Green(3): Azure(8)}
  (Assume Mapping 8 for any bg other than 1 for potential generalization).
Iterate through the input grid's content area (inside the frame) in non-overlapping 3x3 blocks.
For each 3x3 input block:
  - Identify the 'key_color': Find the first color in the block that is not 'bg' and is a valid key in the active color mapping.
  - If a 'key_color' is found:
    - Determine the 'output_fill_color' using the active color mapping.
    - Select the active output pattern structure template.
    - Create the specific 3x3 output pattern by substituting 'fill' with 'output_fill_color' and using the correct 'bg'.
    - Place this output pattern onto the corresponding 3x3 location in the output grid (relative to the frame).
Return the final output grid.
"""

def find_frame_bounds(grid, frame_color=5):
    """Finds the min/max row/col for a given frame color."""
    rows, cols = np.where(grid == frame_color)
    if rows.size == 0:
        # Handle cases where the frame color is not found
        # Based on examples, a frame is expected. Raise error or return None.
        # For robustness, let's try finding any non-background object's bounds
        # But the task strongly implies a gray frame. Let's assume it exists.
        raise ValueError("Frame color not found in grid")
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    return min_r, max_r, min_c, max_c

def get_key_color(block, bg, valid_keys):
    """Finds the first valid key color in the block."""
    # Flatten the block and check each color
    for color in block.flatten():
        if color != bg and color in valid_keys:
            return color
    return None # No valid key color found

def create_pattern(structure_type, bg, fill_color):
    """Creates the 3x3 output pattern based on type, bg, and fill color."""
    pattern = np.full((3, 3), fill_color, dtype=np.int8)
    if structure_type == 'A':
        # [[fill, bg, fill], [fill, fill, fill], [fill, fill, fill]]
        pattern[0, 1] = bg
    elif structure_type == 'D':
        # [[bg, fill, fill], [bg, fill, fill], [bg, fill, bg]]
        pattern[0, 0] = bg
        pattern[1, 0] = bg
        pattern[2, 0] = bg
        pattern[2, 2] = bg
    else:
         # Default or error case - let's default to structure A
         pattern[0, 1] = bg

    return pattern


def transform(input_grid):
    """
    Transforms the input grid based on pattern replacement within a frame,
    adapting patterns and colors based on the frame's internal background color.
    """
    input_grid_np = np.array(input_grid, dtype=np.int8)
    frame_color = 5

    try:
        min_r, max_r, min_c, max_c = find_frame_bounds(input_grid_np, frame_color)
    except ValueError:
         # If no frame found, maybe return input or default?
         # Based on examples, returning input seems unlikely to be correct.
         # Let's return an empty grid or a copy for safety, although error is likely better.
         return input_grid # Or np.array([[]])

    # Determine output grid size
    output_h = max_r - min_r + 1
    output_w = max_c - min_c + 1

    # Determine background color from inside the frame
    # Ensure indices are valid if frame is only 1 pixel thick (although examples aren't)
    bg_r, bg_c = min_r + 1, min_c + 1
    if bg_r > max_r -1 or bg_c > max_c -1:
         # Handle very thin frames - maybe just use frame color? Unlikely based on ARC tasks.
         # Or check multiple locations? For now, assume frame is thick enough.
         # Let's find the most common color inside the frame excluding the frame color itself.
         inner_area = input_grid_np[min_r+1:max_r, min_c+1:max_c]
         if inner_area.size > 0:
             colors, counts = np.unique(inner_area, return_counts=True)
             if colors.size > 0 :
                # Find most frequent color inside that isn't frame color
                bg = colors[counts.argmax()] # Simplistic, assumes single dominant bg
                # A more robust way might be needed if bg is noisy
             else:
                 bg = 0 # Default if inner area empty? Should not happen based on examples.
         else:
             # If frame is too thin, maybe default bg?
             bg = 0 # Default background
    else:
        bg = input_grid_np[bg_r, bg_c]


    # Initialize output grid and fill with background
    output_grid = np.full((output_h, output_w), bg, dtype=np.int8)

    # Copy the frame
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if input_grid_np[r, c] == frame_color:
                out_r, out_c = r - min_r, c - min_c
                output_grid[out_r, out_c] = frame_color

    # Define structures and mappings based on background color
    if bg == 1:
        structure_type = 'D'
        color_map = {2: 4, 6: 7, 3: 8} # Input: Output
    else: # Defaulting to bg=8 behavior for other backgrounds
        structure_type = 'A'
        color_map = {3: 2, 1: 4} # Input: Output


    valid_input_keys = set(color_map.keys())

    # Iterate through input content area in 3x3 steps
    # Start from the first potential top-left corner inside the frame
    # Ensure steps don't go past the inner boundary
    for r in range(min_r + 1, max_r - 1, 3): # Step by 3, stop before last 2 rows
         # Check if the block fits entirely within the inner frame bounds
         if r + 3 > max_r: continue
         for c in range(min_c + 1, max_c - 1, 3): # Step by 3, stop before last 2 cols
            if c + 3 > max_c: continue

            # Extract 3x3 block
            in_block = input_grid_np[r:r+3, c:c+3]

            # Find the key color
            key_color = get_key_color(in_block, bg, valid_input_keys)

            if key_color is not None:
                # Get the corresponding output fill color
                output_fill_color = color_map[key_color]

                # Create the output pattern
                output_pattern = create_pattern(structure_type, bg, output_fill_color)

                # Calculate output position (relative to output grid 0,0)
                out_r = r - min_r
                out_c = c - min_c

                # Place pattern in output grid
                # Ensure the pattern fits within the output grid bounds (should always if frame copied correctly)
                if out_r + 3 <= output_h and out_c + 3 <= output_w:
                   output_grid[out_r:out_r+3, out_c:out_c+3] = output_pattern
                else:
                    # This case should ideally not happen if logic is correct
                    print(f"Warning: Pattern placement out of bounds at ({out_r}, {out_c})")


    return output_grid.tolist() # Return as list of lists per ARC format