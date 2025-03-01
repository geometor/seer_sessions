"""
Transforms the input grid into the output grid based on object identification, color swapping, and object translation.

1.  **Identify Objects:** Group contiguous pixels of the same color into objects.
2.  **Color Swap:**
    *   If an object has color 2(red), change its color to 4(yellow).
    *   If an object has color 5(gray), change its color to 3(green)
    *   If an object has color 6(magenta), change its color to 2(red).
3.  **Move Azure Object:** Find the largest object of color 8 (azure). Translate this object diagonally down and to the right. The exact translation vector might depend on the grid size or other factors (to be determined). Place this object so that it's as close to the bottom-right corner as possible without going out of bounds.
4. **Move other colored object:** Find the largest object of color 1(blue) or 4(yellow). Translate these objects diagonally down and to the right.
5. **Preserve other pixels:** All other pixels maintain their color and their position relative to other pixels of the same color.
"""

import numpy as np
from scipy.ndimage import measurements

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    labeled_array, num_features = measurements.label(grid)
    objects = []
    for i in range(1, num_features + 1):
        coords = np.argwhere(labeled_array == i)
        objects.append(coords.tolist())
    return objects

def change_color(grid, old_color, new_color):
    """Changes all pixels of old_color to new_color."""
    grid[grid == old_color] = new_color

def translate_object(grid, object_coords, translation_vector):
    """
    Translates an object within the grid.
    """
    new_coords = []
    rows, cols = grid.shape
    for r, c in object_coords:
        new_r = min(max(0, r + translation_vector[0]), rows-1)  # keep within bounds
        new_c = min(max(0, c + translation_vector[1]), cols-1)
        new_coords.append((new_r, new_c))
    return new_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.array(input_grid).copy()
    rows, cols = output_grid.shape
    
    # Identify Objects
    objects = find_objects(output_grid)

    # Color Swap
    change_color(output_grid, 2, 4)  # Red to yellow
    change_color(output_grid, 5, 3)  # Gray to green
    change_color(output_grid, 6, 2)  # Magenta to red

    # Move Azure Object
    azure_objects = [obj for obj in objects if output_grid[obj[0][0], obj[0][1]] == 8]
    if azure_objects:
        largest_azure = max(azure_objects, key=len)
        # Calculate a translation vector.  For now, a simple diagonal shift.
        #  This needs refinement based on further analysis.
        translation_vector = [rows - 1 - largest_azure[0][0], cols - 1- largest_azure[0][1]]
        
        #clear the original position of azure
        for r, c in largest_azure:
          output_grid[r,c] = 0

        new_azure_coords = translate_object(output_grid, largest_azure, translation_vector)

        #place the azure to the new position
        for r, c in new_azure_coords:
          output_grid[r,c] = 8

    # Move other colored object (Blue or Yellow)
    #   This logic also needs refinement.
    for move_color in [1,4]:
        color_objects = [obj for obj in objects if input_grid[obj[0][0], obj[0][1]] == move_color] #use the original color before swap
        if color_objects:
          largest_color_obj = max(color_objects, key=len)

          #Calculate a diagonal shift, the parameter need refinement based on analysis.
          translation_vector = [5,5]

          new_color_coords = translate_object(output_grid, largest_color_obj, translation_vector)
          #clear the original position
          for r, c in largest_color_obj:
            output_grid[r,c] = 0
          
          #get color from input grid (before color change)
          old_color = input_grid[largest_color_obj[0][0], largest_color_obj[0][1]]

          #put the objects to new positions
          for r,c in new_color_coords:
            output_grid[r,c] = old_color
          #correct color if needed after the move
          if old_color == 2:
            for r,c in new_color_coords:
              output_grid[r,c] = 4
    

    return output_grid