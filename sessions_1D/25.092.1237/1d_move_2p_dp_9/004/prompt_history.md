
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 6 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 0
```


## train_3

**input:**
```
0 0 0 5 5 5 5 5 5 5 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 5 6 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

1.  **Input/Output Format:** The inputs and outputs are 1D arrays (or grids) of integers representing pixel colors.
2.  **Colors Present:** The colors observed are white (0), yellow (4), magenta (6), orange (7), and gray (5). White serves as the background color.
3.  **Key Objects:** In each input, there are two distinct non-white objects:
    *   A contiguous block of a single color (yellow, orange, or gray).
    *   A single pixel of magenta (6).
4.  **Transformation:** The transformation involves shifting the positions of the non-white objects within the grid. The grid size remains constant.
5.  **Shift Pattern:**
    *   The contiguous block of color (yellow, orange, gray) is shifted 2 positions to the right.
    *   The single magenta pixel (6) is shifted 1 position to the right.
6.  **Background Handling:** Positions vacated by the shifted objects and the positions to the left of the newly placed objects are filled with the background color (white, 0). The overall length of the array remains unchanged.

## Facts


```yaml
task_type: array_transformation_1d
components:
  - role: background
    color: white (0)
    properties: fills empty space
  - role: main_object
    description: A contiguous block of a single non-white, non-magenta color.
    colors_observed: [yellow (4), orange (7), gray (5)]
    properties:
      - contiguous
      - single_color (excluding white and magenta)
    action: shifted right by 2 positions
  - role: marker_object
    description: A single pixel of magenta color.
    color: magenta (6)
    properties:
      - single_pixel
    action: shifted right by 1 position
grid_properties:
  - type: 1D array
  - size: constant between input and output
relationships:
  - The main_object and marker_object are distinct and do not overlap in the input.
  - Their relative order can vary (marker can be before or after the main block).
  - The shift amounts are constant and independent of the object's color or initial position (main block always +2, marker always +1).
```


## Natural Language Program

1.  Initialize an output array of the same size as the input array, filled entirely with the background color (white, 0).
2.  Identify the contiguous block of pixels in the input array that are neither white (0) nor magenta (6). Record its color, starting index, and length.
3.  Identify the index of the single magenta (6) pixel in the input array.
4.  Calculate the new starting index for the main color block by adding 2 to its original starting index.
5.  Calculate the new index for the magenta pixel by adding 1 to its original index.
6.  Place the main color block (using its recorded color and length) into the output array starting at its calculated new index.
7.  Place the magenta pixel (6) into the output array at its calculated new index.
8.  Return the modified output array.
```python
import numpy as np

"""
1. Initialize an output array of the same size as the input array, filled entirely with the background color (white, 0).
2. Identify the contiguous block of pixels in the input array that are neither white (0) nor magenta (6). Record its color, starting index, and length.
3. Identify the index of the single magenta (6) pixel in the input array.
4. Calculate the new starting index for the main color block by adding 2 to its original starting index.
5. Calculate the new index for the magenta pixel by adding 1 to its original index.
6. Place the main color block (using its recorded color and length) into the output array starting at its calculated new index.
7. Place the magenta pixel (6) into the output array at its calculated new index.
8. Return the modified output array.
"""

def find_main_object(grid):
    """Finds the contiguous block of non-white, non-magenta color."""
    color = -1
    start_index = -1
    length = 0
    in_object = False
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 6:
            if not in_object:
                color = pixel
                start_index = i
                length = 1
                in_object = True
            else:
                length += 1
        elif in_object:
            # End of the object
            break
    if start_index == -1:
        raise ValueError("Main object not found in grid")
    return color, start_index, length

def find_marker_object(grid, marker_color=6):
    """Finds the index of the marker pixel."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    raise ValueError(f"Marker object with color {marker_color} not found in grid")


def transform(input_grid):
    """
    Transforms the input grid by shifting the main color block 2 positions
    to the right and the single magenta pixel 1 position to the right.
    """
    # Convert input to a NumPy array for easier handling if it's not already
    # Assuming input_grid is a list or similar iterable
    grid = np.array(input_grid)
    grid_size = len(grid)
    
    # 1. Initialize output_grid with background color (0)
    output_grid = np.zeros(grid_size, dtype=int)

    # 2. Identify the main object
    main_color, main_start_index, main_length = find_main_object(grid)

    # 3. Identify the marker object (magenta, 6)
    marker_index = find_marker_object(grid, marker_color=6)

    # 4. Calculate the new start index for the main object
    new_main_start_index = main_start_index + 2

    # 5. Calculate the new index for the marker object
    new_marker_index = marker_index + 1

    # 6. Place the main object in the output grid
    # Ensure the object stays within bounds
    if new_main_start_index < grid_size:
        end_index = min(new_main_start_index + main_length, grid_size)
        output_grid[new_main_start_index:end_index] = main_color

    # 7. Place the marker object in the output grid
    # Ensure the marker stays within bounds
    if new_marker_index < grid_size:
        output_grid[new_marker_index] = 6 # Magenta color

    # 8. Return the modified output grid as a list
    return output_grid.tolist()
```
```python
import numpy as np

"""
Transforms a 1D input grid based on the following rules:
1. Initialize an output array of the same size as the input array, filled entirely with the background color (white, 0).
2. Identify the contiguous block of pixels in the input array that are neither white (0) nor magenta (6) (the "main object"). Record its color, starting index, and length.
3. Identify the index of the single magenta (6) pixel in the input array (the "marker object"). Record its index.
4. Calculate the new starting index for the main object by adding 2 to its original starting index.
5. Place the main object (using its recorded color and length) into the output array starting at its calculated new index. Ensure the placement does not exceed the array bounds; truncate if necessary.
6. Place the marker object (magenta pixel, 6) into the output array at its *original* identified index.
7. Return the modified output array.
"""

def find_main_object(grid):
    """
    Finds the contiguous block of non-white (0), non-magenta (6) color.

    Args:
        grid (np.array): The 1D input grid.

    Returns:
        tuple: (color, start_index, length) of the main object,
               or (-1, -1, 0) if not found.
    """
    color = -1
    start_index = -1
    length = 0
    in_object = False
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 6: # Found a potential start or continuation
            if not in_object:
                color = pixel
                start_index = i
                length = 1
                in_object = True
            elif pixel == color: # Continue the object
                 length += 1
            else: # Different non-background/marker color, means end of object
                 break
        elif in_object: # Found background or marker after being in an object
            # End of the object
            break
    # Handle case where object runs to the end of the grid (no break occurred)
    if start_index == -1:
        # Optionally raise an error or return indication of not found
        # raise ValueError("Main object not found in grid")
        return -1, -1, 0
    return color, start_index, length

def find_marker_object(grid, marker_color=6):
    """
    Finds the index of the first occurrence of the marker pixel color.

    Args:
        grid (np.array): The 1D input grid.
        marker_color (int): The color of the marker object to find.

    Returns:
        int: The index of the marker object, or -1 if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    # Optionally raise an error or return indication of not found
    # raise ValueError(f"Marker object with color {marker_color} not found in grid")
    return -1


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is a numpy array for easier slicing
    grid = np.array(input_grid)
    grid_size = len(grid)

    # 1. Initialize output_grid with background color (0)
    output_grid = np.zeros(grid_size, dtype=int)

    # 2. Identify the main object
    main_color, main_start_index, main_length = find_main_object(grid)

    # 3. Identify the marker object (magenta, 6)
    marker_index = find_marker_object(grid, marker_color=6)

    # Proceed only if both objects are found
    if main_start_index != -1 and marker_index != -1:
        # 4. Calculate the new start index for the main object
        new_main_start_index = main_start_index + 2

        # 5. Place the main object in the output grid, handling boundaries
        if new_main_start_index < grid_size:
            # Calculate how much of the object fits
            placeable_length = min(main_length, grid_size - new_main_start_index)
            end_index = new_main_start_index + placeable_length
            output_grid[new_main_start_index:end_index] = main_color

        # 6. Place the marker object in the output grid at its original index
        # Check bounds just in case, though marker_index should be valid if found
        if 0 <= marker_index < grid_size:
            output_grid[marker_index] = 6 # Magenta color

    # 7. Return the modified output grid as a list
    return output_grid.tolist()
```
