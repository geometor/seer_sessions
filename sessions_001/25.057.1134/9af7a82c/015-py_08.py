import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape
    
    input_non_zero_counts = [np.count_nonzero(input_grid[:, j]) for j in range(input_cols)]
    total_non_zero = sum(input_non_zero_counts)

    print(f"Input: {input_rows}x{input_cols}, Output: {output_rows}x{output_cols}")
    print(f"Non-zero counts per input column: {input_non_zero_counts}")
    print(f"Total Non-zero count: {total_non_zero}")
    
    # Verify if the output rows match the sum of non-zero elements
    if output_rows == total_non_zero:
      print("Output rows match sum of non-zero cells in input")
    else:
      print("Output rows DO NOT match sum of non-zero cells")
    
    #verify the column counts match
    if input_cols == output_cols:
        print("Input and Output column counts match")
    else:
        print("Input and Output column counts DO NOT match")

examples = [
    ([[5, 1, 5, 5], [1, 5, 5, 5], [5, 5, 5, 1]], [[5, 1, 5, 5], [1, 5, 5, 5], [5, 5, 5, 1], [0, 5, 5, 0], [0, 0, 0, 0]]),
    ([[1, 0, 0, 8], [0, 0, 0, 0], [0, 0, 0, 0]], [[1, 8]]),
    ([[0, 0, 0, 5, 0], [0, 7, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[7, 5]]),
    ([[6, 0, 9, 0, 6], [0, 0, 0, 0, 0]], [[6, 9, 6]]),
]

for i, (input_grid, output_grid) in enumerate(examples):
  print(f"----- Example {i + 1} -----")
  analyze_example(input_grid, output_grid)