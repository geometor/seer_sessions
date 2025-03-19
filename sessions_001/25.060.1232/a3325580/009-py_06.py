import numpy as np

def report(grid, label="Grid"):
    print(f"{label}:\n{grid}")
    print(f"  Shape: {grid.shape}")
    unique, counts = np.unique(grid, return_counts=True)
    print(f"  Unique values: {unique}")
    print(f"  Counts: {counts}")

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    print("--- Example Analysis ---")
    report(input_grid, "Input Grid")
    report(expected_output_grid, "Expected Output Grid")
    report(predicted_output_grid, "Predicted Output Grid")
    print("--- Discrepancies ---")
    if predicted_output_grid.shape == expected_output_grid.shape:
      diff = np.where(predicted_output_grid != expected_output_grid)
      print(f"  Different elements: {len(diff[0])}")
      if (len(diff[0]) > 0):
        print(f"  Input values at differences {input_grid[diff]}")
        print(f"  Expected values at differences {expected_output_grid[diff]}")
        print(f"  Predicted values at differences {predicted_output_grid[diff]}")
    else:
      print("shape mismatch")
    print("\n")
    

# Example grids (replace with actual data from the task)

examples = [
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 4, 0, 0, 0, 0],
                 [0, 0, 0, 4, 4, 4, 0, 0, 0],
                 [0, 0, 0, 0, 4, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 6, 0, 0, 0, 0],
                 [0, 0, 0, 6, 6, 6, 0, 0, 0],
                 [0, 0, 0, 0, 6, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 8, 0, 0, 0, 0],
                 [0, 0, 0, 8, 8, 8, 0, 0, 0],
                 [0, 0, 0, 0, 8, 0, 0, 0, 0]]),
        np.array([[4, 6, 8],
                  [4, 6, 8],
                  [4, 6, 8],
                  [4, 6, 8],
                  [4, 6, 8]]),
      
    ),
        (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 3, 3, 3, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 2, 0, 0, 0],
                  [0, 0, 0, 2, 2, 2, 0, 0],
                  [0, 0, 0, 0, 2, 0, 0, 0]]),
        np.array([[3, 2],
                  [3, 2],
                  [3, 2],
                  [3, 2],
                  [3, 2]]),

    ),
        (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                  [0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
                  [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[5],
                  [5],
                  [5],
                  [5],
                  [5]]),

    ),
    (
         np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 6, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 0, 8, 0]]),
        np.array([[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]),

    )
]
# previous transform implementation - execute it for reporting
def transform(input_grid):
    # Find objects in the input grid.
    objects = get_objects(input_grid)

    # Identify target colors (those that form shapes, not isolated, and don't just have 0 neighbours).
    target_colors = []
    for color, object_list in objects.items():
        for obj_pixels in object_list:
           if not neighbours_only_zero(input_grid,obj_pixels) and not any(is_on_edge(input_grid, cell) for cell in obj_pixels):
                target_colors.append(color)
                break # Go to check next color

    # Remove duplicates and sort to maintain the order found on the first example
    target_colors = sorted(list(set(target_colors)))

    # Construct output grid (5x3).
    output_grid = np.zeros((5, len(target_colors)), dtype=int)

    # Populate columns with target colors.
    for i, color in enumerate(target_colors):
        output_grid[:, i] = color

    return output_grid

for i, (input_grid, expected_output_grid) in enumerate(examples):
    predicted_output_grid = transform(input_grid)
    analyze_example(input_grid, expected_output_grid, predicted_output_grid)
