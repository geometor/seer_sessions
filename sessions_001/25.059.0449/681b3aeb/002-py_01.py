"""
1.  **Identify Colored Objects:** Scan the input grid and identify all contiguous blocks of non-zero (non-white) pixels. Each such block constitutes a distinct "colored object."

2.  **Extract Objects:** Extract each identified colored object. Note their color (numerical value) and their shape (though shape seems to be discarded in the final output, only the order of colors, vertically and then horizontally).

3.  **Arrange in Output:** Take the first non zero color on the first row, add it to the output grid. Move to the next non zero color and add that to the output grid, continue for the whole first row. Then perform the same operation with the next rows.

4. **Output**: return the resulting smaller grid.
"""

import numpy as np

def get_objects(grid):
    """
    Identify and extract non-zero colored objects from the input grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != 0 and (r, c) not in visited:
                color = grid[r,c]
                objects.append(color)
                visited.add((r,c))

    return objects
                

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Identify the colored objects
    objects = get_objects(input_grid)
    
    # Determine output grid size
    num_objects = len(objects)
    output_size = int(np.ceil(np.sqrt(num_objects)))
    
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # arrange objects in output grid.
    k=0
    for i in range(output_size):
        for j in range(output_size):
           if k < num_objects:
              output_grid[i,j] = objects[k]
              k+=1


    return output_grid.tolist()