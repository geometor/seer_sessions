import numpy as np

def find_objects(grid, color):
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return []  # Return empty list if no objects of specified color
    # Group contiguous pixels into objects
    objects = []
    visited = set()
    for x, y in coords:
        if (x, y) not in visited:
            object_coords = []
            stack = [(x, y)]
            while stack:
                curr_x, curr_y = stack.pop()
                if (curr_x, curr_y) in visited:
                    continue
                visited.add((curr_x, curr_y))
                object_coords.append((curr_x, curr_y))
                # Check adjacent pixels (up, down, left, right)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_x, new_y = curr_x + dx, curr_y + dy
                    if (0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1] and
                            grid[new_x, new_y] == color and (new_x, new_y) not in visited):
                        stack.append((new_x, new_y))
            objects.append(object_coords)
    return objects
def get_object_extents(obj):
    """returns xmin, xmax, ymin, ymax"""
    xmin = min(x for x, y in obj)
    xmax = max(x for x, y in obj)
    ymin = min(y for x, y in obj)
    ymax = max(y for x, y in obj)
    return xmin, xmax, ymin, ymax

def analyze_grid(grid, grid_label):
    print(f"Analyzing {grid_label}:")
    azure_objects = find_objects(grid, 8)
    yellow_objects = find_objects(grid, 4)
    print(f"  Number of Azure (8) objects: {len(azure_objects)}")
    for i, obj in enumerate(azure_objects):
        xmin, xmax, ymin, ymax = get_object_extents(obj)
        print(f"    Azure Object {i+1}: Size=({xmax - xmin + 1}x{ymax-ymin+1}), Extents=[({xmin},{ymin})-({xmax},{ymax})]")
    print(f"  Number of Yellow (4) objects: {len(yellow_objects)}")
    for i, obj in enumerate(yellow_objects):
        xmin, xmax, ymin, ymax = get_object_extents(obj)
        print(f" Yellow Object {i + 1}: Size=({xmax-xmin+1}x{ymax-ymin+1}), Extents=[({xmin},{ymin})-({xmax},{ymax})]")

# Example Usage with the provided grids:
# Replace these with actual input, output, and result grids from each example

task_examples = [
  {
      "input": np.array([[4, 0, 0, 8, 8, 8, 8, 8, 8], [4, 0, 0, 8, 8, 8, 8, 8, 8], [4, 0, 0, 8, 8, 8, 8, 8, 8], [4, 0, 0, 0, 0, 0, 0, 0, 0]]),
      "output": np.array([[4, 0, 0, 0, 0, 0, 8, 8, 8], [4, 0, 0, 0, 0, 0, 8, 8, 8], [4, 0, 0, 0, 0, 0, 8, 8, 8], [4, 0, 0, 0, 0, 0, 0, 0, 0]]),
      "result": np.array([[4, 0, 0, 0, 0, 0, 0, 0, 8], [4, 0, 0, 0, 0, 0, 0, 0, 8], [4, 0, 0, 0, 0, 0, 0, 0, 8], [4, 0, 0, 0, 0, 0, 0, 0, 0]])
  },
    {
      "input": np.array([[0, 0, 0, 0, 0, 0, 8, 8, 0], [0, 0, 0, 0, 0, 0, 8, 8, 0], [0, 0, 0, 0, 0, 0, 8, 8, 0], [8, 8, 0, 0, 0, 0, 0, 0, 0], [8, 8, 0, 0, 0, 0, 0, 0, 0]]),
      "output": np.array([[0, 0, 0, 0, 0, 0, 8, 8, 0], [0, 0, 0, 0, 0, 0, 8, 8, 0], [0, 0, 0, 0, 0, 0, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
      "result": np.array([[0, 0, 0, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])

  },
    {
      "input": np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8]]),
      "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0]]),
      "result": np.array([[8, 8, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 8, 8]])
  }
]

for example in task_examples:
    analyze_grid(example["input"], "Input Grid")
    analyze_grid(example["output"], "Output Grid")
    analyze_grid(example["result"], "Result Grid")
    print("-" * 30)