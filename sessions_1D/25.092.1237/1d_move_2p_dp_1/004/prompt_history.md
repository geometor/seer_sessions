
## train_1

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 2 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Task Elements:**

The input and output are presented as 1D arrays or single-row grids. Each example features:
1.  A single red pixel (color 2).
2.  A contiguous block of pixels of a single color other than white (0) or red (2). This "colored block" varies in color (gray, blue, orange) and length across examples.
3.  White pixels (color 0) surrounding these elements.
4.  Crucially, in every input example, the colored block is positioned to the left of the red pixel, separated by exactly two white pixels.

The transformation involves rearranging these elements. Specifically, the colored block moves rightwards, closing the gap with the red pixel. The two white pixels that were originally between the colored block and the red pixel are repositioned to the immediate left of the colored block. The positions of all other white pixels (leading and trailing) and the red pixel remain unchanged relative to the start and end of the array, respectively. The core operation appears to be a positional swap between the colored block and the two adjacent white pixels to its right.

**Facts:**


```yaml
Task: Move a colored block to be adjacent to a target pixel.

Input_Features:
  - Grid: Represented as a 1D array.
  - Objects:
    - Red_Pixel:
        Color: 2
        Count: 1
        Role: Target_Marker
    - Colored_Block:
        Color: Any color except 0 (white) and 2 (red)
        Property: Contiguous sequence of pixels of the same color.
        Position: Located to the left of the Red_Pixel.
        Count: 1
    - White_Separator_Pixels:
        Color: 0
        Count: 2
        Position: Located immediately between the right end of the Colored_Block and the Red_Pixel.
    - Background_Pixels:
        Color: 0
        Position: Elsewhere in the array (leading/trailing).

Relationships:
  - Spatial: `[Leading_Background..., Colored_Block, White_Separator_Pixel_1, White_Separator_Pixel_2, Red_Pixel, Trailing_Background...]`

Transformation:
  - Action: Rearrangement of segments.
  - Rule: Swap the position of the `Colored_Block` segment and the `White_Separator_Pixels` segment.

Output_Features:
  - Grid: Rearranged 1D array.
  - Structure: `[Leading_Background..., White_Separator_Pixel_1, White_Separator_Pixel_2, Colored_Block, Red_Pixel, Trailing_Background...]`
  - Invariant:
    - The Red_Pixel maintains its position relative to the trailing background pixels.
    - The leading background pixels maintain their position relative to the start.
    - The content (colors and counts) of all segments remains the same, only their order changes.
```


**Natural Language Program:**

1.  Identify the index of the single red pixel (value 2) in the input array.
2.  Identify the indices of the two white pixels (value 0) located immediately to the left of the red pixel. Let these be `white_sep_indices`.
3.  Starting from the pixel immediately to the left of the white separator pixels, search leftwards to find the start and end indices of the contiguous block of non-white pixels. This is the `colored_block`. Let its indices be `block_indices`.
4.  Identify the segment of the array *before* the `colored_block`. Let this be `leading_segment`.
5.  Identify the segment of the array *after* the red pixel. Let this be `trailing_segment`.
6.  Construct the output array by concatenating the segments in the following order:
    a.  `leading_segment`
    b.  The two white pixels from `white_sep_indices`.
    c.  The `colored_block` identified by `block_indices`.
    d.  The red pixel.
    e.  `trailing_segment`.
7.  Return the newly constructed array.
```python
import numpy as np
from typing import List, Tuple

"""
Transformation Rule:
Identify the single red pixel (2). Identify the contiguous block of non-white, non-red pixels located to the left of the red pixel, separated by exactly two white pixels (0). Swap the positions of this colored block and the two white separator pixels. All other pixels remain in their relative positions.
"""

def find_pixel_index(grid: List[int], color: int) -> int:
    """Finds the index of the first pixel with the specified color."""
    try:
        return grid.index(color)
    except ValueError:
        return -1 # Indicate not found

def find_colored_block_indices(grid: List[int], search_end_index: int) -> Tuple[int, int]:
    """
    Finds the start and end indices of a contiguous block of non-white pixels
    ending immediately before search_end_index.
    Assumes the block exists and is preceded by a white pixel or the start of the grid.
    """
    if search_end_index <= 0:
        return -1, -1 # Cannot have a block ending before index 0

    block_end_index = search_end_index - 1
    block_color = grid[block_end_index]

    # Should not be white or red based on problem description
    if block_color == 0 or block_color == 2:
         return -1, -1 # Unexpected color

    block_start_index = block_end_index
    while block_start_index > 0 and grid[block_start_index - 1] == block_color:
        block_start_index -= 1

    return block_start_index, block_end_index

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (represented as a 1D list).

    1. Finds the red pixel (2).
    2. Identifies the two white pixels (0) immediately to its left.
    3. Identifies the contiguous colored block immediately to the left of the white pixels.
    4. Reconstructs the grid by swapping the colored block and the two white pixels.
    """

    # Find the index of the red pixel (target marker)
    red_index = find_pixel_index(input_grid, 2)
    if red_index == -1:
        # Handle cases where the red pixel isn't found (though not expected based on examples)
        print("Warning: Red pixel not found.")
        return input_grid # Or raise an error

    # Verify the two white separator pixels exist to the left
    if red_index < 2 or input_grid[red_index - 1] != 0 or input_grid[red_index - 2] != 0:
        # Handle cases where the expected white separators aren't present
        print("Warning: Expected white separator pixels not found.")
        return input_grid # Or raise an error

    white_sep_start_index = red_index - 2
    white_separator_segment = input_grid[white_sep_start_index:red_index] # Should be [0, 0]

    # Find the indices of the colored block
    block_start_index, block_end_index = find_colored_block_indices(input_grid, white_sep_start_index)

    if block_start_index == -1:
         # Handle cases where the colored block isn't found correctly
        print("Warning: Colored block not found or invalid.")
        return input_grid # Or raise an error

    # Extract the segments
    leading_segment = input_grid[:block_start_index]
    colored_block_segment = input_grid[block_start_index : block_end_index + 1]
    red_pixel_segment = [input_grid[red_index]] # Just [2]
    trailing_segment = input_grid[red_index + 1 :]

    # Construct the output grid by rearranging the segments
    output_grid = (
        leading_segment +
        white_separator_segment +
        colored_block_segment +
        red_pixel_segment +
        trailing_segment
    )

    return output_grid
```
```python
import numpy as np
from typing import Tuple

"""
Transformation Rule:
Identify the single red pixel (2) in the 1D NumPy input array. 
Identify the contiguous block of non-white (0), non-red (2) pixels located immediately to the left of two white (0) separator pixels, which are themselves immediately to the left of the red pixel. 
Swap the positions of this colored block segment and the two white separator pixels segment. 
All other pixels (leading background, red pixel, trailing background) remain in their relative positions.
"""

def find_red_pixel_np(grid: np.ndarray) -> int:
    """Finds the index of the single red pixel (2) in a 1D NumPy array."""
    indices = np.where(grid == 2)[0]
    if len(indices) == 1:
        return indices[0]
    elif len(indices) == 0:
        # Handle case where red pixel is not found (error or return default)
        raise ValueError("Red pixel (2) not found in the input grid.")
    else:
        # Handle case where multiple red pixels are found (error or choose first)
        raise ValueError("Multiple red pixels (2) found in the input grid.")

def find_colored_block_indices_np(grid: np.ndarray, search_end_index: int) -> Tuple[int, int]:
    """
    Finds the start and end indices of a contiguous block of non-white, non-red pixels
    ending immediately before search_end_index in a 1D NumPy array.
    """
    if search_end_index <= 0:
        raise ValueError(f"Cannot find block ending before index 0 (search_end_index={search_end_index}).")

    block_end_index = search_end_index - 1
    if block_end_index < 0:
         raise ValueError(f"Block end index is invalid ({block_end_index}).")

    block_color = grid[block_end_index]

    # Check if the color is valid for a 'colored block'
    if block_color == 0 or block_color == 2:
         raise ValueError(f"Pixel at index {block_end_index} is white (0) or red (2), expected a colored block.")

    block_start_index = block_end_index
    # Iterate leftwards to find where the block starts
    while block_start_index > 0 and grid[block_start_index - 1] == block_color:
        block_start_index -= 1

    # Check if the pixel before the block start is white or if it's the beginning of the array
    if block_start_index > 0 and grid[block_start_index - 1] != 0:
         # This check might be too strict depending on variations, but aligns with examples
         # print(f"Warning: Pixel before block start (index {block_start_index - 1}) is not white (0).")
         pass # Relaxing this constraint for now, as the core logic is the swap

    return block_start_index, block_end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    1. Finds the red pixel (2).
    2. Verifies the two white separator pixels (0) immediately to its left.
    3. Identifies the contiguous colored block immediately to the left of the white pixels.
    4. Reconstructs the grid by swapping the colored block and the two white pixels using NumPy concatenation.
    """
    if not isinstance(input_grid, np.ndarray):
         input_grid = np.array(input_grid) # Ensure input is a NumPy array

    if input_grid.ndim != 1:
         raise ValueError("Input grid must be 1-dimensional.")

    # 1. Find the index of the red pixel (target marker)
    try:
        red_index = find_red_pixel_np(input_grid)
    except ValueError as e:
        print(f"Error finding red pixel: {e}")
        return input_grid # Return original grid if prerequisite not met

    # 2. Verify the two white separator pixels exist to the left
    if red_index < 2:
        print(f"Error: Red pixel at index {red_index} is too close to the start for separators.")
        return input_grid
    if not (input_grid[red_index - 1] == 0 and input_grid[red_index - 2] == 0):
        print(f"Error: Expected white separator pixels (0, 0) at indices {red_index - 2}, {red_index - 1}, but found ({input_grid[red_index - 2]}, {input_grid[red_index - 1]}).")
        return input_grid # Return original grid if prerequisite not met

    white_sep_start_index = red_index - 2

    # 3. Find the indices of the colored block
    try:
        block_start_index, block_end_index = find_colored_block_indices_np(input_grid, white_sep_start_index)
    except ValueError as e:
        print(f"Error finding colored block: {e}")
        return input_grid # Return original grid if prerequisite not met

    # 4. Extract the segments using NumPy slicing
    leading_segment = input_grid[:block_start_index]
    colored_block_segment = input_grid[block_start_index : block_end_index + 1]
    white_separator_segment = input_grid[white_sep_start_index : red_index] # Indices red_index-2, red_index-1
    red_pixel_segment = input_grid[red_index : red_index + 1] # Just the red pixel at red_index
    trailing_segment = input_grid[red_index + 1 :]

    # 5. Construct the output grid by concatenating segments in the new order
    output_grid = np.concatenate([
        leading_segment,
        white_separator_segment,
        colored_block_segment,
        red_pixel_segment,
        trailing_segment
    ])

    return output_grid
```
