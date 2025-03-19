import numpy as np

def get_largest_black_rectangle(grid):
    """Finds the largest black rectangle in a grid."""
    black_pixels = np.argwhere(grid == 0)
    if len(black_pixels) == 0:
        return None  # No black pixels

    min_row, min_col = black_pixels.min(axis=0)
    max_row, max_col = black_pixels.max(axis=0)

    # Check if it forms a rectangle
    expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)
    actual_size = np.sum(grid[min_row:max_row+1, min_col:max_col+1] == 0)

    if expected_size == actual_size:
        return (min_row, min_col, max_row, max_col)
    else:
      return None

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_dims = input_grid.shape
    output_dims = output_grid.shape

    black_rect = get_largest_black_rectangle(input_grid)

    print(f"Input Dimensions: {input_dims}")
    print(f"Output Dimensions: {output_dims}")
    print(f"Largest Black Rectangle: {black_rect}")

    if black_rect:
        min_row, min_col, max_row, max_col = black_rect
        # check output has same dimensions as largest black rectangle:
        output_rect_shape = (max_row - min_row + 1, max_col - min_col + 1)
        print(f"output shape equals largest black rectangle: {output_dims == output_rect_shape}")

        # check that the reflected input rectangle equals the output
        input_rect = input_grid[min_row:max_row+1, min_col:max_col+1]
        reflected_input_rect = np.flipud(input_rect)

        print(f"Reflected Input Rectangle equals Output: {np.array_equal(reflected_input_rect, output_grid)}")

# Load the example grids (replace with actual loading logic)
task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[6, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 6]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 0, 8, 8, 8]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        },
        {
           "input":  [[6, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 6]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        }
    ]
}


for i, example in enumerate(task_data["train"]):
    print(f"Example {i+1}:")
    analyze_example(np.array(example["input"]), np.array(example["output"]))
    print("-" * 20)