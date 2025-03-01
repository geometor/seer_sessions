import numpy as np
from io import StringIO

def calculate_center(grid):
    """Calculates the center coordinates of a grid."""
    height, width = grid.shape
    center_y = (height - 1) / 2
    center_x = (width - 1) / 2
    return center_y, center_x

def grid_from_string(s):
    """Converts a grid string representation to a NumPy array."""
    return np.loadtxt(StringIO(s), dtype=int, delimiter=' ')
    
# Example data (replace with actual data from the prompt)

examples = [
    {
        "input": """
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
""",
        "output": """
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
""",
        "result": """
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
"""
    },
      {
        "input": """
0 0 0 0 0 0
0 0 0 0 0 0
0 0 2 2 0 0
0 0 0 0 0 0
""",
        "output": """
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 2 2 0 0
""",
        "result": """
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 2 0 0
"""
    },
    {
        "input": """
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 0
0 2 0 0 0 0 0 0
""",
        "output": """
0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
""",
        "result": """
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0
0 0 0 0 2 0 0 0
"""
    },

        {
        "input": """
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 2 0 0
0 0 2 0 0 0
""",
        "output": """
0 0 2 0 0 0
0 0 0 2 0 0
0 0 0 0 0 0
0 0 0 0 0 0
""",
        "result": """
0 0 0 0 0 0
0 0 0 0 2 0
0 0 0 0 0 0
0 0 0 0 0 0
"""
    },
]


for i, example in enumerate(examples):
    input_grid = grid_from_string(example["input"])
    output_grid = grid_from_string(example["output"])
    result_grid = grid_from_string(example["result"])
    input_center = calculate_center(input_grid)
    output_center = calculate_center(output_grid)
    result_center = calculate_center(result_grid)
    input_red_pixels = np.argwhere(input_grid == 2)
    output_red_pixels = np.argwhere(output_grid == 2)
    result_red_pixels = np.argwhere(result_grid == 2)

    print(f"Example {i+1}:")
    print(f"  Input Grid Center: {input_center}")
    print(f"  Output Grid Center: {output_center}")
    print(f"  Input Red Pixels: {input_red_pixels}")
    print(f"  Output Red Pixels: {output_red_pixels}")
    print(f"  Result Red Pixels: {result_red_pixels}")
    if len(input_red_pixels) > 0 and len(output_red_pixels) > 0:
        input_red_avg = np.mean(input_red_pixels, axis=0)
        output_red_avg = np.mean(output_red_pixels, axis=0)
        print(f"Red Pixel Movement (Input Avg -> Output Avg, dy, dx): {output_red_avg - input_red_avg}")

    print("-" * 20)
