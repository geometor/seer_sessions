
## train_1

**input:**
```
0 7 7 7 0 0 0 7 0 0 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 0 0 7 7 7 0 0 7 7 7 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 6 6 0 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 0 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 9 9 9 0 0 9 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

*   **Input/Output Format:** The examples show input and output data represented as flat lists of integers (0-9), corresponding to colors. Although presented linearly, they likely represent a 1D structure or are treated as such for the transformation. The length of the input and output arrays is the same (33 in these examples).
*   **Colors:** Each input contains predominantly white pixels (0) and pixels of exactly one other color (7-orange, 6-magenta, 9-maroon). Let's call this the "active color". The output also contains only white and the active color.
*   **Transformation:** The core transformation seems to involve changing some white pixels (0) into the active color. The pixels that were originally the active color remain unchanged.
*   **Pattern:** The change appears localized. Comparing input and output, white pixels adjacent to *isolated* active color pixels are changed to the active color. An active color pixel seems "isolated" if its immediate left and right neighbors are both white. Existing contiguous segments of the active color are not modified.

**YAML Facts:**


```yaml
Grid_Properties:
  dimensionality: 1D (treated as a sequence)
  background_color: 0 (white)

Objects:
  - type: Pixel
    properties:
      - color: Integer (0-9)
      - position: index in the 1D sequence
  - type: Active_Pixel
    description: A pixel whose color is the single non-white color in the input.
  - type: Isolated_Active_Pixel
    description: An Active_Pixel whose immediate left and right neighbors in the sequence are white (0). Boundary conditions apply (a pixel at the start/end only needs its single neighbor to be white).
  - type: Active_Color_Segment
    description: A contiguous sequence of one or more Active_Pixels.

Relationships:
  - type: Adjacency
    object_types: [Pixel, Pixel]
    description: Pixels at index i and i+1 (or i-1) are adjacent.
  - type: Isolation
    object_types: [Active_Pixel, Pixel, Pixel]
    description: An Active_Pixel is isolated if its adjacent neighbors (if they exist) are white (0).

Actions:
  - name: Identify_Active_Color
    description: Find the unique non-zero color value in the input sequence.
  - name: Identify_Isolated_Pixels
    input: Input sequence, Active Color
    output: List of indices of Isolated_Active_Pixels.
  - name: Color_Neighbors
    input: Output sequence, Index of Isolated_Active_Pixel, Active Color
    description: Change the color of the white neighbors (at index-1 and index+1, if they exist and are white) of the isolated pixel to the Active Color in the output sequence.

Transformation_Rule:
  - For every Isolated_Active_Pixel in the input sequence, perform the Color_Neighbors action on the corresponding output sequence. Pixels that are not neighbors of isolated active pixels retain their original color.
```


**Natural Language Program:**

1.  **Identify Active Color:** Determine the single non-zero color value present in the input sequence. Call this `active_color`. If no non-zero color exists, return the input sequence unchanged.
2.  **Initialize Output:** Create a copy of the input sequence to serve as the initial output sequence.
3.  **Iterate and Check Isolation:** Go through each pixel in the input sequence at index `i`.
4.  **Check if Pixel is Active:** If the pixel `input[i]` is equal to `active_color`:
    *   **Check Neighbors:** Determine if the pixel is isolated. Check the color of the left neighbor (`input[i-1]`) and the right neighbor (`input[i+1]`).
        *   A pixel at index `i` is considered isolated if:
            *   It has a left neighbor (`i > 0`) which is white (`input[i-1] == 0`), OR it's the first pixel (`i == 0`).
            *   AND
            *   It has a right neighbor (`i < length - 1`) which is white (`input[i+1] == 0`), OR it's the last pixel (`i == length - 1`).
5.  **Apply Color Change:** If the pixel `input[i]` is identified as an isolated active pixel:
    *   If it has a left neighbor (`i > 0`) and that neighbor is white (`input[i-1] == 0`), change the color of the pixel at index `i-1` in the *output* sequence to `active_color`.
    *   If it has a right neighbor (`i < length - 1`) and that neighbor is white (`input[i+1] == 0`), change the color of the pixel at index `i+1` in the *output* sequence to `active_color`.
6.  **Return Output:** After checking all pixels in the input sequence, return the final modified output sequence.
```python
import copy

"""
Transforms a 1D sequence of colors based on the following rule:
1. Identify the single non-white (non-zero) color present in the input sequence ('active_color').
2. Initialize the output sequence as a copy of the input sequence.
3. Iterate through the input sequence. For each pixel that matches the 'active_color':
    a. Check if this pixel is 'isolated', meaning its immediate left neighbor (if it exists) is white (0) AND its immediate right neighbor (if it exists) is white (0). Boundary pixels only need their single neighbor to be white.
    b. If the pixel is isolated:
        i. If its left neighbor exists and is white in the original input, change the color of the left neighbor in the output sequence to 'active_color'.
        ii. If its right neighbor exists and is white in the original input, change the color of the right neighbor in the output sequence to 'active_color'.
4. Return the modified output sequence. If no active_color is found, return the original input.
"""

def find_active_color(input_sequence):
    """Finds the unique non-zero color in the sequence."""
    active_color = 0
    for pixel in input_sequence:
        if pixel != 0:
            active_color = pixel
            break # Assume only one active color as per examples
    return active_color

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Find the active color
    active_color = find_active_color(input_sequence)
    if active_color == 0:
        # No transformation needed if no active color
        return copy.deepcopy(input_sequence)

    # Initialize output_sequence as a copy of the input
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through the input sequence to find isolated active pixels
    for i in range(n):
        # Check if the current pixel has the active color
        if input_sequence[i] == active_color:
            # Determine if the left side is isolated (white neighbor or boundary)
            is_left_isolated = (i == 0) or (input_sequence[i-1] == 0)

            # Determine if the right side is isolated (white neighbor or boundary)
            is_right_isolated = (i == n - 1) or (input_sequence[i+1] == 0)

            # If the pixel is isolated (both sides are white or boundary)
            if is_left_isolated and is_right_isolated:
                # Color the left neighbor in the output if it exists and was white
                if i > 0 and input_sequence[i-1] == 0:
                    output_sequence[i-1] = active_color
                # Color the right neighbor in the output if it exists and was white
                if i < n - 1 and input_sequence[i+1] == 0:
                    output_sequence[i+1] = active_color

    # Return the modified output sequence
    return output_sequence
```
```python
import numpy as np
import copy

"""
Transforms a 2D grid based on the following rule:
1. Identify the single non-white (non-zero) color present in the input grid ('active_color'). If none exists, return the input grid unchanged.
2. Create a copy of the input grid to serve as the output grid.
3. Iterate through each pixel of the *input* grid.
4. If a pixel contains the 'active_color':
    a. Check its immediate horizontal neighbor to the left. If this neighbor exists (is within grid bounds) and is white (0) in the *input* grid, mark this neighbor's coordinates for coloring.
    b. Check its immediate horizontal neighbor to the right. If this neighbor exists (is within grid bounds) and is white (0) in the *input* grid, mark this neighbor's coordinates for coloring.
5. After checking all active pixels, change the color of all marked white neighbors in the *output* grid to the 'active_color'.
6. Return the modified output grid.
"""

def find_active_color(grid):
    """
    Finds the unique non-zero color in the grid.
    Returns the color value or 0 if none is found or multiple are found (though examples suggest only one).
    """
    unique_colors = np.unique(grid)
    active_color = 0
    non_zero_count = 0
    for color in unique_colors:
        if color != 0:
            active_color = color
            non_zero_count += 1

    # Based on examples, we expect exactly one active color.
    # If there's none or more than one, the rule might not apply as expected.
    # Returning 0 handles the 'all white' case gracefully.
    if non_zero_count != 1:
         # Check if grid is all zeros
        if np.all(grid == 0):
            return 0 # No active color
        else:
            # If there are non-zero colors but not exactly one,
            # return the first one found based on example structure,
            # but acknowledge this might be an edge case.
            for color in unique_colors:
                 if color != 0:
                     return color # Return first non-zero found
            return 0 # Should not happen if unique_colors had non-zeros

    return active_color

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Find the active color
    active_color = find_active_color(input_grid)

    # If no active color (grid is all white or assumption violated), return copy
    if active_color == 0:
        return copy.deepcopy(input_grid)

    # Get grid dimensions
    rows, cols = input_grid.shape

    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Use a set to store coordinates of white neighbors to color (avoids duplicates)
    pixels_to_color = set()

    # Iterate through the input grid to find active pixels and identify neighbors
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel has the active color
            if input_grid[r, c] == active_color:
                # Check left neighbor
                if c > 0 and input_grid[r, c - 1] == 0:
                    pixels_to_color.add((r, c - 1))

                # Check right neighbor
                if c < cols - 1 and input_grid[r, c + 1] == 0:
                    pixels_to_color.add((r, c + 1))

    # Apply the color changes to the output grid
    for r_change, c_change in pixels_to_color:
        output_grid[r_change, c_change] = active_color

    return output_grid
```
