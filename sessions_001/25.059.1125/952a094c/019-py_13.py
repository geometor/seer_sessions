import numpy as np

def find_border(grid):
    # Find the coordinates of the blue border (color 1).
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:  # No blue border found.
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def find_inner_objects(grid, border):
    # Find the positions and colors of inner objects within the border.
    min_row, max_row, min_col, max_col = border
    inner_objects = []
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r, c] != 0 and grid[r, c] != 1:  # Not white and not blue.
                inner_objects.append(((r, c), grid[r, c]))
    return inner_objects

def mirror_position(pos, border):
    # Calculate mirrored position within the border.
    min_row, max_row, min_col, max_col = border
    row_center = (min_row + max_row) / 2
    col_center = (min_col + max_col) / 2
    mirrored_row = int(2 * row_center - pos[0])
    mirrored_col = int(2 * col_center - pos[1])
    return (mirrored_row, mirrored_col)
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the blue border.
    border = find_border(output_grid)
    if border is None:
        return output_grid  # No border found, return original grid.

    # Find inner objects.
    inner_objects = find_inner_objects(output_grid, border)

    # Place inner objects at their mirrored positions.  Do NOT clear original position
    for (row, col), color in inner_objects:
        mirrored_pos = mirror_position((row, col), border)
        #Copy the color value to mirrored position, without clearing original
        output_grid[mirrored_pos] = color
    
    return output_grid

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_border = find_border(input_grid)
    output_border = find_border(output_grid)
    
    
    transformed_grid = transform(input_grid)
    
    print(f"Input Border: {input_border}")
    print(f"Output Border: {output_border}")
    print(f"Correct Transformation: {np.array_equal(transformed_grid, output_grid)}")
    print(f"Transformed Grid:\n {transformed_grid}")

# Example Data (Replace with your actual example data)
examples = [
  (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 3, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 3, 1, 0, 0, 0],
            [0, 0, 0, 1, 3, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
 (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0]],
        
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 5, 5, 5, 5, 5, 0],
         [0, 5, 5, 5, 5, 5, 0],
         [0, 5, 5, 5, 5, 5, 0],
         [0, 5, 5, 5, 5, 5, 0],
         [0, 5, 5, 5, 5, 5, 0],
         [0, 0, 0, 0, 0, 0, 0]]
    )
]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("-" * 30)