
## train_1

**input:**
```
1 4 1 1 1 1 1 1 1 4 1
4 4 1 1 1 1 1 1 1 4 4
1 1 1 1 1 1 1 8 8 1 1
1 1 3 1 1 1 1 1 8 1 1
1 1 3 1 1 1 1 1 8 1 1
1 1 1 1 1 1 1 8 8 1 1
4 4 1 1 1 1 1 1 1 4 4
1 4 1 1 1 1 1 1 1 4 1
1 4 1 1 1 1 1 1 1 4 1
4 4 1 1 1 1 1 1 1 4 4
1 1 1 1 1 1 8 8 8 1 1
1 1 3 3 1 1 1 1 8 1 1
1 1 3 3 1 1 1 1 8 1 1
1 1 1 1 1 1 8 8 8 1 1
4 4 1 1 1 1 1 1 1 4 4
1 4 1 1 1 1 1 1 1 4 1
1 4 1 1 1 1 1 1 1 4 1
4 4 1 1 1 1 1 1 1 4 4
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
4 4 1 1 1 1 1 1 1 4 4
1 4 1 1 1 1 1 1 1 4 1
```


**output:**
```
1 4 1 1 1 1 1 1 1 4 1
4 4 1 1 1 1 1 1 1 4 4
1 1 1 1 1 8 8 8 8 1 1
1 1 3 3 3 1 1 1 8 1 1
1 1 3 3 3 1 1 1 8 1 1
1 1 1 1 1 8 8 8 8 1 1
4 4 1 1 1 1 1 1 1 4 4
1 4 1 1 1 1 1 1 1 4 1
```


## train_2

**input:**
```
8 2 2 2 2 2 2 2 2 2 8
2 8 8 2 8 8 8 2 8 8 2
2 8 1 1 4 2 2 2 2 8 2
2 2 4 4 4 2 2 2 2 2 2
2 8 1 1 4 2 2 2 2 8 2
2 8 8 2 8 8 8 2 8 8 2
8 2 2 2 2 2 2 2 2 2 8
8 2 2 2 2 2 2 2 2 2 8
2 8 8 2 8 8 8 2 8 8 2
2 8 1 1 1 4 2 2 2 8 2
2 2 4 4 4 4 2 2 2 2 2
2 8 1 1 1 4 2 2 2 8 2
2 8 8 2 8 8 8 2 8 8 2
8 2 2 2 2 2 2 2 2 2 8
8 2 2 2 2 2 2 2 2 2 8
2 8 8 2 8 8 8 2 8 8 2
2 8 2 2 2 2 2 2 2 8 2
2 2 2 2 2 2 2 2 2 2 2
2 8 2 2 2 2 2 2 2 8 2
2 8 8 2 8 8 8 2 8 8 2
8 2 2 2 2 2 2 2 2 2 8
```


**output:**
```
8 2 2 2 2 2 2 2 2 2 8
2 8 8 2 8 8 8 2 8 8 2
2 8 1 1 1 1 4 2 2 8 2
2 2 4 4 4 4 4 2 2 2 2
2 8 1 1 1 1 4 2 2 8 2
2 8 8 2 8 8 8 2 8 8 2
8 2 2 2 2 2 2 2 2 2 8
```

Okay, let's analyze the task based on the provided examples.

**Perception:**

The task involves extracting a specific horizontal subgrid (a slice) from a larger input grid. The input grids appear to be composed of vertically stacked repeating or related patterns/blocks. The height of the output grid dictates the height of these blocks or slices within the input grid. The core challenge is identifying *which* slice from the input becomes the output.

Observing the two examples:

1.  **Example 1:** Input is 24x11, output is 8x11. The input can be seen as three 8x11 slices stacked vertically. The output corresponds to the middle slice (rows 8-15).
2.  **Example 2:** Input is 21x11, output is 7x11. The input can be seen as three 7x11 slices stacked vertically. The output corresponds to the middle slice (rows 7-13).

It seems we need a criterion to select the correct slice. Let's analyze the content of the slices:

*   In Example 1, the slices contain colors {white(1), yellow(4), green(3), azure(8)}, {white(1), yellow(4), green(3), azure(8)}, and {white(1), yellow(4)} respectively. The colors common to all slices are white(1) and yellow(4), likely acting as background or frame. The "content" colors are green(3) and azure(8). Slice 1 has 7 content pixels, Slice 2 has 11, and Slice 3 has 0. The output (Slice 2) has the maximum number of content pixels.
*   In Example 2, the slices contain colors {red(2), azure(8), blue(1), yellow(4)}, {red(2), azure(8), blue(1), yellow(4)}, and {red(2), azure(8)} respectively. The colors common to all slices are red(2) and azure(8). The "content" colors are blue(1) and yellow(4). Slice 1 has 6 content pixels, Slice 2 has 8, and Slice 3 has 0. The output (Slice 2) has the maximum number of content pixels.

This suggests a rule based on maximizing the count of non-background/non-frame pixels within a slice.

**Facts:**


```yaml
Task: Extract a specific horizontal slice from the input grid.

Input_Grid:
  - Properties:
      - Height: H_in
      - Width: W_in
      - Pixels: Array of colors (0-9)
  - Structure: Composed of vertically stacked slices.

Output_Grid:
  - Properties:
      - Height: H_out
      - Width: W_out (W_out == W_in)
      - Pixels: Array of colors (0-9)
  - Relationship_to_Input: Is one of the horizontal slices of the Input_Grid.

Slice:
  - Properties:
      - Height: H_slice (H_slice == H_out)
      - Width: W_slice (W_slice == W_in)
      - Index: Position in the vertical stack (0-indexed from top)
      - Pixels: Sub-array of Input_Grid pixels
      - Colors_Present: Set of unique colors within the slice
      - Content_Pixel_Count: Number of pixels whose color is not a Background_Color.

Background_Colors:
  - Definition: Set of colors that are present in *every* Slice of the Input_Grid.
  - Role: Represent background or framing elements, not primary content.

Selection_Rule:
  - Action: Compare slices based on their Content_Pixel_Count.
  - Condition: The Slice with the maximum Content_Pixel_Count is selected.
  - Tie-breaking: If multiple slices share the maximum count, the one with the lowest Index (topmost) is selected (although not observed in examples).
  - Result: The selected Slice becomes the Output_Grid.

Assumptions:
  - H_in is divisible by H_out.
  - W_in is equal to W_out.
  - There are at least two slices to compare to determine Background_Colors effectively (if only one slice, it is the output).

```


**Natural Language Program:**

1.  Determine the height of the output grid (`H_out`) from the examples. This defines the `slice_height`.
2.  Determine the width of the grids (`W`).
3.  Divide the input grid vertically into non-overlapping horizontal slices, each of size `slice_height` x `W`. Let the number of slices be `N`.
4.  If `N` is 1, the input grid itself is the output grid. Stop.
5.  Identify the set of "Background Colors":
    a.  Find the set of unique colors present in the first slice.
    b.  For each subsequent slice (from the second to the `N`th slice), find the set of unique colors within it.
    c.  The "Background Colors" are the colors common to the unique color sets of *all* `N` slices (the intersection of all sets).
6.  For each slice (indexed `i` from 0 to `N-1`):
    a.  Initialize a `content_pixel_count` for slice `i` to 0.
    b.  Iterate through each pixel in slice `i`.
    c.  If the pixel's color is *not* in the set of "Background Colors", increment the `content_pixel_count` for slice `i`.
7.  Find the slice index (`best_slice_index`) that corresponds to the maximum `content_pixel_count` found across all slices. If there is a tie for the maximum count, choose the lowest index among the tied slices.
8.  Extract the slice corresponding to `best_slice_index` from the input grid. This extracted slice is the final output grid.
```python
"""
Transforms the input grid by extracting a specific horizontal slice.

The transformation assumes the input grid is composed of exactly 3
vertically stacked slices of equal height (input height / 3).
It identifies 'background' colors (those colors present in all 3 slices)
and 'content' colors (all other colors present in the grid).
It then calculates the number of 'content' pixels within each of the 3 slices.
The slice containing the maximum number of content pixels is selected as
the output grid. If multiple slices share the maximum count, the topmost
slice (the one with the lowest starting row index) among them is chosen.
"""

import numpy as np

def get_unique_colors(grid_slice: np.ndarray) -> set:
    """Helper function finds the set of unique colors in a numpy grid slice."""
    # np.unique returns sorted unique elements. Converting to set is fast.
    return set(np.unique(grid_slice))

def transform(input_grid_list):
    """
    Applies the slice extraction logic to the input grid.

    Args:
        input_grid_list: A list of lists representing the input grid pixels.

    Returns:
        A list of lists representing the transformed output grid.

    Raises:
        ValueError: If the input grid height is not divisible by 3, or if the
                    height is less than 3, violating the core structural assumption
                    derived from the training examples.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)

    # Handle edge case: empty input grid
    if input_grid.size == 0:
        return [] # Return empty list for empty input

    H_in, W_in = input_grid.shape

    # 1. Determine slice height and number of slices based on the core assumption
    #    derived from examples: the input is composed of exactly 3 vertical slices.
    num_slices = 3
    if H_in % num_slices != 0:
        # This check enforces the structural assumption. If the input grid's height
        # is not divisible by 3, the logic derived cannot be applied.
        raise ValueError(f"Input grid height {H_in} is not divisible by {num_slices}.")

    slice_height = H_in // num_slices

    # Check for invalid slice height (occurs if H_in < num_slices, e.g., H_in=1 or H_in=2)
    if slice_height == 0:
         raise ValueError(f"Input grid height {H_in} is too small to form {num_slices} slices.")

    # 2. Divide the input grid into slices
    slices = []
    for i in range(num_slices):
        start_row = i * slice_height
        end_row = start_row + slice_height
        # Create views or copies of the slices
        slices.append(input_grid[start_row:end_row, :])

    # 3. Identify Background Colors
    # Background colors are defined as those colors present in ALL slices.
    # Initialize with colors from the first slice
    common_colors = get_unique_colors(slices[0])
    # Sequentially find the intersection with colors from subsequent slices
    for i in range(1, num_slices):
        slice_colors = get_unique_colors(slices[i])
        common_colors.intersection_update(slice_colors)
        # Optimization: if common_colors becomes empty, no need to check further
        if not common_colors:
            break
            
    background_colors = common_colors

    # 4. Calculate Content Pixel Count for Each Slice
    # Content pixels are defined as those whose color is NOT a background color.
    content_pixel_counts = []
    for i in range(num_slices):
        current_slice = slices[i]
        count = 0
        # Use numpy's unique function with return_counts for efficiency
        unique_slice_colors, counts_in_slice = np.unique(current_slice, return_counts=True)
        # Iterate through the unique colors found in the current slice
        for color, num_pixels in zip(unique_slice_colors, counts_in_slice):
             # If the color is not in the set of background colors, add its count
             if color not in background_colors:
                 count += num_pixels
        content_pixel_counts.append(count)

    # 5. Find Best Slice Index
    # The best slice is the one with the maximum content pixel count.
    # np.argmax is suitable as it returns the index of the *first* occurrence
    # of the maximum value, automatically handling ties by choosing the lowest index (topmost slice).
    if not content_pixel_counts:
         # This case should theoretically not be reached if input is valid and slicing worked.
         # However, if it occurs (e.g., all pixels are background), default to the first slice.
         best_slice_index = 0
    else:
        best_slice_index = np.argmax(content_pixel_counts)

    # 6. Extract the Best Slice
    # Select the slice corresponding to the determined index
    output_grid = slices[best_slice_index]

    # Convert the resulting numpy array back to a list of lists format for the ARC standard output
    return output_grid.tolist()
```
```python
import numpy as np
from collections import Counter

"""
Transforms the input grid by first selecting a specific horizontal slice and then modifying it through horizontal color expansion.

The transformation follows these steps:
1.  **Slicing:** Assumes the input grid is composed of exactly 3 vertically stacked slices of equal height. The input grid is divided into these three slices.
2.  **Background Identification:** Determines 'background' colors by finding the set of colors present in *all* three slices.
3.  **Slice Selection:** Calculates the number of 'content' pixels (non-background colors) in each slice. The slice with the maximum number of content pixels is selected. Ties are broken by choosing the topmost slice (lowest index).
4.  **Fill Color Identification:** Within the selected slice, identifies the 'fill color'. This is the background color that appears most frequently in that specific slice. If background colors are tied in frequency, the one with the lower numerical value is chosen. If no background colors are present in the selected slice (or if no background colors were identified globally), no fill color is determined.
5.  **Horizontal Expansion:** Creates a modified version of the selected slice. For each pixel that is a 'content' color in the original selected slice, its color is expanded horizontally (left and right) into adjacent pixels, overwriting them *only if* their original color was the 'fill color'. Expansion stops at the grid boundaries or when a pixel of a different color (not the fill color) is encountered. If no fill color was determined, this step is skipped.
6.  **Output:** The resulting modified slice is the output grid.
"""


def _get_unique_colors(grid_slice: np.ndarray) -> set:
    """Helper function finds the set of unique non-zero colors in a numpy grid slice."""
    return set(np.unique(grid_slice))

def _get_fill_color(grid_slice: np.ndarray, background_colors: set) -> int | None:
    """
    Identifies the most frequent background color within the slice.

    Args:
        grid_slice: The numpy array representing the selected slice.
        background_colors: A set of colors identified as background.

    Returns:
        The integer color value of the most frequent background color in the slice,
        or None if no background colors are present in the slice.
    """
    if not background_colors:
        return None # No background colors defined globally

    # Flatten the slice and count all colors
    colors, counts = np.unique(grid_slice, return_counts=True)
    
    # Filter counts to include only background colors present in this slice
    bg_color_counts = {
        color: count
        for color, count in zip(colors, counts)
        if color in background_colors
    }

    if not bg_color_counts:
        return None # No background colors found in this specific slice

    # Find the background color with the maximum count
    # If counts are tied, max() on the dictionary items will prioritize the key (color value)
    # after prioritizing the value (count). We want max count, then min color value for ties.
    # A more explicit way:
    max_count = -1
    fill_color = None
    # Sort by count desc, then color asc to handle ties consistently
    sorted_bg_colors = sorted(bg_color_counts.items(), key=lambda item: (-item[1], item[0]))

    if sorted_bg_colors:
       fill_color = sorted_bg_colors[0][0]
       return int(fill_color) # Ensure return type is standard int
       
    return None # Should not be reached if bg_color_counts was not empty

def _expand_horizontally(grid_slice: np.ndarray, background_colors: set, fill_color: int | None) -> np.ndarray:
    """
    Performs the horizontal expansion of content colors into the fill color.

    Args:
        grid_slice: The numpy array representing the selected slice.
        background_colors: A set of colors identified as background.
        fill_color: The specific background color to be overwritten by expansion.

    Returns:
        A new numpy array representing the slice after horizontal expansion.
    """
    # If there's no fill color, no expansion can occur
    if fill_color is None:
        return grid_slice.copy() # Return a copy to maintain immutability of the original slice

    H, W = grid_slice.shape
    output_slice = grid_slice.copy() # Work on a copy

    for r in range(H):
        for c in range(W):
            original_color = grid_slice[r, c]

            # Check if the current pixel is a content color
            if original_color not in background_colors:
                content_color = original_color

                # Expand Left
                for col in range(c - 1, -2, -1): # Go from c-1 down to -1 (boundary check)
                    if col < 0: # Hit left boundary
                        break
                    # Check the color in the *original* slice to decide if we can expand *into* it
                    if grid_slice[r, col] == fill_color:
                        # Modify the output slice
                        output_slice[r, col] = content_color
                    else:
                        # Stop expanding left if we hit a non-fill color
                        break

                # Expand Right
                for col in range(c + 1, W + 1, 1): # Go from c+1 up to W (boundary check)
                    if col >= W: # Hit right boundary
                        break
                     # Check the color in the *original* slice to decide if we can expand *into* it
                    if grid_slice[r, col] == fill_color:
                         # Modify the output slice
                        output_slice[r, col] = content_color
                    else:
                        # Stop expanding right if we hit a non-fill color
                        break
                        
    return output_slice


def transform(input_grid_list):
    """
    Applies the slice selection and horizontal expansion logic.

    Args:
        input_grid_list: A list of lists representing the input grid pixels.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)

    # Handle edge case: empty input grid
    if input_grid.size == 0:
        return []

    H_in, W_in = input_grid.shape

    # --- 1. Slicing ---
    num_slices = 3
    if H_in == 0 or H_in % num_slices != 0:
        # If height is 0 or not divisible by 3, the core assumption is violated.
        # Depending on ARC rules, might return input, raise error, or return empty.
        # Returning input unchanged seems safest if the pattern doesn't match.
        # However, the examples strongly suggest divisibility by 3 is required.
        # Let's raise an error for clarity during development/testing.
        raise ValueError(f"Input grid height {H_in} is not divisible by {num_slices} or is zero.")

    slice_height = H_in // num_slices

    slices = []
    for i in range(num_slices):
        start_row = i * slice_height
        end_row = start_row + slice_height
        slices.append(input_grid[start_row:end_row, :])

    # --- 2. Background Identification ---
    if not slices: # Should not happen if H_in > 0 and divisible by 3
         return []

    common_colors = _get_unique_colors(slices[0])
    for i in range(1, num_slices):
        slice_colors = _get_unique_colors(slices[i])
        common_colors.intersection_update(slice_colors)
        if not common_colors: # Optimization
            break
    background_colors = common_colors

    # --- 3. Slice Selection ---
    content_pixel_counts = []
    for i in range(num_slices):
        current_slice = slices[i]
        count = 0
        # Efficiently count non-background pixels
        mask = ~np.isin(current_slice, list(background_colors))
        count = np.sum(mask)
        content_pixel_counts.append(count)

    # Find the index of the slice with the maximum content pixels
    # np.argmax handles ties by returning the first occurrence (lowest index)
    if not content_pixel_counts: # Should only happen if input was empty or H_in=0
        best_slice_index = 0 # Default to first slice if counts are somehow empty
    else:
        best_slice_index = np.argmax(content_pixel_counts)

    selected_slice = slices[best_slice_index]

    # --- 4. Fill Color Identification ---
    fill_color = _get_fill_color(selected_slice, background_colors)

    # --- 5. Horizontal Expansion ---
    output_grid_np = _expand_horizontally(selected_slice, background_colors, fill_color)

    # --- 6. Output ---
    # Convert the resulting numpy array back to a list of lists
    return output_grid_np.tolist()
```
