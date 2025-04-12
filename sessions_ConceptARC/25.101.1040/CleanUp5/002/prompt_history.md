
## train_1

**input:**
```
0 0 0 0 0 2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 3 0 2 0 0 0 2 0 3 0 0 0 2 0 0 0 2 0 0 3
0 0 2 0 0 0 0 0 2 0 0 0 3 0 0 0 0 0 3 0 0
0 2 0 3 0 0 0 0 0 2 0 2 0 0 0 3 0 0 0 2 0
2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


## train_2

**input:**
```
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 4 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0
```

## Perception

The task involves transforming an input grid into an output grid by selectively removing certain colored pixels (changing them to white/0). The rule for removal depends on the number of distinct non-white colors present in the input grid.

1.  **Case 1: Multiple non-white colors present (Example: train_1)**
    *   Input `train_1` contains red (2) and green (3) pixels.
    *   Output `train_1` contains only red (2) pixels.
    *   Observation: All pixels of the color with the highest numerical value (green=3) are removed (changed to white). The other non-white color (red=2) remains unchanged.

2.  **Case 2: Single non-white color present (Example: train_2)**
    *   Input `train_2` contains only yellow (4) pixels.
    *   Output `train_2` contains fewer yellow (4) pixels. Some specific yellow pixels have been removed.
    *   Observation: The removal seems related to the structure of the connected components formed by the single non-white color.
        *   Pixels forming components of size 1 (isolated single pixels) are removed.
        *   Pixels that are the starting points (leftmost for horizontal, presumably topmost for vertical) of small, simple line-shaped components (like size 2 horizontal segments) are also removed.
        *   Pixels within larger, more complex components are kept.

## YAML Facts


```yaml
task_type: color_removal_conditional
grid_properties:
  preserves_size: true
  background_color: 0 # white

input_features:
  - name: pixel_colors
    description: The grid contains pixels of various colors (0-9).
    values:
      - example_1: [0, 2, 3] # white, red, green
      - example_2: [0, 4] # white, yellow
  - name: color_count
    description: Number of distinct non-white colors in the input grid.
    values:
      - example_1: 2
      - example_2: 1
  - name: max_color_value
    description: The maximum numerical value among non-white colors present.
    values:
      - example_1: 3 # green
      - example_2: 4 # yellow
  - name: connected_components
    description: Non-white pixels of the same color form connected components (using 8-way adjacency).
    properties: [size, shape, pixels]
    relevant_when: color_count == 1
    observations:
      - example_2:
          components:
            - size: 1 # e.g., (0,0), (0,23), (1,6)
            - size: 2
              shape: horizontal_line # e.g., {(0,18), (0,19)}, {(1,13), (1,14)}
            - size: 24
              shape: complex

actions:
  - name: remove_pixel
    description: Change a pixel's color to the background color (0).
    conditions:
      - if: color_count > 1
        target: pixels where color == max_color_value
      - if: color_count == 1
        target: pixels belonging to components satisfying specific criteria (size 1, or start of small simple line)

transformation_logic:
  - condition: color_count > 1
    action: Remove all pixels whose color matches the maximum non-white color value in the input.
  - condition: color_count == 1
    action:
      - Find all connected components (8-way adjacency) of the single non-white color.
      - Remove pixels in components of size 1.
      - For components forming horizontal line segments of size > 1, remove the leftmost pixel.
      - (Hypothesized) For components forming vertical line segments of size > 1, remove the topmost pixel.
      - Keep all other pixels.

output_features:
  - name: pixel_colors
    description: The output grid contains a subset of the input's non-white pixels, or potentially none if all were removed.
    values:
      - example_1: [0, 2]
      - example_2: [0, 4]

```


## Natural Language Program

1.  **Analyze Input Colors**: Identify all distinct non-white colors present in the input grid and count how many distinct non-white colors there are (let this count be `N`).
2.  **Check Color Count**:
    *   **If `N` is greater than 1**:
        *   Find the non-white color with the highest numerical value.
        *   Create the output grid by copying the input grid.
        *   Change all pixels matching this highest color value to white (0) in the output grid.
    *   **If `N` is equal to 1**:
        *   Let the single non-white color be `C`.
        *   Create the output grid by copying the input grid.
        *   Find all connected components of color `C` using 8-way adjacency (pixels are connected if they touch sides or corners). Keep track of the pixels belonging to each component and the size (number of pixels) of each component.
        *   **Identify Pixels to Remove**:
            *   Initialize an empty set of pixels to remove.
            *   Iterate through all found components:
                *   If a component's size is 1, add its single pixel to the set of pixels to remove.
                *   If a component consists of exactly two pixels arranged horizontally (e.g., `(r, c)` and `(r, c+1)`), add the leftmost pixel `(r, c)` to the set of pixels to remove.
                *   (Hypothesized Extension) If a component consists of exactly two pixels arranged vertically (e.g., `(r, c)` and `(r+1, c)`), add the topmost pixel `(r, c)` to the set of pixels to remove. *(Note: This case wasn't explicitly tested in the examples but follows the pattern)*.
                *   (Refinement) Consider extending the horizontal/vertical line check for sizes greater than 2, still removing only the leftmost/topmost pixel.
        *   **Apply Removal**: Iterate through the set of pixels identified for removal. For each pixel coordinate in the set, change the corresponding pixel in the output grid to white (0).
3.  **Return Output**: The modified grid is the result.
```python
import numpy as np
from scipy.ndimage import label

"""
This function transforms an input grid based on the number and values of distinct non-white colors present.

Transformation Logic:

1.  **Analyze Input Colors**: Identify all distinct non-white (non-zero) colors in the input grid.
2.  **Count Distinct Colors**: Let the number of distinct non-white colors be `N`.
3.  **Apply Conditional Rules**:
    *   **If `N > 1` (Multiple distinct non-white colors):**
        *   Find the non-white color with the highest numerical value.
        *   Remove all pixels of this highest color by changing them to white (0).
    *   **If `N == 1` (Single distinct non-white color):**
        *   Let the single non-white color be `C`.
        *   Find all connected components (using 8-way adjacency) formed by pixels of color `C`.
        *   Identify pixels to remove based on component properties:
            *   Remove all pixels belonging to components of size 1 (isolated pixels).
            *   For components consisting of exactly two pixels arranged horizontally, remove the leftmost pixel.
        *   Keep all other pixels of color `C`.
    *   **If `N == 0` (No non-white colors):**
        *   The grid remains unchanged (all white).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the number and values of non-white colors.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Create a copy to modify for the output
    output_array = np.copy(input_array)
    
    # Find unique non-zero colors in the grid
    non_zero_colors = np.unique(input_array[input_array != 0])
    num_distinct_colors = len(non_zero_colors)

    # --- Apply transformation based on the number of distinct non-white colors ---

    if num_distinct_colors > 1:
        # Case 1: More than one non-white color present
        # Find the maximum color value among the non-zero colors
        max_color = np.max(non_zero_colors)
        # Set all pixels with the maximum color to 0 (white) in the output array
        output_array[output_array == max_color] = 0
        
    elif num_distinct_colors == 1:
        # Case 2: Exactly one non-white color present
        single_color = non_zero_colors[0]
        
        # Create a boolean mask where the grid matches the single color
        mask = input_array == single_color
        
        # Define the connectivity structure for finding components (8-way adjacency)
        # This means pixels are considered connected if they touch at sides or corners
        structure = np.array([[1, 1, 1], 
                              [1, 1, 1], 
                              [1, 1, 1]], dtype=bool)
        
        # Find connected components in the boolean mask
        # labeled_array assigns a unique integer label to each component
        # num_features gives the total number of components found (excluding background)
        labeled_array, num_features = label(mask, structure=structure)
        
        # Keep track of pixel coordinates that need to be removed (set to white)
        pixels_to_remove = set()
        
        # Iterate through each component found (labels are 1-based)
        for i in range(1, num_features + 1):
            # Get the coordinates (row, column) of all pixels belonging to the current component
            component_coords = np.argwhere(labeled_array == i)
            component_size = len(component_coords)
            
            if component_size == 1:
                # Rule: Remove components of size 1 (isolated pixels)
                # Get the single coordinate and add it to the removal set
                pixel_coord = tuple(component_coords[0])
                pixels_to_remove.add(pixel_coord)
                
            elif component_size == 2:
                # Rule: For components of size 2, check if they form a horizontal line
                p1 = component_coords[0] # Coordinates of the first pixel
                p2 = component_coords[1] # Coordinates of the second pixel
                
                # Check if rows are the same and columns differ by exactly 1
                if p1[0] == p2[0] and abs(p1[1] - p2[1]) == 1:
                    # This is a horizontal line of size 2
                    # Find the leftmost pixel (the one with the smaller column index)
                    leftmost_pixel_coord = tuple(p1) if p1[1] < p2[1] else tuple(p2)
                    # Add the leftmost pixel to the removal set
                    pixels_to_remove.add(leftmost_pixel_coord)
                    
                # Note: Vertical lines of size 2 or other size 2 configurations are not removed
                # based on the provided examples.

        # Apply the removals: Iterate through the collected coordinates and set them to white
        for r, c in pixels_to_remove:
            output_array[r, c] = 0
            
    # Case 3 (Implicit): If num_distinct_colors is 0, the output_array (a copy of input)
    # is already all white (or contains only 0s), so no changes are needed.

    # Convert the final NumPy array back to a list of lists format
    output_grid = output_array.tolist()
    
    return output_grid
```
