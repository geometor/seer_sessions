import numpy as np
from collections import Counter

def get_dominant_color(grid):
    counts = Counter(grid.flatten())
    if counts:  # Check if counts is not empty
        return counts.most_common(1)[0][0]
    else:
        return None  # Handle empty grid case

def analyze_examples(task):
    for example in task["train"]:
        input_grid = example["input"]
        expected_output = example["output"]
        input_array = np.array(input_grid)
        height, width = input_array.shape

        center_y = height // 2
        center_x = width // 2
        region_size = 3
        start_y = max(0, center_y - region_size // 2)
        start_x = max(0, center_x - region_size // 2)
        end_y = min(height, start_y + region_size)
        end_x = min(width, start_x + region_size)
        central_region = input_array[start_y:end_y, start_x:end_x]

        dominant_color_center = get_dominant_color(central_region)
        dominant_color_full = get_dominant_color(input_array)
        
        actual_output = transform(input_grid) #using existing transform function

        match = np.array_equal(np.array(actual_output), np.array(expected_output))

        print(f"Example:")
        print(f"  Input Dimensions: {height}x{width}")
        print(f"  Central Region:\n{central_region}")
        print(f"  Dominant Color (Center): {dominant_color_center}")
        print(f"  Dominant Color (Full): {dominant_color_full}")
        print(f"  Expected Output:\n{np.array(expected_output)}")
        print(f"  Actual Output:\n{np.array(actual_output)}")
        print(f"  Match: {match}")
        print("-" * 20)

# Assuming 'task' is a global variable containing the ARC task data
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        },
		{
            "input": [[8, 5, 8, 8, 5, 8, 8, 5, 8], [5, 8, 5, 5, 8, 5, 5, 8, 5], [8, 5, 8, 8, 5, 8, 8, 5, 8], [8, 5, 8, 8, 5, 8, 8, 5, 8], [5, 8, 5, 5, 8, 5, 5, 8, 5], [8, 5, 8, 8, 5, 8, 8, 5, 8], [8, 5, 8, 8, 5, 8, 8, 5, 8], [5, 8, 5, 5, 8, 5, 5, 8, 5], [8, 5, 8, 8, 5, 8, 8, 5, 8]],
            "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
        },
        {
            "input": [[2, 0, 2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2, 0, 2]],
            "output": [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]],
            "output": [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
        }
    ]
}
analyze_examples(task)
