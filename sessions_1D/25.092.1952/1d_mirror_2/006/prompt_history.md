
## train_1

**input:**
```
4 4 4 4 4 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 0 4 4 4 4 4 0 0 0 0 0
```


## train_2

**input:**
```
0 0 5 5 5 5 0 0 9 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 9 0 0 5 5 5 5 0 0 0
```


## train_3

**input:**
```
0 0 0 5 5 5 5 5 0 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 9 0 5 5 5 5 5 0 0
```

**Perception of the Elements:**

1.  **Grid Structure:** Both input and output grids are 1-dimensional arrays (1x18).
2.  **Key Colors:** Three colors are primarily involved: white (0), maroon (9), and another color (yellow - 4 in this example, gray - 5 in others).
3.  **Persistent Elements:**
    *   A single maroon pixel (9) acts as a fixed reference point or marker. Its position does not change between input and output.
    *   A contiguous block of a non-white, non-maroon color exists (e.g., `4 4 4 4 4`). This block constitutes the primary "object" being manipulated.
4.  **Transformation:** The core transformation involves moving the colored object block.
    *   In the input, the object block (`4 4 4 4 4`) is located at the beginning (indices 0-4).
    *   The marker pixel (`9`) is at index 6.
    *   In the output, the marker pixel (`9`) remains at index 6.
    *   The object block (`4 4 4 4 4`) is now located starting at index 8.
    *   The original location of the object block is filled with white pixels (0).
5.  **Relative Positioning:** The object block moves from its original position to a new position relative to the fixed maroon marker. Specifically, it moves to the position starting two indices *after* the marker's index (Marker at index `i`, Object starts at index `i+2`). The space between the marker and the object (index `i+1`) is filled with a white pixel.

**Facts:**


```yaml
task_elements:
  - grid_dimensions:
      type: ثابت # constant
      value: 1x18 (inferred from example)
  - background_color:
      id: 0
      name: white
  - marker:
      id: 9
      name: maroon
      shape: single pixel
      role: fixed reference point
      property: position remains unchanged
  - movable_object:
      property: contiguous block of pixels
      color: non-white and non-maroon (e.g., 4 - yellow, 5 - gray)
      role: element to be relocated
      relationship_to_marker_input: varies
      relationship_to_marker_output: starts two positions after the marker's index
  - action:
      type: move
      target: movable_object
      destination: new position relative to the marker
      details:
        - The original position of the movable_object is filled with the background_color (white).
        - The new position starts two indices after the marker's index.
        - The index immediately following the marker becomes background_color (white).
```


**Natural Language Program:**

1.  Identify the single maroon (9) pixel in the input grid; note its index (marker_index).
2.  Identify the contiguous block of pixels whose color is neither white (0) nor maroon (9); note its pixels (object_pixels) and its starting index (original_start_index) and ending index (original_end_index).
3.  Create a new grid identical to the input grid.
4.  Fill the cells in the new grid from original_start_index to original_end_index with white (0) pixels.
5.  Calculate the new starting index for the object block as `new_start_index = marker_index + 2`.
6.  Place the object_pixels into the new grid starting at `new_start_index`.
```python
import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Identify the single maroon (9) pixel (marker) and its index.
Identify the contiguous block of pixels whose color is neither white (0) nor maroon (9) (movable object), noting its color, pixels, start and end indices.
Create a new grid filled with white (0) pixels, the same size as the input.
Place the maroon marker in the new grid at its original index.
Calculate the new starting index for the movable object as marker_index + 2.
Place the movable object's pixels into the new grid starting at the calculated new index.
Return the modified grid.
"""

def find_pixel_index(grid: List[int], color: int) -> Optional[int]:
    """Finds the index of the first occurrence of a specific color."""
    for i, pixel in enumerate(grid):
        if pixel == color:
            return i
    return None # Should not happen based on task description

def find_contiguous_object(grid: List[int], exclude_colors: List[int]) -> Optional[Tuple[int, int, int, List[int]]]:
    """
    Finds the first contiguous block of pixels whose color is not in exclude_colors.
    Returns: (start_index, end_index, object_color, object_pixels) or None if not found.
    """
    start_index = -1
    object_color = -1
    object_pixels = []
    for i, pixel in enumerate(grid):
        if pixel not in exclude_colors:
            if start_index == -1: # Start of a potential object
                start_index = i
                object_color = pixel
                object_pixels.append(pixel)
            elif pixel == object_color: # Continuing the object
                 object_pixels.append(pixel)
            else: # Found a different color, previous object ends
                 end_index = i - 1
                 return start_index, end_index, object_color, object_pixels
        elif start_index != -1: # End of the object block
            end_index = i - 1
            return start_index, end_index, object_color, object_pixels

    # Check if object runs until the end of the grid
    if start_index != -1:
        end_index = len(grid) - 1
        return start_index, end_index, object_color, object_pixels

    return None # No object found


def transform(input_grid_list: List[int]) -> List[int]:
    """
    Moves a contiguous block of non-white, non-maroon pixels to a position
    relative to a fixed maroon marker pixel.
    """
    # Convert list to numpy array for easier slicing if needed, though list ops are fine here.
    # input_grid = np.array(input_grid_list) # Optional, sticking with lists for simplicity
    grid_size = len(input_grid_list)
    background_color = 0
    marker_color = 9
    exclude_colors = [background_color, marker_color]

    # 1. Identify the marker pixel index
    marker_index = find_pixel_index(input_grid_list, marker_color)
    if marker_index is None:
        # Handle error: marker not found (optional based on problem constraints)
        return input_grid_list # Or raise error

    # 2. Identify the movable object
    object_info = find_contiguous_object(input_grid_list, exclude_colors)
    if object_info is None:
         # Handle error: object not found (optional based on problem constraints)
        return input_grid_list # Or raise error
    
    _original_start_index, _original_end_index, _object_color, object_pixels = object_info
    object_length = len(object_pixels)

    # 3. Create a new grid filled with the background color
    output_grid_list = [background_color] * grid_size

    # 4. Place the marker in the new grid
    output_grid_list[marker_index] = marker_color

    # 5. Calculate the new starting index for the object
    new_start_index = marker_index + 2

    # 6. Place the object pixels into the new grid
    # Ensure placement doesn't go out of bounds
    new_end_index = new_start_index + object_length
    if new_end_index <= grid_size:
         output_grid_list[new_start_index:new_end_index] = object_pixels
    else:
         # Handle potential out-of-bounds placement if necessary
         # For this specific task, examples suggest it fits.
         pass # Or adjust logic if needed

    # Convert back to list if numpy was used
    # return output_grid.tolist()
    return output_grid_list
```
```python
"""
Transforms an input 1D grid based on the following rules:
1. Identifies a single 'marker' pixel (maroon, 9) and its index (`marker_index`).
2. Identifies the first contiguous block of pixels (the 'object') whose color is neither background (white, 0) nor the marker color. Notes the object's pixel sequence (`object_pixels`), start index (`original_start_index`), and end index (`original_end_index`).
3. Calculates a new starting index for the object using the formula: `new_start_index = 2 * marker_index - original_end_index`.
4. Creates a new grid of the same size, filled with the background color.
5. Places the marker pixel at its original index (`marker_index`) in the new grid.
6. Places the object's pixels (`object_pixels`) into the new grid, starting at the calculated `new_start_index`.
"""

import numpy as np
from typing import List, Tuple, Optional

# Define constants for colors
BACKGROUND_COLOR = 0
MARKER_COLOR = 9

def find_marker_index(grid: List[int], marker_color: int) -> Optional[int]:
    """Finds the index of the first occurrence of the marker color."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return None # Marker not found

def find_object(grid: List[int], exclude_colors: List[int]) -> Optional[Tuple[List[int], int, int]]:
    """
    Finds the first contiguous block of pixels whose color is not in exclude_colors.
    Returns: (object_pixels, start_index, end_index) or None if not found.
    """
    object_pixels = []
    start_index = -1
    end_index = -1
    current_object_color = -1

    for i, pixel in enumerate(grid):
        if pixel not in exclude_colors:
            if start_index == -1: # Start of a potential object
                start_index = i
                current_object_color = pixel
                object_pixels.append(pixel)
            elif pixel == current_object_color: # Continuing the object
                object_pixels.append(pixel)
            else: # Found a different non-excluded color, object ended at i-1
                end_index = i - 1
                return object_pixels, start_index, end_index
        elif start_index != -1: # End of the object block (encountered excluded color)
            end_index = i - 1
            return object_pixels, start_index, end_index

    # Check if object runs until the end of the grid
    if start_index != -1:
        end_index = len(grid) - 1
        return object_pixels, start_index, end_index

    return None # No object found

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    """
    grid_size = len(input_grid)
    exclude_colors = [BACKGROUND_COLOR, MARKER_COLOR]

    # 1. Find the marker index
    marker_index = find_marker_index(input_grid, MARKER_COLOR)
    if marker_index is None:
        print("Error: Marker pixel not found.")
        return input_grid # Return original grid or raise error

    # 2. Find the object pixels and its original indices
    object_info = find_object(input_grid, exclude_colors)
    if object_info is None:
        print("Error: Movable object not found.")
        return input_grid # Return original grid or raise error
    
    object_pixels, _original_start_index, original_end_index = object_info
    object_length = len(object_pixels)

    # 3. Calculate the new starting index for the object
    # Formula derived from examples: new_start = 2 * marker_pos - original_end
    new_start_index = (2 * marker_index) - original_end_index
    new_end_index = new_start_index + object_length # Calculate expected end index

    # 4. Create a new grid filled with the background color
    output_grid = [BACKGROUND_COLOR] * grid_size

    # 5. Place the marker in the new grid
    if 0 <= marker_index < grid_size:
         output_grid[marker_index] = MARKER_COLOR
    else:
         # This case should ideally not happen if marker is found
         print(f"Warning: Marker index {marker_index} out of bounds for grid size {grid_size}.")


    # 6. Place the object pixels into the new grid at the calculated position
    # Check if the calculated placement is valid within grid bounds
    if 0 <= new_start_index < grid_size and new_end_index <= grid_size:
        for i in range(object_length):
            output_grid[new_start_index + i] = object_pixels[i]
    else:
        # Handle cases where the calculated position might be invalid/out of bounds
        # Based on the examples, this calculation seems robust, but good practice to check.
        print(f"Warning: Calculated object placement [{new_start_index}:{new_end_index}] might be out of bounds for grid size {grid_size}.")
        # Potentially adjust behavior here if needed, e.g., clamp indices or return an error state.
        # For now, attempt placement even if partially out of bounds, relying on list slicing behavior.
        # Note: Python slicing handles out-of-bounds gracefully for assignment length mismatch, 
        # but direct index assignment needs care. The loop above is safer.
        # A slice assignment alternative (less safe if indices are wrong):
        # output_grid[new_start_index:new_end_index] = object_pixels 
        # --> Let's stick to the loop for explicit index checking.
        pass # Continue, potentially placing partial object if start is valid but end goes over

    return output_grid
```
```python
"""
Transforms a 1D input grid based on the following reflection-like rule:
1. Identifies a single 'marker' pixel (maroon, 9) and its index (`marker_index`).
2. Identifies the first contiguous block of pixels (the 'object') whose color is neither background (white, 0) nor the marker color. Notes the object's pixel sequence (`object_pixels`) and its ending index in the input grid (`original_end_index`).
3. Creates a new grid of the same size, filled with the background color (white, 0).
4. Places the marker pixel at its original index (`marker_index`) in the new grid.
5. Calculates a new starting index for the object (`new_start_index`) using the formula: `new_start_index = (2 * marker_index) - original_end_index`. This effectively reflects the object's position relative to the marker, mapping the original end position to the new start position.
6. Places the object's pixels (`object_pixels`) into the new grid, starting at the calculated `new_start_index`.
"""

from typing import List, Tuple, Optional

# Define constants for colors used in this task
BACKGROUND_COLOR = 0
MARKER_COLOR = 9

def find_marker_index(grid: List[int], marker_color: int) -> Optional[int]:
    """Finds the index of the first occurrence of the marker color."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return None # Marker not found

def find_object(grid: List[int], exclude_colors: List[int]) -> Optional[Tuple[List[int], int, int]]:
    """
    Finds the first contiguous block of pixels whose color is not in exclude_colors.
    Searches from the beginning of the grid.
    Returns: A tuple containing (object_pixels, start_index, end_index) or None if no such object is found.
             object_pixels: A list of the pixel values forming the object.
             start_index: The starting index of the object in the grid.
             end_index: The ending index of the object in the grid.
    """
    object_pixels = []
    start_index = -1
    end_index = -1
    current_object_color = -1

    for i, pixel in enumerate(grid):
        is_excluded = pixel in exclude_colors
        
        if not is_excluded: # Pixel is part of a potential object
            if start_index == -1: # Start of a new potential object
                start_index = i
                current_object_color = pixel
                object_pixels.append(pixel)
            elif pixel == current_object_color: # Continuing the current object
                object_pixels.append(pixel)
            else: # Found a different non-excluded color, the previous object ends here
                end_index = i - 1
                # We only care about the *first* object found
                return object_pixels, start_index, end_index
        elif start_index != -1: # Pixel is excluded, marks the end of the current object
            end_index = i - 1
            # We only care about the *first* object found
            return object_pixels, start_index, end_index

    # Check if an object was found and extends to the end of the grid
    if start_index != -1:
        end_index = len(grid) - 1
        return object_pixels, start_index, end_index

    # No object found matching the criteria
    return None

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the reflection transformation rule to the input grid.
    """
    grid_size = len(input_grid)
    exclude_colors = [BACKGROUND_COLOR, MARKER_COLOR]

    # --- Step 1: Initialize Output Grid ---
    # Create a new grid of the same size, filled with the background color
    output_grid = [BACKGROUND_COLOR] * grid_size

    # --- Step 2: Find Marker ---
    # Identify the single marker pixel (maroon, 9) and its index
    marker_index = find_marker_index(input_grid, MARKER_COLOR)
    
    # Handle case where marker is not found (though examples suggest it's always present)
    if marker_index is None:
        # print("Warning: Marker pixel not found. Returning default grid.")
        return output_grid # Or return input_grid, or raise error, depending on spec

    # --- Step 3: Place Marker in Output ---
    # Place the marker pixel into the output grid at its original index
    if 0 <= marker_index < grid_size:
         output_grid[marker_index] = MARKER_COLOR

    # --- Step 4: Find Object ---
    # Identify the first contiguous block of non-background, non-marker pixels
    object_info = find_object(input_grid, exclude_colors)

    # Handle case where object is not found (though examples suggest it's always present)
    if object_info is None:
        # print("Warning: Movable object not found. Returning grid with only marker.")
        return output_grid # Or return input_grid, or raise error

    object_pixels, _original_start_index, original_end_index = object_info
    object_length = len(object_pixels)

    # --- Step 5: Calculate New Position ---
    # Calculate the new starting index using the reflection formula
    new_start_index = (2 * marker_index) - original_end_index

    # --- Step 6: Place Object in Output ---
    # Place the object's pixels into the output grid at the calculated position
    # Ensure the placement stays within the grid bounds
    new_end_index_exclusive = new_start_index + object_length
    
    # Iterate and place pixel by pixel, checking bounds for each placement
    for i in range(object_length):
        current_output_index = new_start_index + i
        # Check if the calculated index is valid for the output grid
        if 0 <= current_output_index < grid_size:
            output_grid[current_output_index] = object_pixels[i]
        else:
            # Handle cases where part of the object might fall out of bounds
            # print(f"Warning: Object pixel placement out of bounds at index {current_output_index}.")
            pass # Skip placing pixels that fall outside the grid

    return output_grid
```
