import numpy as np

def get_corner_colors(grid, top_left_row, top_left_col):
    """Extracts the corner colors of a 3x3 region."""
    region = grid[top_left_row:top_left_row + 3, top_left_col:top_left_col + 3]
    corners = []
    if region.shape == (3,3):
        corners = [region[0, 0], region[0, 2], region[2, 0], region[2, 2]] # top-left, top-right, bottom-left, bottom-right
    return corners

def transform(input_grid):
    # Initialize the output grid (4x4)
    output_grid = np.zeros((4, 4), dtype=int)
    input_grid = np.array(input_grid)

    # Get top-left corner colors
    top_left_corners = get_corner_colors(input_grid, 0, 0)
    # print(f"Top left: {top_left_corners}")
    output_grid[0,0] = top_left_corners[0]
    output_grid[1,0] = top_left_corners[0]

    # bottom left corner colors
    bottom_left_corners = get_corner_colors(input_grid, input_grid.shape[0]-3, 0)
    # print(f"Bottom left: {bottom_left_corners}")
    output_grid[2,0] = bottom_left_corners[0]
    output_grid[3,0] = bottom_left_corners[0]


    top_right_corners = get_corner_colors(input_grid, 0, input_grid.shape[1]-3)
    # print(f"top right: {top_right_corners}")
    output_grid[0,3] = top_right_corners[2]
    output_grid[0,1] = top_right_corners[0]

    center_right_corners = get_corner_colors(input_grid, 3, input_grid.shape[1]-3)
    output_grid[1,1] = center_right_corners[0]
    
    mid_right_corners = get_corner_colors(input_grid, 1, input_grid.shape[1]-4)

    output_grid[2,1] = mid_right_corners[2]

    output_grid[1,2] = center_right_corners[2]
    output_grid[2,2] = input_grid[2,2]
    output_grid[3,3] = input_grid[2,2]
    return output_grid

def show_result(example):
    input_grid = example['input']
    output_grid = example['output']
    transformed_grid = transform(input_grid)
    match = np.array_equal(output_grid,transformed_grid)
    print(f"expected:\n{np.array(output_grid)}\n\ntransformed:\n{transformed_grid}\n\nmatch: {match}")

task = {
    "train": [
        {
            "input": [
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 2, 2],
                [3, 3, 3, 8, 8, 8, 2, 2],
                [3, 3, 3, 8, 8, 8, 2, 2],
            ],
            "output": [[3, 8, 0, 8], [3, 8, 0, 0], [3, 0, 0, 0], [3, 2, 0, 2]],
        },
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
            ],
            "output": [[8, 3, 0, 3], [8, 0, 0, 0], [8, 0, 0, 0], [8, 3, 0, 3]],
        },
        {
            "input": [
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [8, 8, 8, 8, 8, 1, 1, 1],
                [8, 8, 8, 8, 8, 1, 1, 1],
                [8, 8, 8, 8, 8, 1, 1, 1],
            ],
            "output": [[4, 1, 0, 1], [4, 0, 0, 0], [8, 0, 0, 0], [8, 1, 0, 1]],
        },
        {
            "input": [
                [7, 7, 7, 0, 0, 0, 0, 0],
                [7, 7, 7, 0, 0, 0, 0, 0],
                [7, 7, 7, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
            ],
            "output": [[7, 0, 0, 0], [0, 5, 0, 5], [0, 5, 0, 5], [0, 5, 0, 5]],
        },
    ],
    "test": [
        {"input": [[6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3]], "output": [[6, 3, 0, 3], [6, 0, 0, 0], [6, 0, 0, 0], [6, 3, 0, 3]]}
    ],
}

for i, example in enumerate(task['train']):
  print(f"Example {i}:")
  show_result(example)
  print("\n")
