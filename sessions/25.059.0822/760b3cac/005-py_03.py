import numpy as np

def get_vertical_stacks(grid, color):
    """
    Finds contiguous vertical stacks of a specified color.

    Args:
        grid: The input grid.
        color: The color to search for.

    Returns:
        A list of tuples, where each tuple contains (start_row, start_col, height).
    """
    stacks = []
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                height = 0
                for r2 in range(r, rows):
                    if grid[r2, c] == color:
                        height += 1
                        visited.add((r2, c))
                    else:
                        break
                if height > 0:
                  stacks.append((r, c, height))
    return stacks

def find_all_pixels(grid, color):
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color:
                pixels.append((r,c))
    return pixels

def analyze_example(input_grid, output_grid):
    input_azure_stacks = get_vertical_stacks(input_grid, 8)
    output_azure_stacks = get_vertical_stacks(output_grid, 8)
    
    input_all_azure = find_all_pixels(input_grid,8)
    output_all_azure = find_all_pixels(output_grid, 8)

    input_yellow_pixels = find_all_pixels(input_grid, 4)
    output_yellow_pixels = find_all_pixels(output_grid, 4)

    input_white_pixels = find_all_pixels(input_grid, 0)
    output_white_pixels = find_all_pixels(output_grid, 0)

    print("Input Azure Stacks:", input_azure_stacks)
    print("Output Azure Stacks:", output_azure_stacks)
    print("Input All Azure:", input_all_azure)
    print("Output All Azure:", output_all_azure)
    print("Input Yellow Pixels:", input_yellow_pixels)
    print("Output Yellow Pixels:", output_yellow_pixels)
    print("Input White Pixels", input_white_pixels)
    print("Output White Pixels", output_white_pixels)
    print("-" * 20)
    
# Load the training examples
train = [
    ([
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 8, 4, 4, 4, 4, 4],
        [4, 4, 4, 8, 4, 4, 4, 4, 4],
        [4, 4, 4, 8, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4]
    ],
    [
        [8, 8, 8, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]),

    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8]
    ],
    [
        [8, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),

    ([
        [0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0],
        [0, 0, 8, 0, 0, 0, 0, 0, 0]
    ],
    [
        [8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
        ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 4, 4, 4, 4, 0, 0],
        [0, 0, 4, 4, 4, 4, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 0, 0]
    ],
    [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 4, 4, 4, 4, 0, 0],
        [0, 0, 4, 4, 4, 4, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
]

# Analyze each example
for i, (input_grid, output_grid) in enumerate(train):
    print(f"Example {i+1}:")
    analyze_example(np.array(input_grid), np.array(output_grid))