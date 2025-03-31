
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 36.363636363636346

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 3 2 3 3 0 0 0
0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.925925925925924

## Example 3:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 6 5 5 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.974025974025977
**General Assessment:**

The previous code correctly identified the color swapping rule and the concept of reflection. However, it failed because it incorrectly assumed the reflection axis (the blue line) was always horizontal. Analysis of the failed examples reveals:

1.  **Example 1:** The blue line is *vertical*, and the reflection occurs horizontally across this line. The previous code failed to detect the vertical line.
2.  **Examples 2 & 3:** The blue line is *horizontal*. The previous code correctly identified the line and reflected objects from *below* the line to *above*. However, it failed to reflect objects from *above* the line to *below*. This indicates an issue in how the reflection was applied or perhaps in the iteration logic, although the core reflection calculation seems sound for both directions. The most likely culprit remains the axis detection failing in Example 1, leading to subsequent errors. The errors in Examples 2 & 3 showing only half the reflection might stem from how the output grid was populated or an unexpected interaction after the failed axis detection in Example 1 (though unlikely as executions are separate). A re-evaluation of the pixel processing loop is warranted, ensuring *all* non-background, non-axis pixels are processed and placed correctly.

**Strategy:**

1.  Implement a robust axis detection function that identifies both horizontal and vertical blue lines (composed of blue '1' and potentially white '0' pixels, but containing at least one '1').
2.  Adapt the reflection logic to work correctly for both horizontal and vertical axes.
3.  Ensure the identified axis (blue line) is accurately copied to the output grid.
4.  Verify that the loop iterates through all relevant input pixels and correctly calculates the reflected position and color swap for each, placing them onto the output grid.

**Metrics and Verification:**

Let's verify the axis detection and type for each example.


*code_execution:*
```python
import numpy as np

def find_axis(grid_list):
    grid = np.array(grid_list, dtype=int)
    height, width = grid.shape
    axis_type = None
    axis_idx = -1

    # Check horizontal
    for r in range(height):
        is_potential_axis = True
        has_blue = False
        for c in range(width):
            if grid[r, c] == 1:
                has_blue = True
            elif grid[r, c] != 0:
                is_potential_axis = False
                break
        if is_potential_axis and has_blue:
            axis_type = 'horizontal'
            axis_idx = r
            print(f"Found horizontal axis at row {r}")
            return axis_type, axis_idx

    # Check vertical if no horizontal found
    if axis_type is None:
        for c in range(width):
            is_potential_axis = True
            has_blue = False
            for r in range(height):
                 if grid[r, c] == 1:
                     has_blue = True
                 elif grid[r, c] != 0:
                     is_potential_axis = False
                     break
            if is_potential_axis and has_blue:
                axis_type = 'vertical'
                axis_idx = c
                print(f"Found vertical axis at col {c}")
                return axis_type, axis_idx

    if axis_type is None:
        print("No axis found")
    return axis_type, axis_idx

# Example 1 Input
grid1 = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 8, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 8, 4, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
]
print("Example 1:")
axis1_type, axis1_idx = find_axis(grid1)
print(f"Result: {axis1_type}, {axis1_idx}")

# Example 2 Input
grid2 = [
    [0, 0, 0, 2, 0, 2, 0, 0, 0],
    [0, 0, 2, 3, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\nExample 2:")
axis2_type, axis2_idx = find_axis(grid2)
print(f"Result: {axis2_type}, {axis2_idx}")

# Example 3 Input
grid3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 6, 6, 5, 0, 0, 0, 0, 0],
    [0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\nExample 3:")
axis3_type, axis3_idx = find_axis(grid3)
print(f"Result: {axis3_type}, {axis3_idx}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1:
Found horizontal axis at row 0
Result: horizontal, 0

Example 2:
Found horizontal axis at row 4
Result: horizontal, 4

Example 3:
Found horizontal axis at row 8
Result: horizontal, 8

```
**Correction:** The axis detection code still failed for Example 1. The logic needs refinement. A row/column is an axis if it *only* contains blue (1) and white (0), AND *at least one* blue (1).

Let's fix the `find_axis` function.



*code_execution:*
```python
import numpy as np

def find_axis(grid_list):
    grid = np.array(grid_list, dtype=int)
    height, width = grid.shape
    axis_type = None
    axis_idx = -1

    # Check horizontal
    for r in range(height):
        is_potential_axis = True
        has_blue = False
        for c in range(width):
            pixel = grid[r, c]
            if pixel == 1:
                has_blue = True
            elif pixel != 0: # Any non-blue, non-white pixel disqualifies the row
                is_potential_axis = False
                break
        if is_potential_axis and has_blue:
            axis_type = 'horizontal'
            axis_idx = r
            # print(f"Found horizontal axis at row {r}") # Keep commented for final run
            return axis_type, axis_idx

    # Check vertical only if no horizontal found
    if axis_type is None:
        for c in range(width):
            is_potential_axis = True
            has_blue = False
            for r in range(height):
                 pixel = grid[r, c]
                 if pixel == 1:
                     has_blue = True
                 elif pixel != 0: # Any non-blue, non-white pixel disqualifies the column
                    is_potential_axis = False
                    break
            if is_potential_axis and has_blue:
                axis_type = 'vertical'
                axis_idx = c
                # print(f"Found vertical axis at col {c}") # Keep commented for final run
                return axis_type, axis_idx

    # if axis_type is None: # Keep commented for final run
        # print("No axis found")
    return axis_type, axis_idx

# Example 1 Input
grid1 = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 8, 0, 8, 0], # Has 8, so row 2 is not axis
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 8, 4, 0], # Has 8, 4
    [0, 0, 0, 0, 0, 0, 1, 0, 8, 8, 8, 0], # Has 8
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
]
print("Example 1:")
axis1_type, axis1_idx = find_axis(grid1)
print(f"Result: {axis1_type}, {axis1_idx}")

# Example 2 Input
grid2 = [
    [0, 0, 0, 2, 0, 2, 0, 0, 0],
    [0, 0, 2, 3, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1], # This is the axis
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\nExample 2:")
axis2_type, axis2_idx = find_axis(grid2)
print(f"Result: {axis2_type}, {axis2_idx}")

# Example 3 Input
grid3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # This is the axis
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 6, 6, 5, 0, 0, 0, 0, 0],
    [0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\nExample 3:")
axis3_type, axis3_idx = find_axis(grid3)
print(f"Result: {axis3_type}, {axis3_idx}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1:
Result: horizontal, 0

Example 2:
Result: horizontal, 4

Example 3:
Result: horizontal, 8

```
**Further Correction:** The axis detection logic is *still* incorrect for Example 1. The issue is subtle. My code correctly disqualifies rows/columns with non-zero/non-one colors. However, for Example 1, row 0 *is* `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]`, which fits the criteria `is_potential_axis and has_blue`. The horizontal check runs first and finds this row, incorrectly identifying it as the axis. The *true* axis is the vertical line at column 6.

The definition of the "axis" needs refinement. It's not just *any* line containing blue and white. It's the line that *separates* the objects being reflected. In examples 2 and 3, the horizontal blue line clearly separates the objects above and below. In example 1, the vertical blue line separates objects left and right.

How to distinguish the separating line from other potential lines?
Perhaps the line must span most of the grid dimension (like in Ex 2 & 3) OR be the only line present? In Ex 1, the vertical line spans the full height. The horizontal line candidates (like row 0) only have a single blue pixel.

**Revised Axis Finding Strategy:**
1.  Find all *candidate* horizontal lines (rows with only 0s and 1s, including at least one 1).
2.  Find all *candidate* vertical lines (columns with only 0s and 1s, including at least one 1).
3.  If only one candidate exists (either horizontal or vertical), that's the axis.
4.  If multiple candidates exist, perhaps choose the one that is "most complete" (has the most blue pixels)? Or the one that spans the largest dimension? In Ex 2 & 3, the horizontal line spans the full width. In Ex 1, the vertical line spans the full height. This seems promising.

Let's try implementing the "longest line" heuristic.



*code_execution:*
```python
import numpy as np

def find_axis(grid_list):
    grid = np.array(grid_list, dtype=int)
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
            elif pixel != 0:
                is_potential_axis = False
                break
        if is_potential_axis and blue_count > 0:
            # Heuristic: Prefer lines that are longer / more complete
            if blue_count > max_blue_count:
                 max_blue_count = blue_count
                 best_axis_type = 'horizontal'
                 best_axis_idx = r
            # Optional: Add tie-breaking? E.g. prefer full span lines?
            # elif blue_count == max_blue_count and best_axis_type is None: # First time seeing this count
            #    best_axis_type = 'horizontal'
            #    best_axis_idx = r


    # Check vertical candidates
    # Note: Reset max_blue_count only if switching axis type preference?
    # Let's keep it simple: find the single line with the most blue pixels overall.
    for c in range(width):
        is_potential_axis = True
        blue_count = 0
        for r in range(height):
             pixel = grid[r, c]
             if pixel == 1:
                 blue_count += 1
             elif pixel != 0:
                is_potential_axis = False
                break
        if is_potential_axis and blue_count > 0:
             if blue_count > max_blue_count:
                 max_blue_count = blue_count
                 best_axis_type = 'vertical'
                 best_axis_idx = c
             # Tie-breaking: if equal count, maybe prefer horizontal? Or first found?
             # Current logic prefers vertical if counts are equal and vertical check runs second.
             # Let's explicitly prefer horizontal in ties for now.
             elif blue_count == max_blue_count and best_axis_type == 'vertical':
                 # Keep vertical only if strictly greater
                 pass
             elif blue_count == max_blue_count and best_axis_type is None: # First candidate found
                 best_axis_type = 'vertical'
                 best_axis_idx = c


    # if best_axis_type is None: # Keep commented for final run
        # print("No axis found")
    # else:
        # print(f"Selected axis: {best_axis_type} at {best_axis_idx} with {max_blue_count} blue pixels")

    return best_axis_type, best_axis_idx


# Example 1 Input
grid1 = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 8, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 8, 4, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
]
print("Example 1:")
axis1_type, axis1_idx = find_axis(grid1)
print(f"Result: {axis1_type}, {axis1_idx}") # Expect vertical, 6

# Example 2 Input
grid2 = [
    [0, 0, 0, 2, 0, 2, 0, 0, 0],
    [0, 0, 2, 3, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\nExample 2:")
axis2_type, axis2_idx = find_axis(grid2)
print(f"Result: {axis2_type}, {axis2_idx}") # Expect horizontal, 4

# Example 3 Input
grid3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 6, 6, 5, 0, 0, 0, 0, 0],
    [0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
print("\nExample 3:")
axis3_type, axis3_idx = find_axis(grid3)
print(f"Result: {axis3_type}, {axis3_idx}") # Expect horizontal, 8
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1:
Result: vertical, 6

Example 2:
Result: horizontal, 4

Example 3:
Result: horizontal, 8

```
Success! The axis detection now works for all examples using the "longest line" heuristic.

**YAML Facts:**


```yaml
elements:
  - type: grid
    description: Input and output are 2D grids of colored pixels (0-9).
    properties:
      - height
      - width
  - type: axis_line
    color: blue (1)
    orientation: horizontal or vertical
    composition: Consists of only blue (1) and white (0) pixels, with at least one blue pixel.
    role: separator & axis_of_reflection
    identification: The single candidate line (horizontal or vertical) with the most blue pixels.
    persistence: Remains unchanged between input and output grids.
  - type: object_pixel
    description: A single pixel that is not part of the background (white, 0) or the axis_line (blue, 1).
    properties:
      - color
      - location: (row, column)
actions:
  - name: find_reflection_axis
    input: input_grid
    output: axis_type ('horizontal' or 'vertical'), axis_index (row or column index)
    method: Identify the line (row or column) composed only of blue (1) and white (0) pixels that contains the maximum number of blue pixels.
  - name: initialize_output
    input: input_grid_dimensions
    output: output_grid (filled with white, 0)
  - name: copy_axis_line
    input: input_grid, output_grid, axis_type, axis_index
    process: Copy only the blue (1) pixels from the axis line in the input to the corresponding locations in the output grid.
  - name: reflect_and_swap_pixel
    input: pixel_location (r, c), pixel_color, axis_type, axis_index
    process:
      - If axis is 'horizontal': calculate reflected_row = 2 * axis_index - r, reflected_col = c.
      - If axis is 'vertical': calculate reflected_row = r, reflected_col = 2 * axis_index - c.
      - Determine swapped_color based on predefined pairs (8<>4, 2<>3, 5<>6).
      - Check if reflected location is within grid bounds.
    output: reflected_location (refl_r, refl_c), swapped_color
  - name: place_pixel_on_output
    input: output_grid, reflected_location, swapped_color
    process: Update the pixel at reflected_location in the output_grid with swapped_color.
color_swaps:
  - pair: [azure (8), yellow (4)]
  - pair: [red (2), green (3)]
  - pair: [gray (5), magenta (6)]
relationships:
  - input_pixel maps to reflected_output_pixel
  - distance from axis_line is preserved but mirrored across the axis
  - specific color pairs are mutually swapped during reflection
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filling it with the background color (white, 0).
2.  **Find the Axis of Reflection:**
    a.  Scan each row of the input grid. Identify rows composed *only* of white (0) and blue (1) pixels, containing at least one blue pixel. Count the blue pixels in each such candidate row.
    b.  Scan each column of the input grid. Identify columns composed *only* of white (0) and blue (1) pixels, containing at least one blue pixel. Count the blue pixels in each such candidate column.
    c.  Determine the single candidate line (row or column) with the maximum count of blue pixels. This is the axis of reflection. Record its type ('horizontal' or 'vertical') and its index (row index or column index).
3.  **Copy the Axis:** Iterate through the identified axis line (row or column) in the *input* grid. For every blue pixel (1) found on this axis, copy it to the same location in the *output* grid.
4.  **Reflect and Swap Other Pixels:** Iterate through every pixel (`r`, `c`) in the input grid.
    a.  Get the `original_color` of the pixel.
    b.  If the pixel is background (white, 0) OR if it lies on the identified axis of reflection, skip to the next pixel.
    c.  **Calculate Reflected Position:**
        *   If the axis is 'horizontal' at `axis_index`: `reflected_row = (2 * axis_index) - r`, `reflected_col = c`.
        *   If the axis is 'vertical' at `axis_index`: `reflected_row = r`, `reflected_col = (2 * axis_index) - c`.
    d.  **Determine Swapped Color:** Find the corresponding `swapped_color` for the `original_color` using the predefined pairs: (Azure 8 <-> Yellow 4), (Red 2 <-> Green 3), (Gray 5 <-> Magenta 6). If a color is not in these pairs, it maps to itself (though only these pairs appear in examples).
    e.  **Place on Output:** Check if the calculated `reflected_row` and `reflected_col` are within the bounds of the grid. If they are, set the pixel at (`reflected_row`, `reflected_col`) in the *output* grid to the `swapped_color`.
5.  Return the completed output grid.
