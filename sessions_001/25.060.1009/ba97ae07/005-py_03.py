import numpy as np

def get_object(grid, color):
    coords = np.where(grid == color)
    if len(coords[0]) == 0:
        return None, None
    min_row, min_col = np.min(coords[0]), np.min(coords[1])
    max_row, max_col = np.max(coords[0]), np.max(coords[1])
    return (min_row, min_col), (max_row, max_col)

def get_objects(grid):
    objects = {}
    for color in np.unique(grid):
        top_left, bottom_right = get_object(grid, color)
        if top_left:  # Ensure object exists
            objects[color] = {
                "top_left": top_left,
                "bottom_right": bottom_right,
                "height": bottom_right[0] - top_left[0] + 1,
                "width": bottom_right[1] - top_left[1] + 1,
            }
    return objects

def report_differences(input_grid, output_grid):
    """
    Reports the differences between the input and output grids, focusing on changed pixels.
    """
    if input_grid.shape != output_grid.shape:
        return "Shapes are different"

    diff = input_grid != output_grid
    diff_indices = np.where(diff)
    differences = []
    for i in range(len(diff_indices[0])):
        row, col = diff_indices[0][i], diff_indices[1][i]
        differences.append(
            {
                "position": (row, col),
                "input_value": input_grid[row, col],
                "output_value": output_grid[row, col],
            }
        )
    return differences
    

# Load the task data - using the first example pair:
task_data = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}
input_grid = np.array(task_data['train'][0]['input'])
output_grid = np.array(task_data['train'][0]['output'])

input_objects = get_objects(input_grid)
output_objects = get_objects(output_grid)
differences = report_differences(input_grid, output_grid)

print("Input Objects:")
for color, details in input_objects.items():
    print(f"  Color {color}: {details}")

print("\nOutput Objects:")
for color, details in output_objects.items():
    print(f"  Color {color}: {details}")
    
print("\nDifferences:")
print(differences)

# Load the task data - second training example:
task_data = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}
input_grid = np.array(task_data['train'][0]['input'])
output_grid = np.array(task_data['train'][0]['output'])

input_objects = get_objects(input_grid)
output_objects = get_objects(output_grid)
differences = report_differences(input_grid, output_grid)

print("Input Objects:")
for color, details in input_objects.items():
    print(f"  Color {color}: {details}")

print("\nOutput Objects:")
for color, details in output_objects.items():
    print(f"  Color {color}: {details}")
    
print("\nDifferences:")
print(differences)

# Load the task data - third training example:
task_data = {
  "train": [
 {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}
input_grid = np.array(task_data['train'][0]['input'])
output_grid = np.array(task_data['train'][0]['output'])

input_objects = get_objects(input_grid)
output_objects = get_objects(output_grid)
differences = report_differences(input_grid, output_grid)

print("Input Objects:")
for color, details in input_objects.items():
    print(f"  Color {color}: {details}")

print("\nOutput Objects:")
for color, details in output_objects.items():
    print(f"  Color {color}: {details}")
    
print("\nDifferences:")
print(differences)