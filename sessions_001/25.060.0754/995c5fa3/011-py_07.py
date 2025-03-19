import numpy as np

def analyze_example(input_grid, output_grid, predicted_output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output_grid = np.array(predicted_output_grid)
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    print(f"Input Dimensions: {input_height}x{input_width}")
    print(f"Output Dimensions: {output_height}x{output_width}")
    print(f"is_correct: {np.array_equal(output_grid, predicted_output_grid)}")

    # Define section boundaries
    sections = [
      ((0, 1), (0, 4)),  # Section 1
      ((0, 1), (4, 9)),  # Section 2
      ((0, 1), (9, 14)), # Section 3
      ((1, 2), (0, 4)),  # Section 4
      ((1, 2), (4, 9)),  # Section 5
      ((1, 2), (9, 14)), # Section 6
      ((2, 4), (0, 4)),  # Section 7
      ((2, 4), (4, 9)),  # Section 8
      ((2, 4), (9, 14))  # Section 9
    ]

    # Process each section
    for i, ((row_start, row_end), (col_start, col_end)) in enumerate(sections):
        section = input_grid[row_start:row_end, col_start:col_end]
        count = 0
        for row in section:
          if 0 in row:
            count +=1
        print(f"section {i+1} count of rows with 0: {count}")

# Provide your example data here
examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[4, 4, 4], [4, 4, 4], [3, 3, 3]],
        [[3, 4, 4], [4, 2, 2], [3, 3, 3]],
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[2, 2, 4], [4, 4, 4], [3, 3, 3]],
        [[4, 4, 4], [4, 2, 2], [3, 3, 3]],
    ),
    (
      [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      [[4, 4, 4], [4, 4, 4], [3, 3, 3]],
      [[4, 4, 4], [4, 4, 4], [3, 3, 3]],
    ),
        (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[2, 2, 4], [4, 4, 4], [3, 3, 3]],
        [[4, 4, 4], [4, 2, 2], [3, 3, 3]],
    ),

]

for input_grid, output_grid, predicted_output_grid in examples:
    analyze_example(input_grid, output_grid, predicted_output_grid)
    print("-" * 20)