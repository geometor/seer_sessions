import numpy as np

def analyze_example(input_grid, output_grid):
    input_non_zero = np.count_nonzero(input_grid)
    output_non_zero = np.count_nonzero(output_grid)
    input_non_zero_positions = np.transpose(np.nonzero(input_grid))
    output_non_zero_positions = np.transpose(np.nonzero(output_grid))
    input_colors = [input_grid[pos[0], pos[1]] for pos in input_non_zero_positions]
    output_colors = [output_grid[pos[0], pos[1]] for pos in output_non_zero_positions]

    return {
        "input_non_zero_count": input_non_zero,
        "output_non_zero_count": output_non_zero,
        "input_non_zero_positions": input_non_zero_positions.tolist(),
        "output_non_zero_positions": output_non_zero_positions.tolist(),
        "input_colors": input_colors,
        "output_colors": output_colors,

    }

examples = [
    # Example 1 (Correct)
    (np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]]), np.array([[2, 0, 0], [0, 0, 0], [0, 0, 0]])),
    # Example 2 (Incorrect)
    (np.array([[0, 0, 0], [0, 6, 0], [0, 0, 0]]), np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]])),
    # Example 3 (Incorrect)
    (np.array([[0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 0, 0], [8, 0, 0, 0]]), np.array([[0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0], [2, 0, 0, 0]])),
]

reports = []
for i, (input_grid, output_grid) in enumerate(examples):
     reports.append(analyze_example(input_grid, output_grid))
     print(f"--- Example {i+1} ---")
     print(reports[-1])