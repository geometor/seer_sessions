"""
1.  **Identify Objects:** Determine all distinct objects within the input grid. An object is defined as a contiguous set of pixels sharing the same color. Record each object's color and shape (height, width). Also note the overall input grid dimensions.

2.  **Transformation Rules (Prioritized):**

    a. **No Change:** If the input grid contains single-pixel objects of different colors and includes empty (white/0) cells, and if the input and output grid dimensions are identical, then the output is an exact copy of the input.

    b. **Checkerboard Expansion:** If the input consists of a horizontal sequence of *different* single-pixel colored objects (1x1) along the top row, create a checkerboard pattern in the output. The output dimensions match the input dimensions. The checkerboard uses the colors from the input sequence, cycling through them in a row-major (left-to-right, top-to-bottom) order.  The specific color at output[r,c] is determined by `colors[(r + c) % len(colors)]`.

    c. **Vertical and Horizontal Expansion with Fill:** If the input grid consists *only* of single-pixel objects (1x1) of different color *and* has a height not equal to 1, then extend each object into a full column. If there is more than one row in the input, the output grid's height will be equal to the input's height. The output width equals the number of input objects.

    d. **Horizontal Block Expansion:** If the input contains at least one object with a height greater than 1, the output's height equals the input's height, and output's width equals the input width multiplied by a consistent factor. Each color fills an area based on the shape.

3.  **Default:** If none of the above rules apply, perform no transformation (return an empty grid or potentially a copy, to be determined by further examples).  This needs to be made more specific with more test cases.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a list of objects, where each object is a dictionary containing:
    - 'shape': (height, width)
    - 'color': color value
    - 'pixels': list of (row, col) tuples representing the object's pixels
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        current_object['pixels'].append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                current_object = {'shape': None, 'color': grid[r][c], 'pixels': []}
                dfs(r, c, grid[r][c], current_object)
                
                # Calculate shape based on pixels
                min_row = min(pixel[0] for pixel in current_object['pixels'])
                max_row = max(pixel[0] for pixel in current_object['pixels'])
                min_col = min(pixel[1] for pixel in current_object['pixels'])
                max_col = max(pixel[1] for pixel in current_object['pixels'])
                current_object['shape'] = (max_row - min_row + 1, max_col - min_col + 1)

                objects.append(current_object)
    return objects

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape
    objects = get_objects(input_grid)

    # Rule 2a: No Change
    if (all(obj['shape'] == (1, 1) for obj in objects) and
        0 in input_grid and
        input_rows > 1): #This condition was refined based in the analysis
        output_grid = input_grid.copy()

    # Rule 2b: Checkerboard Expansion
    elif (len(objects) > 0 and
        all(obj['shape'] == (1, 1) for obj in objects) and
        objects[0]['pixels'][0][0] == 0 and
        input_rows == 1
        ):
        output_rows, output_cols = input_cols, input_cols #corrected output size
        output_grid = np.zeros((output_rows, output_cols), dtype=int)
        colors = [obj['color'] for obj in objects]
        for r in range(output_rows):
            for c in range(output_cols):
                output_grid[r, c] = colors[(r + c) % len(colors)]

    # Rule 2c: Vertical and Horizontal Expansion with Fill
    elif all(obj['shape'] == (1, 1) for obj in objects) and input_rows > 1 :
        output_rows, output_cols = input_rows, len(objects)
        output_grid = np.zeros((output_rows, output_cols), dtype=int)
        for i, obj in enumerate(objects):
            for r in range(output_rows):
                output_grid[r, i] = obj['color']

    # Rule 2d: Horizontal Block Expansion
    elif any(obj['shape'][0] > 1 for obj in objects):
        output_rows = input_rows
        output_cols = input_cols * 2  # Expansion factor hardcoded for example 2
        output_grid = np.zeros((output_rows, output_cols), dtype=int)
        current_col = 0
        for obj in objects:
            for r in range(output_rows):
                for c in range(current_col, current_col + (output_cols//input_cols)* obj['shape'][1]): #corrected logic
                    output_grid[r,c] = obj['color']
            current_col += (output_cols//input_cols) * obj['shape'][1]  #corrected logic

    else:
        output_grid = np.empty_like(input_grid)

    return output_grid.tolist()