
## train_1

**input:**
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 8 0 8 0
0 0 0 0 0 0 1 0 0 8 4 0
0 0 0 0 0 0 1 0 8 8 8 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 8 0 8 0 1 0 4 0 4 0
0 0 4 8 0 0 1 0 0 4 8 0
0 0 8 8 8 0 1 0 4 4 4 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 2 0 2 0 0 0
0 0 2 3 2 2 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 3 0 0 0
0 0 3 2 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 2 3 2 2 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 6 5 5 6 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

1.  **Input/Output Structure:** Both input and output are 2D grids of pixels with different colors.
2.  **Key Feature:** A prominent horizontal blue line (color 1) exists in all examples, dividing the grid into an upper and a lower section. This blue line remains unchanged in the output.
3.  **Transformation:** The core transformation appears to be a reflection across the horizontal blue line, combined with a color swap.
4.  **Objects:** Objects are contiguous blocks of non-white (color 0) and non-blue (color 1) pixels. These objects exist either entirely above or entirely below the blue line in the input.
5.  **Reflection Action:**
    *   Objects *above* the blue line in the input are reflected *below* the blue line in the output. The reflection is symmetrical with respect to the blue line's row index.
    *   Objects *below* the blue line in the input are reflected *above* the blue line in the output.
    *   The original objects are removed from their initial positions in the output grid, leaving white pixels (color 0) behind, unless overwritten by a reflected object.
6.  **Color Swapping:** During the reflection, specific pairs of colors are swapped:
    *   Example 1: Azure (8) swaps with Yellow (4).
    *   Example 2: Red (2) swaps with Green (3).
    *   Example 3: Gray (5) swaps with Magenta (6).
7.  **Symmetry:** The reflection preserves the shape and relative positions of the pixels within an object, but flips it vertically across the blue line. The distance of each pixel from the blue line remains the same but on the opposite side.

**YAML Facts:**


```yaml
elements:
  - type: grid
    description: Input and output are 2D grids of colored pixels.
  - type: line
    color: blue (1)
    orientation: horizontal
    role: separator & axis_of_reflection
    persistence: remains unchanged between input and output
  - type: object
    description: Contiguous block of non-white (0), non-blue (1) pixels.
    location: Located entirely above or entirely below the blue line in the input.
    properties:
      - color
      - shape
      - position_relative_to_blue_line
actions:
  - name: find_blue_line
    input: input_grid
    output: row_index_of_blue_line
  - name: identify_objects
    input: input_grid
    criteria: contiguous pixels not color 0 or 1
    output: list_of_objects (with their pixels, colors, locations)
  - name: reflect_and_swap_color
    input: object, blue_line_row_index
    process:
      - determine if object is above or below the blue line
      - calculate new row index for each pixel based on reflection across blue_line_row_index
      - swap color of each pixel based on predefined pairs
    output: reflected_object (with new locations and swapped colors)
  - name: construct_output_grid
    process:
      - start with a white grid of the same dimensions as the input
      - copy the blue line from the input to the output
      - place the reflected_and_swapped objects onto the output grid
color_swaps:
  - pair: [azure (8), yellow (4)]
  - pair: [red (2), green (3)]
  - pair: [gray (5), magenta (6)]
relationships:
  - input_object maps to reflected_output_object
  - pixel distance from blue line is preserved but mirrored
  - specific color pairs are mutually swapped during reflection
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, filled with the background color (white, 0).
2.  Identify the row index of the horizontal blue line (color 1) in the input grid.
3.  Copy the blue line from the input grid to the same row index in the output grid.
4.  Iterate through each pixel in the input grid.
5.  If a pixel is *not* white (0) and *not* blue (1):
    a.  Determine its original row (`r_orig`) and column (`c`).
    b.  Determine its original color (`color_orig`).
    c.  Calculate the vertical distance (`dist`) from the pixel's row to the blue line's row (`blue_line_row`). `dist = r_orig - blue_line_row`.
    d.  Calculate the reflected row index (`r_refl`) by flipping the distance: `r_refl = blue_line_row - dist`.
    e.  Determine the swapped color (`color_swapped`) based on the original color:
        *   If `color_orig` is azure (8), `color_swapped` is yellow (4).
        *   If `color_orig` is yellow (4), `color_swapped` is azure (8).
        *   If `color_orig` is red (2), `color_swapped` is green (3).
        *   If `color_orig` is green (3), `color_swapped` is red (2).
        *   If `color_orig` is gray (5), `color_swapped` is magenta (6).
        *   If `color_orig` is magenta (6), `color_swapped` is gray (5).
        *   (Assume other colors, if any, remain unchanged, although none are present in examples).
    f.  Place the `color_swapped` pixel at the calculated reflected position (`r_refl`, `c`) in the output grid.
6.  Return the completed output grid.
```python
import numpy as np

"""
The transformation reflects non-white (0) and non-blue (1) pixels across a
horizontal blue line (color 1) while swapping specific pairs of colors.

1. Find the row index of the horizontal blue line.
2. Initialize an output grid of the same dimensions as the input, filled with white (0).
3. Copy the blue line from the input to the output grid.
4. Define the color swap pairs: Azure(8) <-> Yellow(4), Red(2) <-> Green(3), Gray(5) <-> Magenta(6).
5. Iterate through each pixel of the input grid.
6. If a pixel is neither white (0) nor blue (1):
   a. Calculate its vertical distance from the blue line.
   b. Determine the reflected row index by mirroring the distance across the blue line.
   c. Determine the swapped color based on the original color using the defined pairs.
   d. Place the swapped color at the reflected position (same column, reflected row) in the output grid.
7. Return the output grid.
"""

# Define the color swapping pairs
COLOR_SWAP_MAP = {
    8: 4,  # Azure -> Yellow
    4: 8,  # Yellow -> Azure
    2: 3,  # Red -> Green
    3: 2,  # Green -> Red
    5: 6,  # Gray -> Magenta
    6: 5,  # Magenta -> Gray
    # Add other colors here if needed, mapping them to themselves if they don't swap
    0: 0,  # White maps to White (background)
    1: 1,  # Blue maps to Blue (reflection line)
    7: 7,  # Orange maps to Orange (example not seen, but logical)
    9: 9   # Maroon maps to Maroon (example not seen, but logical)
}

def find_blue_line_row(grid):
    """Finds the row index of the first horizontal line of blue pixels (1)."""
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 1):
            return r
        # Check if at least one blue pixel exists in the row (might be sufficient for some ARC tasks)
        # More robust check might be needed depending on variations,
        # but examples show full blue lines.
        if 1 in grid[r,:]:
             # Check if the entire row is either blue (1) or white (0)
             # This handles cases where the line doesn't span the whole grid width
             is_line = True
             for c in range(grid.shape[1]):
                 if grid[r, c] != 1 and grid[r,c] != 0:
                    is_line = False
                    break
             if is_line and np.any(grid[r,:] == 1): # Ensure there's at least one blue pixel
                 return r


    # Check columns if no horizontal line found (less likely based on description)
    # for c in range(grid.shape[1]):
    #     if np.all(grid[:, c] == 1):
    #         # Handle vertical line case if necessary
    #         pass # Not needed for this specific task description

    return -1 # Indicate not found

def transform(input_grid):
    """
    Applies the reflection and color swap transformation based on a horizontal blue line.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with background color (white, 0)
    output_np = np.zeros_like(input_np)

    # Find the row index of the blue line
    blue_line_row = find_blue_line_row(input_np)

    if blue_line_row == -1:
        # Handle error: Blue line not found. Maybe return input or raise error.
        # For ARC, often returning the input or an empty grid might be expected.
        # Based on examples, assume it's always present.
        print("Error: Blue line not found!")
        return input_grid # Or handle differently

    # Copy the blue line itself to the output grid
    # We only copy the blue pixels, preserving the white background where the input might have 0s on the line row
    for c in range(width):
        if input_np[blue_line_row, c] == 1:
             output_np[blue_line_row, c] = 1


    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            original_color = input_np[r, c]

            # Skip background (white) and the blue line itself
            if original_color == 0 or r == blue_line_row:
                continue

            # Calculate distance from the blue line
            # Positive distance means below the line, negative means above
            dist = r - blue_line_row

            # Calculate the reflected row index
            reflected_r = blue_line_row - dist

            # Check if the reflected row is within grid bounds
            if 0 <= reflected_r < height:
                # Get the swapped color
                swapped_color = COLOR_SWAP_MAP.get(original_color, original_color) # Default to original if not in map

                # Place the swapped color at the reflected position in the output grid
                # Important: Only place if the target cell is currently background (0)
                # or if this is the intended behavior based on potential overlaps.
                # The examples suggest overwriting is fine.
                output_np[reflected_r, c] = swapped_color

    # Convert back to list of lists if required by the ARC environment
    return output_np.tolist()
```
```python
import numpy as np

"""
The transformation identifies a primary axis line (horizontal or vertical) composed 
of blue (1) and white (0) pixels, selecting the one with the most blue pixels. 
It then reflects all non-white, non-axis pixels across this line, swapping 
their colors according to specific pairs: Azure(8) <-> Yellow(4), 
Red(2) <-> Green(3), Gray(5) <-> Magenta(6). The axis line itself (only the 
blue pixels) is preserved in the output.
"""

# Define the color swapping pairs
COLOR_SWAP_MAP = {
    8: 4,  # Azure -> Yellow
    4: 8,  # Yellow -> Azure
    2: 3,  # Red -> Green
    3: 2,  # Green -> Red
    5: 6,  # Gray -> Magenta
    6: 5,  # Magenta -> Gray
    # Identity mappings for other colors (including background and axis color)
    0: 0,
    1: 1,
    7: 7,
    9: 9
}

def find_reflection_axis(grid):
    """
    Finds the reflection axis (a line of blue(1) and white(0) pixels).
    Selects the axis (horizontal or vertical) with the maximum number of blue pixels.
    """
    height, width = grid.shape
    best_axis_type = None
    best_axis_idx = -1
    max_blue_count = 0

    # Check horizontal candidates
    for r in range(height):
        is_potential_axis = True
        blue_count = 0
        for c in range(width):
            pixel = grid[r, c]
            if pixel == 1:
                blue_count += 1
            elif pixel != 0: # Must be only 0s and 1s
                is_potential_axis = False
                break
        if is_potential_axis and blue_count > 0:
            if blue_count > max_blue_count:
                 max_blue_count = blue_count
                 best_axis_type = 'horizontal'
                 best_axis_idx = r
            # Simple tie-breaking: prefer horizontal if counts are equal
            elif blue_count == max_blue_count and best_axis_type == 'vertical':
                 best_axis_type = 'horizontal'
                 best_axis_idx = r


    # Check vertical candidates
    for c in range(width):
        is_potential_axis = True
        blue_count = 0
        for r in range(height):
             pixel = grid[r, c]
             if pixel == 1:
                 blue_count += 1
             elif pixel != 0: # Must be only 0s and 1s
                is_potential_axis = False
                break
        if is_potential_axis and blue_count > 0:
             if blue_count > max_blue_count:
                 max_blue_count = blue_count
                 best_axis_type = 'vertical'
                 best_axis_idx = c
             # Tie-breaking already handled (prefer horizontal if equal)

    return best_axis_type, best_axis_idx


def transform(input_grid):
    """
    Applies the reflection and color swap transformation based on the identified axis.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # initialize output_grid with background color (white, 0)
    output_np = np.zeros_like(input_np)

    # Find the axis of reflection
    axis_type, axis_idx = find_reflection_axis(input_np)

    if axis_type is None:
        # No axis found - return the input grid or an empty grid?
        # Based on examples, an axis should always be present.
        # Returning input might be safer for unexpected cases.
        print("Warning: No reflection axis found.")
        return input_grid

    # Copy the blue pixels from the axis line to the output grid
    if axis_type == 'horizontal':
        for c in range(width):
            if input_np[axis_idx, c] == 1:
                output_np[axis_idx, c] = 1
    elif axis_type == 'vertical':
        for r in range(height):
            if input_np[r, axis_idx] == 1:
                output_np[r, axis_idx] = 1

    # Iterate through each pixel of the input grid to reflect and swap
    for r in range(height):
        for c in range(width):
            original_color = input_np[r, c]

            # Skip background color (0)
            if original_color == 0:
                continue

            # Skip pixels on the axis line itself
            if axis_type == 'horizontal' and r == axis_idx:
                continue
            if axis_type == 'vertical' and c == axis_idx:
                continue

            # Calculate reflected position
            reflected_r, reflected_c = r, c # Initialize
            if axis_type == 'horizontal':
                reflected_r = (2 * axis_idx) - r
            elif axis_type == 'vertical':
                reflected_c = (2 * axis_idx) - c

            # Check if the reflected position is within grid bounds
            if 0 <= reflected_r < height and 0 <= reflected_c < width:
                # Get the swapped color
                swapped_color = COLOR_SWAP_MAP.get(original_color, original_color)

                # Place the swapped color at the reflected position in the output grid
                output_np[reflected_r, reflected_c] = swapped_color

    # Convert back to list of lists for the expected output format
    return output_np.tolist()
```
