import numpy as np

def code_execution(input_grid, expected_output, predicted_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = np.array(predicted_output)

    input_shape = input_grid.shape
    output_shape = expected_output.shape
    predicted_shape = predicted_output.shape

    # Find the 2x2 yellow (4) core in the input grid.
    input_core = find_core(input_grid) if find_core(input_grid) is not None else "Not Found"
    expected_core = find_core(expected_output) if find_core(expected_output) is not None else "Not Found"
    predicted_core = find_core(predicted_output) if find_core(predicted_output) is not None else "Not Found"
   
    # Check if prediction matches the expected output
    match = np.array_equal(expected_output, predicted_output)

    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "predicted_shape": predicted_shape,
        "input_core": input_core,
        "expected_core": expected_core,
        "predicted_core": predicted_core,
        "match": match
    }

def find_core(grid):
    # Find the 2x2 yellow (4) core in the input grid.  Assumes it exists and is unique.
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 4 and grid[r + 1, c] == 4 and grid[r, c + 1] == 4 and grid[r + 1, c + 1] == 4:
                return (r, c)
    return None
# Previous Code:
#
# ```python
# """
# Expands a 2x2 core of an input grid to 4x4 and then mirrors/duplicates the input's rows and columns to create a 6x6 output grid.
# """
#
# import numpy as np
#
# def find_core(grid):
#     # Find the 2x2 yellow (4) core in the input grid.  Assumes it exists and is unique.
#     rows, cols = grid.shape
#     for r in range(rows - 1):
#         for c in range(cols - 1):
#             if grid[r, c] == 4 and grid[r + 1, c] == 4 and grid[r, c + 1] == 4 and grid[r + 1, c + 1] == 4:
#                 return (r, c)
#
# def transform(input_grid):
#     # initialize output_grid
#     output_grid = np.zeros((6, 6), dtype=int)
#
#     # Find the 2x2 core
#     core_row, core_col = find_core(input_grid)
#
#     # Expand Core: Place the 2x2 core into the center of the output grid, making it 4x4.
#     output_grid[1:5, 1:5] = 4
#
#     # Mirror/Duplicate Columns:
#     #   - input_grid[:,0] becomes the 1th column
#     #   - input_grid[:,0] becomes the last column
#     output_grid[1:5,0] = input_grid[0: , 0]
#     output_grid[1:5,5] = input_grid[0: , 0]
#
#     # Mirror/Duplicate rows
#     #   - copy extended last row of input grid, including new columns
#     #      and duplicate it into the last row of output
#     #   - mirror extended first row, including new columns and make it first row of output.
#
#     output_grid[5, 1:5] = input_grid[2,:]
#     output_grid[5,0] = input_grid[2,0]
#     output_grid[5,5] = input_grid[2,0]
#
#     output_grid[0, 1:5] = input_grid[0,:]
#     output_grid[0,0] = input_grid[0,0]
#     output_grid[0,5] = input_grid[0,0]
#
#     return output_grid
# ```
#

examples = [
    (
        [[8, 8, 3, 3, 8, 8], [8, 8, 3, 3, 8, 8], [5, 5, 4, 4, 6, 6], [5, 5, 4, 4, 6, 6], [1, 1, 3, 3, 2, 2], [1, 1, 3, 3, 2, 2]],
        [[8, 8, 3, 3, 8, 8], [8, 8, 3, 3, 8, 8], [5, 5, 4, 4, 6, 6], [5, 5, 4, 4, 6, 6], [1, 1, 3, 3, 2, 2], [1, 1, 3, 3, 2, 2]]
    ),
    (
        [[8, 3, 3, 8, 8, 8], [5, 4, 4, 6, 6, 6], [5, 4, 4, 6, 6, 6], [1, 3, 3, 2, 2, 2]],
        [[8, 3, 3, 8, 8, 8], [5, 4, 4, 6, 6, 6], [5, 4, 4, 6, 6, 6], [1, 3, 3, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 8, 0, 3, 8], [8, 5, 5, 4, 4], [0, 5, 5, 4, 4], [3, 1, 1, 3, 2], [8, 0, 0, 0, 8]],
        [[8, 8, 3, 8, 8, 8], [5, 5, 4, 4, 6, 6], [5, 5, 4, 4, 6, 6], [1, 1, 3, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    ),
        (
        [[3, 8, 8, 8], [4, 4, 6, 6], [4, 4, 6, 6], [3, 2, 2, 2]],
        [[3, 8, 8, 8], [4, 4, 6, 6], [4, 4, 6, 6], [3, 2, 2, 2]]
    )
]

results = []
for input_grid, expected_output in examples:
    predicted_output = transform(np.array(input_grid))
    results.append(code_execution(input_grid, expected_output, predicted_output))
    
for i, result in enumerate(results):
    print(f"Example {i+1}:")
    for key, value in result.items():
        print(f"  {key}: {value}")