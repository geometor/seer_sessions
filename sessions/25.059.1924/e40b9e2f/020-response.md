# e40b9e2f • 020 • refine_coder

---
```python
"""
1.  **Locate the Maroon Pixel:** Find the single maroon (color code 9) pixel in the input grid.
2.  **Identify the Azure Rectangle:** Find the single azure (color code 8) rectangle in the input grid. If either the maroon pixel or the azure rectangle is not present, the program stops and returns the original grid.
3.  **Determine Mirroring Lines:** Calculate the row indices corresponding to the top and bottom edges of the azure rectangle.
4.  **Mirror the Maroon Pixel:** Mirror the position of the maroon pixel across the top and bottom edges of the azure rectangle, calculating a new row index for each reflection.
5.  **Bound Check**: If a mirrored position is within the grid bounds, create a new maroon pixel.
6.  **Place Maroon Pixels:** Place the new maroon pixels at the *in-bound* mirrored positions, overwriting any existing pixels at those locations. The output grid includes the original maroon pixel and any mirrored maroon pixels that are within bounds.
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
    grid_height = output_grid.shape[0]

    # 1. Locate the Maroon Pixel
    maroon_pixels = find_object(input_grid, 9, "pixel")

    # 2. Identify the Azure Rectangle
    azure_rectangles = find_object(input_grid, 8, "rectangle")

    if not maroon_pixels or not azure_rectangles:
        return output_grid  # Return original if objects are missing
    
    maroon_pixel = maroon_pixels[0]
    azure_rectangle = azure_rectangles[0]

    top_left, (height, width) = azure_rectangle
    top_edge = top_left[0]
    bottom_edge = top_left[0] + height - 1

    # 3. Determine Mirroring Lines (already done above)

    # 4. Mirror the Maroon Pixel
    mirrored_top, mirrored_bottom = mirror_position(maroon_pixel, top_edge, bottom_edge)

    # 5. Bound Check and 6. Place Maroon Pixels
    if 0 <= mirrored_top[0] < grid_height:
        output_grid[mirrored_top] = 9
    if 0 <= mirrored_bottom[0] < grid_height:
        output_grid[mirrored_bottom] = 9

    return output_grid
```
