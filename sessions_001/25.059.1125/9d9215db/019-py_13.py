import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify non-zero pixels
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((r, c, input_grid[r, c]))

    # 2 & 3. Iterate and create 3x3 blocks.
    for r, c, color in non_zero_pixels:
        # create the bounds for the 3x3 block
        min_row = max(0, r - 1)
        max_row = min(rows, r + 2)
        min_col = max(0, c - 1)
        max_col = min(cols, c + 2)

        for block_r in range(min_row, max_row):
          for block_c in range(min_col, max_col):
            output_grid[block_r, block_c] = color

    # 4, 5, & 6. Extend horizontal lines and copy original pixels.
    for r, c, color in non_zero_pixels:
        output_grid[r, c] = color  # Ensure original pixel is copied

        # Extend right
        for c_right in range(c + 1, cols):
          stop = False
          for i in range(-1,2):
            check_row = r + i
            if 0 <= check_row < rows and output_grid[check_row, c_right] != 0:
                stop = True
                break
          if stop:
            break
          else:
            output_grid[r, c_right] = color
        
        # Extend left
        for c_left in range(c - 2, -1, -1): # start from c-2 because c-1 to c+1 is handled by block
            stop = False
            for i in range(-1,2):
              check_row = r + i
              if 0 <= check_row < rows and output_grid[check_row, c_left] != 0:
                  stop=True
                  break
            if stop:
                break
            else:

              output_grid[r, c_left] = color

    return output_grid

# Example data (replace with your actual task data)
task_data = {
    "train": [
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        },
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        },
        {
           "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        },
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        },
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 4, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [7, 7, 7, 7, 7, 7, 7, 7, 7],
                               [4, 4, 4, 4, 4, 4, 4, 4, 4],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        }
    ]
}

for example in task_data['train']:
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)
    print("Input:\n", input_grid)
    print("Expected Output:\n", expected_output)
    print("Actual Output:\n", actual_output)
    print("-" * 20)