import numpy as np

def find_vertical_red_blocks(grid):
    rows = len(grid)
    cols = len(grid[0])
    red_blocks = []
    for r in range(rows - 1):
        for c in range(cols):
            if grid[r][c] == 2 and grid[r+1][c] == 2:
                red_blocks.append((r, c))
    return red_blocks

def code_execution(input_grid, output_grid, expected_output_grid):

    # 1. Correct Output
    correct_output = np.array_equal(output_grid, expected_output_grid)

    # 2. Red Block Locations
    red_block_locations = find_vertical_red_blocks(input_grid)
    
    # 3. Red Blocks in 3rd and 4th Row
    red_blocks_in_rows_3_4 = any(r in [2, 3] for r, _ in red_block_locations)

    print(f"  Correct Output: {correct_output}")
    print(f"  Red Block Locations (Input): {red_block_locations}")
    print(f"  Red Blocks Exist in Rows 3 and 4: {red_blocks_in_rows_3_4}")

# Example Usage (replace with actual grids from the task)
task_data = [
    {
        'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    },
    {
        'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 2, 0, 0, 2, 0, 0]],
        'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 2, 0, 0, 2, 0, 0]],
    },
    {
        'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0]],
    },
]
for i, grids in enumerate(task_data):
    input_grid = np.array(grids['input'])
    expected_output_grid = np.array(grids['output'])
    output_grid = transform(input_grid)
    print(f"Example {i + 1}:")
    code_execution(input_grid, output_grid, expected_output_grid)

del task_data