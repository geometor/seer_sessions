import numpy as np

def diff_arrays(grid1, grid2):
    """
    Compares two NumPy arrays and returns details about their differences.
    """
    if grid1.shape != grid2.shape:
        return {"different_shapes": True, "shape1": grid1.shape, "shape2": grid2.shape}

    diff = grid1 != grid2
    diff_indices = np.where(diff)
    num_differences = len(diff_indices[0])

    return {
        "different_shapes": False,
        "num_differences": num_differences,
        "different_values": [(grid1[i, j], grid2[i, j]) for i, j in zip(*diff_indices)],
        "diff_coords": diff_indices
    }

def detect_objects(grid):
    """
    Detects distinct objects in a grid.  An object is a contiguous region of
    non-zero pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:  # Ensure object is not empty
                    min_r = min(coord[0] for coord in obj_coords)
                    max_r = max(coord[0] for coord in obj_coords)
                    min_c = min(coord[1] for coord in obj_coords)
                    max_c = max(coord[1] for coord in obj_coords)
                    width = max_c - min_c + 1
                    height = max_r - min_r + 1
                    objects.append({
                        "color": grid[r, c],
                        "coordinates": obj_coords,
                        "min_row": min_r,
                        "max_row": max_r,
                        "min_col": min_c,
                        "max_col": max_c,
                        "width": width,
                        "height": height
                    })
    return objects

# Example Input and Output grids (replace with actual data)
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 1, 0, 0],
                            [0, 0, 1, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 1, 1],
                            [0, 0, 0, 0, 1, 1],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 0, 0],
                            [0, 0, 0, 1, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]]),
        },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]]),
        }

]

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output_grid = example["output"]

    # current transform
    predicted_output_grid = np.copy(input_grid)

    diff_result = diff_arrays(expected_output_grid, predicted_output_grid)

    input_objects = detect_objects(input_grid)
    expected_output_objects = detect_objects(expected_output_grid)
    predicted_output_objects = detect_objects(predicted_output_grid) #probably don't need

    print(f"Example {i+1}:")
    print(f"  Differences: {diff_result}")
    print(f"  Input Objects: {input_objects}")
    print(f"  Expected Output Objects: {expected_output_objects}")
    print(f"  Predicted Output Objects: {predicted_output_objects}")
    print("-" * 40)
