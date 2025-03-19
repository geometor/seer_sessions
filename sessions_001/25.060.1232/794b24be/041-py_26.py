import numpy as np

# Function to analyze a single example pair
def analyze_example(input_grid, output_grid):
    changed_pixels = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != output_grid[i, j]:
                changed_pixels.append(
                    {
                        "row": i,
                        "col": j,
                        "input_color": int(input_grid[i, j]),
                        "output_color": int(output_grid[i, j]),
                    }
                )
    return changed_pixels

# provided example grids for train set

example_grids = [
    { # Example 1
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 1, 5, 5, 5, 5],
                           [5, 5, 5, 5, 1, 5, 5, 5, 5],
                           [5, 5, 5, 5, 1, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 2, 5, 5, 5, 5],
                            [5, 5, 5, 5, 2, 5, 5, 5, 5],
                            [5, 5, 5, 5, 2, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    },
     { # Example 2
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 1, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 2, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
     { # Example 3
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 2, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },
]

# Analyze all examples
analysis_results = [analyze_example(eg["input"], eg["output"]) for eg in example_grids]

for i, result in enumerate(analysis_results):
    print(f"Example {i+1} Changed Pixels: {result}")
