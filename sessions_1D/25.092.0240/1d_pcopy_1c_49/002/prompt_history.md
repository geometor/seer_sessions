
## train_1

**input:**
```
0 8 8 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 6 6 6 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 8 8 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 8 8 0 8 8 8 0 0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of the Elements:**

1.  **Grid Structure:** The input and output grids appear to be one-dimensional arrays or single rows. All examples show a 1x32 grid.
2.  **Colors:** The primary colors involved are white (0) and one other non-white color per example (azure '8' or magenta '6').
3.  **Input Pattern:** Each input starts with a white pixel (0) followed by a three-pixel sequence of a non-white color (e.g., `8 8 8` or `6 6 6`). This sequence appears to act as a template. Further along the row, there are one or more isolated single pixels of the *same* non-white color as the template. These isolated pixels are surrounded by white pixels.
4.  **Transformation:** The core transformation seems to involve the isolated single non-white pixels. Each of these isolated pixels in the input is replaced in the output by a copy of the initial three-pixel template pattern. The replacement is centered on the original position of the isolated pixel.
5.  **Preservation:** The initial template pattern at the beginning of the row (indices 1, 2, 3) remains unchanged in the output. The white pixels (0) that are not part of the replacement also remain unchanged.

**Facts:**


```yaml
task_type: pattern_replacement
grid_dimensionality: 1D # or 1xN 2D grid

elements:
  - element: background
    color: white (0)
    role: fills most of the grid

  - element: template_pattern
    description: A sequence of three identical non-white pixels found near the start of the input grid.
    properties:
      - location: fixed, starts at index 1 (columns 1, 2, 3)
      - size: 3 pixels wide
      - color: consistent within the pattern (e.g., all azure '8' or all magenta '6')
      - count: 1 per input grid
    role: defines the pattern to be copied

  - element: target_pixel
    description: Isolated single pixels matching the color of the template_pattern.
    properties:
      - location: variable, occurs after the template_pattern
      - size: 1 pixel
      - color: same as template_pattern
      - context: must be surrounded by background pixels (white '0') horizontally.
      - count: one or more per input grid
    role: marks locations for pattern insertion

actions:
  - action: identify_template
    input: input_grid
    output: template_pattern (value and color)
    condition: located at indices [1, 2, 3]

  - action: identify_targets
    input: input_grid
    output: list of target_pixel locations (indices)
    condition: pixels match template_pattern color and are isolated (index > 3, input[index-1]==0, input[index+1]==0)

  - action: copy_paste_pattern
    source: template_pattern
    destination_grid: output_grid (initially a copy of input_grid)
    targets: identified target_pixel locations
    process: For each target location `i`, overwrite the output grid at indices `[i-1, i, i+1]` with the `template_pattern`.
    centering: The middle pixel of the copied pattern aligns with the original target_pixel location.

relationships:
  - relationship: color_match
    between: [template_pattern, target_pixel]
    details: The color of the target_pixels must be the same as the color of the pixels in the template_pattern.
  - relationship: positional
    between: [template_pattern, target_pixel]
    details: Target pixels always appear later in the grid than the template pattern.
  - relationship: isolation
    element: target_pixel
    details: Target pixels are horizontally adjacent only to background pixels.

output_construction:
  - step: Initialize the output grid as a copy of the input grid.
  - step: Identify the template pattern (color C, pattern CCC) at indices 1, 2, 3.
  - step: Find all indices `i` where the input grid has value C, and input[i-1] and input[i+1] are 0.
  - step: For each such index `i`, modify the output grid by setting output[i-1]=C, output[i]=C, output[i+1]=C.
```


**Natural Language Program:**

1.  Start with the input grid. Create a copy of the input grid to serve as the basis for the output grid.
2.  Identify the "template pattern": Look at the pixels at indices 1, 2, and 3 in the input grid. This three-pixel sequence is the template pattern. Note its color (let's call it C).
3.  Scan the input grid starting from index 4 to find all "target pixels". A target pixel is a pixel that meets two conditions:
    a.  Its color is C (the same color as the template pattern).
    b.  Its immediate horizontal neighbors (at index - 1 and index + 1) are both white (0).
4.  For each identified target pixel located at index `i`:
    a.  Modify the output grid (which started as a copy of the input).
    b.  Replace the pixel at index `i` in the output grid with color C.
    c.  Replace the pixel at index `i-1` in the output grid with color C.
    d.  Replace the pixel at index `i+1` in the output grid with color C.
    (Essentially, copy the template pattern `C C C` into the output grid, centered at index `i`).
5.  The final modified grid is the result.
```python
import copy

# COLOR_MAP = {
#     0: (238, 238, 238),  # white
#     1: (30, 147, 255),  # blue
#     2: (220, 50, 40),  # red
#     3: (79, 204, 48),  # green
#     4: (230, 200, 0),  # yellow
#     5: (85, 85, 85),  # gray
#     6: (229, 58, 163),  # magenta
#     7: (230, 120, 20),  # orange
#     8: (135, 216, 241),  # azure
#     9: (146, 18, 49),  # maroon
# }

def transform(input_grid):
    """
    Transforms the input grid based on a pattern replacement rule.
    1. Identifies a 3-pixel template pattern (e.g., C C C) starting at index 1
       in the input row. The color C is noted.
    2. Scans the rest of the input row (from index 4 onwards) for 'target' pixels.
    3. A target pixel is a pixel with color C that is surrounded by the
       background color (white, 0) on both its left and right sides.
    4. For each target pixel found at index 'i', the output grid (initially a
       copy of the input) is modified by replacing the pixels at indices
       i-1, i, and i+1 with the template color C.
    5. The initial template pattern at indices 1, 2, 3 remains unchanged.
    """

    # Ensure input is a list of lists and extract the first row
    # ARC grids are typically 2D, even if 1xN
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Handle unexpected input format if necessary, or raise error
        # For now, assume it's the expected format [[...]]
        return [] # Or raise ValueError("Invalid input grid format")

    input_row = input_grid[0]
    grid_width = len(input_row)

    # Initialize output_grid as a copy of the input_grid
    # Using copy.deepcopy to handle the list of lists structure properly
    output_grid = copy.deepcopy(input_grid)
    # Get a reference to the row we will modify
    output_row = output_grid[0]

    # Check if grid is wide enough for the template and potential targets
    if grid_width < 5: # Need at least index 1,2,3 for template and index 4 to check neighbors
        return output_grid # Return unchanged grid if too small

    # Identify the template color from index 1
    # We assume the pattern C C C exists at indices 1, 2, 3 based on examples
    template_color = input_row[1]
    background_color = 0 # White

    # Iterate through the grid to find target pixels
    # Start scan from index 4 (after the template)
    # End scan at grid_width - 2 to safely access index i+1
    for i in range(4, grid_width - 1):
        # Check if the current pixel is a target pixel
        current_pixel_color = input_row[i]
        left_neighbor_color = input_row[i-1]
        right_neighbor_color = input_row[i+1]

        is_target = (current_pixel_color == template_color and
                     left_neighbor_color == background_color and
                     right_neighbor_color == background_color)

        if is_target:
            # Apply the transformation: replace the segment [i-1, i, i+1]
            # in the output row with the template color
            output_row[i-1] = template_color
            output_row[i]   = template_color
            output_row[i+1] = template_color

    return output_grid
```
