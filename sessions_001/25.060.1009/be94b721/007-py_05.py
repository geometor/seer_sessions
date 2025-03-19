import numpy as np

# Example data (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]]),
        "output": np.array([[2]])
    },
     {
        "input": np.array([[1, 1, 1, 1], [1, 2, 2, 1], [1, 1, 1, 1]]),
        "output": np.array([[2, 2]])
    },
      {
        "input": np.array([[1, 1, 1, 1], [1, 2, 2, 1], [1, 2, 2, 1],[1, 1, 1, 1]]),
        "output": np.array([[2, 2],[2,2]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 2, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]),
        "output": np.array([[2]])
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 5, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[]])
    },
    {
        "input" : np.array([[5, 0, 5, 0, 5, 0, 5],
                            [0, 5, 0, 5, 0, 5, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [5, 0, 5, 0, 5, 0, 5],
                            [0, 5, 0, 5, 0, 5, 0]]),
        "output": np.array([[]])
    },
       {
        "input" : np.array([[2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0]]),
        "output": np.array([[2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0],
                            [2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0]])
    }
]

def calculate_area(coords):
    """Calculates the area of an object based on its coordinates."""
    return len(coords)

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def analyze_example(example, example_index):
    input_grid = example['input']
    expected_output = example['output']
    
    # call to the transform function developed in the previous iteration
    actual_output = transform(input_grid)
    
    objects = find_objects(input_grid)
    red_objects = [coords for color, coords in objects if color == 2]
    smallest_red_object = min(red_objects, key=calculate_area, default=None)
    smallest_red_object_area = calculate_area(smallest_red_object) if smallest_red_object else 0
    
    print(f"Example {example_index + 1}:")
    print(f"  Input Grid Shape: {input_grid.shape}")
    print(f"  Expected Output Shape: {expected_output.shape}")
    print(f"  Actual Output Shape: {actual_output.shape}")
    print(f"  Number of Red Objects: {len(red_objects)}")
    print(f"  Smallest Red Object Area: {smallest_red_object_area}")
    print(f"  Expected Output Matches Actual Output: {np.array_equal(actual_output, expected_output)}")    
    print("-" * 40)

for i, example in enumerate(train_examples):
    analyze_example(example, i)
