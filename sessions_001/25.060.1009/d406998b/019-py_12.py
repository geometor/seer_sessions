import numpy as np
from collections import Counter

def analyze_grid(grid):
    """
    Analyzes a single grid and provides information about objects and colors.
    """
    objects = get_objects(grid)
    object_colors = [grid[list(obj)[0]] for obj in objects]  # Color of each object
    color_counts = Counter(grid.flatten())
    rectangle_objects = [obj for obj in objects if is_rectangle(obj)]
    rectangle_colors = [grid[list(obj)[0]] for obj in rectangle_objects]
    
    return {
        "objects": objects,
        "object_colors": object_colors,
        "color_counts": color_counts,
        "rectangle_objects": rectangle_objects,
        "rectangle_colors": rectangle_colors,
        "grid_shape": grid.shape
    }

def color_diff(input_grid, output_grid):
    """
    Compare colors present in input and output
    """
    input_colors = set(input_grid.flatten())
    output_colors = set(output_grid.flatten())

    only_in_input = input_colors - output_colors
    only_in_output = output_colors - input_colors
    return only_in_input, only_in_output

# Example Usage (assuming the previous functions 'get_objects' and 'is_rectangle' are defined)

task_data = [
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3]]),
        "result": "success" # Assuming the previous code's result for this example
    },
     {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3]]),
        "result": "success"
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]),
        "result": "failure"
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]),
        "result": "failure"
    }
]

for i, example in enumerate(task_data):
    input_analysis = analyze_grid(example["input"])
    output_analysis = analyze_grid(example["output"])
    only_in_input, only_in_output = color_diff(example["input"], example["output"])

    print(f"Example {i+1}:")
    print(f"  Input Grid Shape: {input_analysis['grid_shape']}")
    print(f"  Input Colors: {input_analysis['color_counts']}")
    print(f"  Rectangle Colors (Input): {input_analysis['rectangle_colors']}")
    print(f"  Output Colors: {output_analysis['color_counts']}")
    print(f"  Rectangle Colors (Output): {output_analysis['rectangle_colors']}")
    print(f"  Colors only in Input: {only_in_input}")
    print(f"  Colors only in Output: {only_in_output}")
    print(f"  Result: {example['result']}")
    print("-" * 20)
