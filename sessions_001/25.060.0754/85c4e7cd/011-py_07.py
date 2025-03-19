import numpy as np
from io import StringIO

# Function to analyze a single example
def analyze_example(input_grid_str, output_grid_str):
    input_grid = np.loadtxt(StringIO(input_grid_str), dtype=int)
    output_grid = np.loadtxt(StringIO(output_grid_str), dtype=int)

    input_red_count = np.sum(input_grid == 2)
    input_magenta_count = np.sum(input_grid == 6)
    output_red_count = np.sum(output_grid == 2)
    output_magenta_count = np.sum(output_grid == 6)

    return {
        'input_red_count': int(input_red_count),
        'input_magenta_count': int(input_magenta_count),
        'output_red_count': int(output_red_count),
        'output_magenta_count': int(output_magenta_count),
    }

# Example data (replace with actual data from the prompt)
examples = [
    (
        """
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 6
8 8 8 8 8 8 8 8 6 6
8 8 8 8 8 8 8 6 6 6
8 8 8 8 8 8 6 6 6 6
8 8 8 8 8 6 6 6 6 6
""",
        """
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 8 8 8 2 2
8 8 8 8 8 8 8 2 2 2
8 8 8 8 8 8 2 2 2 2
8 8 8 8 8 2 2 2 2 2
"""
    ),
     (
        """
1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
1 6 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
""",
        """
1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
"""
    ),
   (
        """
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 6 0 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
""",
        """
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 0 6 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
"""
    )
]

# Analyze all examples
results = [analyze_example(in_grid, out_grid) for in_grid, out_grid in examples]

# Print the results
print(results)