
## train_1

**input:**
```
0 0 0 4 4 4 4 4 4 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 4 4 4 4 4 4 0
```


## train_2

**input:**
```
7 7 7 7 7 7 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 9 0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 2 2 2 2 2 2 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 2 2 2 2 2 2 0 0 0
```

Okay, let's analyze the task examples.

**Perception of Task Elements:**

1.  **Grid Structure:** The input and output are both 1-dimensional grids (or single rows).
2.  **Key Pixels:** Each grid contains three types of pixels:
    *   Background pixels: Represented by white (0).
    *   A single pivot pixel: Represented by maroon (9). Its position remains unchanged between input and output.
    *   A line object: A contiguous sequence of pixels of a single color (yellow, orange, or red in the examples), distinct from white and maroon.
3.  **Transformation:** The core transformation involves the line object. Its position changes relative to the pivot pixel. Comparing the input and output, the line object appears to be reflected or mirrored across the position of the maroon pivot pixel. The color and length of the line object remain the same.

**YAML Fact Documentation:**


```yaml
task_context:
  grid_dimensionality: 1D
  background_color: white (0)
objects:
  - object_type: pivot
    identifier: maroon_pixel
    properties:
      color: maroon (9)
      count: 1
      position: fixed (remains same in output)
    role: center_of_transformation
  - object_type: line
    identifier: colored_line
    properties:
      color: variable (non-white, non-maroon)
      count: 1
      shape: contiguous_horizontal_segment
      length: variable
      position: variable
    role: object_being_transformed
transformation:
  action: reflection
  actor: colored_line
  reference_point: position of maroon_pixel
  details: Each pixel of the colored_line is moved to a new position such that its distance and direction from the maroon_pixel are reversed.
constraints:
  - The maroon_pixel's position does not change.
  - The colored_line's color and length do not change.
  - The colored_line does not overlap the maroon_pixel in input or output.
```


**Natural Language Program:**

1.  Create the output grid with the same dimensions as the input grid, initially filled with the background color (white, 0).
2.  Locate the index (position) of the single maroon pixel (9) in the input grid. Place a maroon pixel at the *same* index in the output grid. Let this index be `maroon_index`.
3.  Identify the contiguous sequence of non-white, non-maroon pixels in the input grid. Note their color (`line_color`) and their indices.
4.  For each pixel belonging to this colored line at index `i` in the input grid:
    a.  Calculate the pixel's displacement relative to the maroon pixel: `displacement = i - maroon_index`.
    b.  Calculate the new index for this pixel in the output grid by reflecting the displacement: `new_index = maroon_index - displacement`. (Alternatively: `new_index = 2 * maroon_index - i`).
    c.  Place a pixel of `line_color` at `new_index` in the output grid.
5.  Return the completed output grid.
```python
"""
Reflect a colored line object across a stationary maroon pivot pixel in a 1D grid.

The input is a 1D grid (represented as a list of integers) containing:
- Background pixels (white, 0).
- A single pivot pixel (maroon, 9).
- A contiguous line object of a single color (non-white, non-maroon).

The transformation performs the following steps:
1. Initialize an output grid of the same size as the input, filled with the background color (0).
2. Locate the index of the maroon pivot pixel (9) in the input grid.
3. Place the maroon pixel at the same index in the output grid.
4. Identify the contiguous sequence of non-white, non-maroon pixels (the line object) in the input grid, noting their color and indices.
5. For each pixel of the line object at index 'i' in the input:
   a. Calculate its displacement relative to the maroon pixel's index ('maroon_index'): displacement = i - maroon_index.
   b. Calculate the new index for this pixel in the output grid by reflecting the displacement: new_index = maroon_index - displacement.
   c. Place a pixel of the line object's color at 'new_index' in the output grid.
6. Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Reflects a colored line object across a maroon pivot pixel in a 1D grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Convert input list to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    grid_size = len(input_array)
    
    # Define known colors/pixel values
    background_color = 0
    pivot_color = 9

    # Initialize output grid with the background color
    output_array = np.full(grid_size, background_color, dtype=int)

    # --- Find Pivot ---
    # Locate the index of the single maroon pivot pixel (9)
    # Assumes exactly one pivot pixel exists based on examples
    try:
        maroon_index = np.where(input_array == pivot_color)[0][0]
    except IndexError:
        # Handle case where pivot is missing, though not expected from examples
        # For now, just return the background grid or raise an error
        # print("Error: Pivot pixel (9) not found.")
        return output_array.tolist() # Or raise ValueError("Pivot pixel not found")

    # Place the pivot pixel in the output grid at the same location
    output_array[maroon_index] = pivot_color

    # --- Find Line Object ---
    line_indices = []
    line_color = -1 # Initialize with an invalid color

    # Iterate through the input grid to find the line object's pixels and color
    for i, pixel_value in enumerate(input_array):
        # Check if the pixel is part of the line (not background and not pivot)
        if pixel_value != background_color and pixel_value != pivot_color:
            line_indices.append(i)
            # Capture the color of the line from the first line pixel found
            if line_color == -1:
                line_color = pixel_value

    # --- Perform Reflection ---
    # If a line object was found (i.e., line_color is valid)
    if line_color != -1:
        # Iterate through each pixel index of the found line object
        for i in line_indices:
            # Calculate the pixel's displacement relative to the pivot
            displacement = i - maroon_index
            
            # Calculate the new index by reflecting the displacement across the pivot
            # new_index = maroon_index - (i - maroon_index) = 2 * maroon_index - i
            new_index = maroon_index - displacement 
            
            # Place the line pixel at the new reflected index in the output grid
            # Check bounds to prevent errors, although not needed for provided examples
            if 0 <= new_index < grid_size:
                output_array[new_index] = line_color
            # else:
                # Handle cases where reflection goes out of bounds if necessary
                # print(f"Warning: Reflected index {new_index} for pixel at {i} is out of bounds.")

    # Convert the numpy array back to a list before returning
    return output_array.tolist()
```
