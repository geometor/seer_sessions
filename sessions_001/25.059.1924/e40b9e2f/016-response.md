# e40b9e2f • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate the single maroon (9) pixel and the azure (8) rectangular block within the input grid.

2.  **Mirror the maroon pixel:** Locate the positions obtained by mirroring the maroon pixel across the top and the bottom border of the azure rectangle.

3. **Place Additional Maroon Pixels:** If it is not there already, add a maroon pixel to the locations determined in step 2.

4.  **Output:** The output grid consists of the initial input, plus the extra maroon pixels.
"""

import numpy as np

def find_object(grid, color, object_type="pixel"):
    """Finds objects of a specific color in the grid."""
    objects = []
    if object_type == "pixel":
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == color:
                    objects.append((i, j))
    elif object_type == "rectangle":
        # Find top-left corner
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == color:
                    # Determine dimensions
                    height = 0
                    width = 0

                    #check if a solid rectangle exists
                    for row in range(i, grid.shape[0]):
                        if grid[row,j] == color:
                            height +=1
                        else:
                            break

                    for col in range(j, grid.shape[1]):
                        if grid[i,col] == color:
                            width += 1
                        else:
                            break

                    # we're looking for solid rectangles not lines
                    if (height > 1) and (width > 1):
                        objects.append( ((i,j), (height, width)) ) #top_left, (height, width)
                    
                    #we can stop after we find 1 rectangle
                    return objects
    return objects

def mirror_position(point, top_edge, bottom_edge):
    """Mirrors a point across top and bottom edges."""
    x, y = point
    mirrored_top_x = top_edge - (x - top_edge)
    mirrored_bottom_x = bottom_edge + (bottom_edge - x)
    return (mirrored_top_x, y), (mirrored_bottom_x, y)

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)

    # 1. Identify Objects
    maroon_pixels = find_object(input_grid, 9, "pixel")
    azure_rectangles = find_object(input_grid, 8, "rectangle")

    if not maroon_pixels or not azure_rectangles:
        return output_grid  # Return original if objects are missing
    
    maroon_pixel = maroon_pixels[0]
    azure_rectangle = azure_rectangles[0]

    top_left, (height, width) = azure_rectangle
    top_edge = top_left[0]
    bottom_edge = top_left[0] + height -1

    # 2. Mirror the maroon pixel
    mirrored_top, mirrored_bottom = mirror_position(maroon_pixel, top_edge, bottom_edge)

    # 3. Place Additional Maroon Pixels
    if output_grid[mirrored_top] != 9:
      output_grid[mirrored_top] = 9
    if output_grid[mirrored_bottom] != 9:
      output_grid[mirrored_bottom] = 9

    return output_grid
```
