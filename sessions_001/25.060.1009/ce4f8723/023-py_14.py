import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    print("Input Shape:", input_grid.shape)
    print("Output Shape:", output_grid.shape)

    print("Input Colors:", np.unique(input_grid))
    print("Output Colors:", np.unique(output_grid))

    diff = (input_grid != output_grid)
    print("Number of Different Pixels:", np.sum(diff))
    print("Difference Grid (1 indicates a change):\n", diff.astype(int))

# Example Usage (using the provided example data)
example1_input = [[0, 0, 1, 1, 1, 0, 1],[0, 0, 0, 1, 1, 0, 1],[0, 0, 0, 1, 1, 1, 1],[4, 4, 4, 4, 4, 4, 4],[2, 2, 2, 2, 2, 2, 2],[2, 2, 2, 0, 2, 2, 2],[2, 2, 2, 2, 0, 2, 2]]
example1_output =  [[0, 0, 3, 3, 3, 0, 3],[0, 0, 0, 3, 3, 0, 3],[0, 0, 0, 3, 3, 3, 3],[3, 3, 3, 3, 3, 3, 3]]
analyze_example(example1_input, example1_output)

example2_input = [[0, 0, 1, 1, 1, 0, 1],[0, 0, 0, 1, 1, 0, 1],[0, 0, 0, 1, 1, 1, 1],[4, 4, 4, 4, 4, 4, 4],[2, 2, 2, 2, 2, 2, 2],[2, 2, 2, 0, 2, 2, 2],[2, 2, 2, 2, 0, 2, 2],[4,4,4,4,4,4,4],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
example2_output =  [[0, 0, 3, 3, 3, 0, 3],[0, 0, 0, 3, 3, 0, 3],[0, 0, 0, 3, 3, 3, 3],[3, 3, 3, 3, 3, 3, 3]]

analyze_example(example2_input, example2_output)

example3_input = [[0, 0, 1, 1, 1, 0, 1],[0, 0, 0, 1, 1, 0, 1],[0, 0, 0, 1, 1, 1, 1],[4, 4, 4, 4, 4, 4, 4],[2, 2, 2, 2, 2, 2, 2],[2, 2, 2, 0, 2, 2, 2],[2, 2, 2, 2, 0, 2, 2],[4,4,4,4,4,4,4],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,2,2,0,2,2,2],[0,0,0,0,0,0,0]]
example3_output =  [[0, 0, 3, 3, 3, 0, 3],[0, 0, 0, 3, 3, 0, 3],[0, 0, 0, 3, 3, 3, 3],[3, 3, 3, 3, 3, 3, 3]]
analyze_example(example3_input, example3_output)