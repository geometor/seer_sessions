import numpy as np
from typing import List, Tuple, Dict, Any

COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

def find_pixel(grid_np: np.ndarray, color: int) -> Tuple[int, int] | None:
    """Finds the location of a pixel of the given color.  Assumes only one exists."""
    locations = np.argwhere(grid_np == color)
    if len(locations) > 0:
        return locations[0]  # Return the first location found
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """Transforms the input grid according to the observed rules."""

    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_np = input_np.copy() # start with a copy, to preserve the azure pixel

    # 1. Identify Azure and 2. Target Row
    azure_location = find_pixel(input_np, 8)
    if azure_location is None:
        return output_np.tolist() # No azure pixel, return input unchanged

    target_row = azure_location[0]

    # 3. Fill with Black (and implicitly 4. Preserve Azure)
    for c in range(cols):
        output_np[target_row, c] = 0

    return output_np.tolist()

def process_examples(task: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Processes examples to generate metrics and results."""

    results = []
    for example in task["train"]:
        input_grid = example["input"]
        expected_output_grid = example["output"]
        input_np = np.array(input_grid)
        transformed_grid = transform(input_grid)
        transformed_np = np.array(transformed_grid)
        azure_location = find_pixel(input_np, 8)

        example_data = {
            "input_grid": input_grid,
            "expected_output_grid": expected_output_grid,
            "transformed_grid": transformed_grid,
            "azure_location": azure_location.tolist() if azure_location is not None else None,
            "correct": transformed_grid == expected_output_grid
        }
        results.append(example_data)
    return results

# create an ARC task dictionary to demonstrate use
task = {
    "train": [
        {
            "input": [[0, 1, 2, 3, 8]],
            "output": [[0, 0, 0, 0, 8]]
        },
         {
            "input": [[0, 0, 8, 1, 2]],
            "output": [[0, 0, 8, 1, 2]]
        },
        {
            "input": [[8, 1, 2, 3, 0]],
            "output": [[8, 1, 2, 3, 0]]
        },
        {
            "input": [[0, 8, 2, 3, 0]],
            "output": [[0, 8, 2, 3, 0]]
        }
    ]
}
example_metrics = process_examples(task)

# Print the results in a readable way
for i, example_data in enumerate(example_metrics):
  print(f"Example {i+1}:")
  print(f"  Input Grid: {example_data['input_grid']}")
  print(f"  Expected Output Grid: {example_data['expected_output_grid']}")
  print(f"  Transformed Grid: {example_data['transformed_grid']}")
  print(f"  Azure Location: {example_data['azure_location']}")
  print(f"  Correct: {example_data['correct']}")
  print("-" * 20)
