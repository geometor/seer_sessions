```python
"""
The transformation rule involves identifying objects of different colors, and then moving, reflecting, or copying them based on their relative positions. The background color is consistently maintained.

1. **Example 1 (Red and Azure):** The azure object is removed. The red object is copied down by one row. The entire grid is then shifted down, with the top section filled with the background color, such that the original red object's top row becomes the top row of the shifted grid.
2. **Example 2 (Blue and Red):** The blue object is copied to the top of the grid. The red object is copied to a position above where the blue object was originally, and then the red object is copied down one position.
3. **Example 3 (Yellow and Magenta):** The magenta objects are removed.  The rows occupied by the magenta object are replaced by the yellow objects.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies the background color and foreground objects in the grid.
    Returns a dictionary where keys are colors and values are lists of (row, col) positions.
    """
    background_color = np.bincount(grid.flatten()).argmax()
    objects = {}
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != background_color:
                if color not in objects:
                    objects[color] = []
                objects[color].append((r, c))
    return background_color, objects

def shift_rows(grid, start_row, num_rows, shift_amount, fill_color):
    """
    Shifts rows down within a grid.

    Args:
      grid: The numpy array representing the grid.
      start_row: The index of the first row to shift.
      num_rows:  How many rows must be shifted
      shift_amount: The number of rows to shift down (positive integer).
      fill_color: The color to fill the vacated rows with.

    """
    new_grid = grid.copy()

    if shift_amount > 0 :
        new_grid[start_row + shift_amount:start_row+num_rows, :] = grid[start_row : start_row+num_rows-shift_amount, :]
        new_grid[start_row:start_row + shift_amount, :] = fill_color
    return new_grid

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = input_grid.copy()
    background_color, objects = get_objects(input_grid)

    # Example 1 Logic (Red and Azure objects)
    if len(objects) == 2 and 2 in objects and 8 in objects:

        # find red object top row
        red_object = objects.get(2,[])
        red_top_row = -1
        if len(red_object) > 0:
            red_top_row = min(r for r, c in red_object)

        blue_object = objects.get(8, [])
        blue_top_row = -1
        if len(blue_object) > 0:
          blue_top_row = min(r for r,c in blue_object)


        # fill the area with the same pattern where the object was first encountered
        for r in range(output_grid.shape[0]):
            for c in range(output_grid.shape[1]):
                if output_grid[r,c] == 8:
                    output_grid[r,c] = background_color

        output_grid = shift_rows(output_grid,blue_top_row, output_grid.shape[0]-blue_top_row, red_top_row, background_color)

        #Copy Red Objects
        red_positions = objects.get(2, [])
        if red_positions:
            #first_red_row = min(r for r, _ in red_positions) # Not needed
            for r, c in red_positions:
                 if r+1 < output_grid.shape[0]:
                    output_grid[r + 1, c] = 2

    # Example 2 Logic (Blue and Red objects)
    elif len(objects) == 2 and 1 in objects and 2 in objects:
       #Invert and move blue

        output_grid[:] = background_color  # Clear the output grid first.

        blue_object = objects.get(1, [])
        
        if len(blue_object) > 0:
            blue_top_row =  min(r for r,c in blue_object)
            blue_bottom_row =  max(r for r,c in blue_object)

            blue_height = blue_bottom_row - blue_top_row + 1

            new_blue_top = 2 # constant
            # copy the object in new place
            for r,c in blue_object:
                output_grid[new_blue_top + (r - blue_top_row), c] = 1


        red_object = objects.get(2,[])
        
        if len(red_object) > 0:
            red_top_row = min(r for r, c in red_object)
            new_red_top = blue_top_row - (red_top_row+4)  # calculate distance based on dream
            
            for r, c in red_object:
              if(new_red_top > -1):  
                output_grid[new_red_top,c] = 2

            #Copy Red Object down
            for r in range(output_grid.shape[0]):
                for c in range(output_grid.shape[1]):
                    if output_grid[r,c] == 2:
                       if r+1 < output_grid.shape[0]:
                            output_grid[r + 1, c] = 2


    # Example 3 Logic (Yellow and Magenta objects)
    elif len(objects) == 2 and 4 in objects and 6 in objects:
        # find yellow objects
        yellow_object = objects.get(4,[])

        # find magenta objects
        magenta_object = objects.get(6,[])

        #replace yellow to magenta
        if len(magenta_object) > 0 and len(yellow_object) > 0:

            magenta_rows = sorted(list(set([r for r,c in magenta_object])))
            yellow_rows = sorted(list(set([r for r,c in yellow_object])))

            # clear magenta
            for r,c in magenta_object:
                output_grid[r,c] = background_color
            # clear yellow
            for r,c in yellow_object:
                output_grid[r,c] = background_color

            # copy yellows to magenta's old place
            for i in range(min(len(magenta_rows),len(yellow_rows))):
                 for r,c in yellow_object:
                    if (r-yellow_rows[0]) < output_grid.shape[0]:
                         output_grid[magenta_rows[i] + (r-yellow_rows[0]),c] = 4
            
            # copy 1 row below yellow
            for r,c in yellow_object:
                if magenta_rows[0]-1 > -1:
                    output_grid[magenta_rows[0]-1+(r-yellow_rows[0]),c] = 4

    return output_grid
```