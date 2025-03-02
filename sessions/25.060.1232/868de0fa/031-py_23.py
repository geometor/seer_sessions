import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(output_grid)
    print("Predicted Output Grid:")
    print(predicted_grid)
    
    input_blue_shapes = find_shapes(input_grid, 1)
    output_blue_shapes = find_shapes(output_grid, 1)

    print(f"Number of input blue shapes: {len(input_blue_shapes)}")
    print(f"Number of output blue shapes: {len(output_blue_shapes)}")


    correct = np.array_equal(output_grid, predicted_grid)
    print(f"Correct prediction?: {correct}")

    if not correct:
        diff = output_grid != predicted_grid
        print("Difference:")
        print(diff.astype(int)) # show differences as 0 and 1
        
        # Check fill colors in the *output* grid within blue shapes
        if len(output_blue_shapes) > 0 :
          for shape in output_blue_shapes:
            min_x = min(x for x, y in shape)
            max_x = max(x for x, y in shape)
            min_y = min(y for x, y in shape)
            max_y = max(y for x, y in shape)
            
            fill_colors = set()
            for x in range(min_x + 1, max_x):
              for y in range(min_y+1, max_y):
                if output_grid[x,y] != 1:
                    fill_colors.add(output_grid[x,y])

            print(f"Fill colors within output shape: {fill_colors}")

# Example Usage (replace with actual grids)
# Assuming 'transform' function is defined as in the provided code

examples = [
    # Example 0
  (np.array([[0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 7, 7, 7, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0]]),
  "Example 0"
  ),

    # Example 1
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
      "Example 1"
    ),

        # Example 2
    (
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
        ]),
        np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 7, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
        ]),
      "Example 2"
    ),
]


for input_grid, output_grid, label in examples:
    predicted_grid = transform(input_grid)
    print(f"--- {label} ---")
    analyze_example(input_grid, output_grid, predicted_grid)
    print("\n")
