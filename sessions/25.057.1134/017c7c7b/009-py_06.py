import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_shape = input_grid.shape
    output_shape = output_grid.shape
    shape_change = (output_shape[0] - input_shape[0], output_shape[1] - input_shape[1])

    unique_input_colors = np.unique(input_grid)
    unique_output_colors = np.unique(output_grid)
    color_changes = {}
    
    for color in unique_input_colors:
        if color not in unique_output_colors:
          # find where this color was in input, and what it is in output
          coords = np.where(input_grid == color)
          first = (coords[0][0], coords[1][0])
          changed_to = output_grid[first]
          color_changes[color] = changed_to
          
        
    print(f"  Input Shape: {input_shape}")
    print(f"  Output Shape: {output_shape}")
    print(f"  Shape Change (rows, cols): {shape_change}")
    print(f"  Unique Input Colors: {unique_input_colors}")
    print(f"  Unique Output Colors: {unique_output_colors}")
    print(f"  Color changes: {color_changes}")
    print("-" * 20)
    return

# Training Examples (from the prompt)
train_examples = [
    (
        [[8, 1, 8, 8, 8], [1, 8, 1, 8, 8], [8, 1, 8, 8, 8]],
        [[8, 2, 8, 8, 8], [2, 8, 2, 8, 8], [8, 2, 8, 8, 8], [8, 2, 8, 8, 8], [2, 8, 2, 8, 8], [8, 2, 8, 8, 8]],
    ),
    (
        [[8, 1, 8, 1, 8], [1, 8, 1, 8, 1], [8, 1, 8, 1, 8]],
        [[8, 2, 8, 2, 8], [2, 8, 2, 8, 2], [8, 2, 8, 2, 8]],
    ),
    (
        [[1, 8, 8, 8, 8], [8, 1, 8, 8, 8], [8, 8, 8, 1, 8], [8, 1, 8, 8, 8]],
        [[2, 8, 8, 8, 8], [8, 2, 8, 8, 8], [8, 8, 8, 2, 8], [8, 2, 8, 8, 8], [2, 8, 8, 8, 8], [8, 2, 8, 8, 8], [8, 8, 8, 2, 8]],
    ),
    (
        [[0, 0, 0, 0, 0, 1, 8, 8, 8], [0, 0, 0, 0, 0, 8, 1, 8, 8], [0, 0, 0, 0, 0, 8, 8, 1, 8]],
        [[0, 0, 0, 0, 0, 2, 8, 8, 8], [0, 0, 0, 0, 0, 8, 2, 8, 8], [0, 0, 0, 0, 0, 8, 8, 2, 8]],
    ),
    (
      [[8, 8, 8, 8, 1],
       [8, 8, 8, 1, 8],
       [8, 8, 1, 8, 8],
       [8, 1, 8, 8, 8],
       [1, 8, 8, 8, 8]],

      [[8, 8, 8, 8, 2],
       [8, 8, 8, 2, 8],
       [8, 8, 2, 8, 8],
       [8, 2, 8, 8, 8],
       [2, 8, 8, 8, 8]]
    )
]
#previous transform function
def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Replace all blue (1) pixels with red (2)
    output_grid[output_grid == 1] = 2
    
    # Get dimensions of original grid
    rows, cols = output_grid.shape
    
    # Create the extension rows as numpy array.  The existing output_grid establishes
    # the checkerboard pattern, so just duplicate a slice.
    extension = np.copy(output_grid[0:3,:])
    
    # Vertically stack to add to bottom
    output_grid = np.vstack((output_grid, extension))

    return output_grid

for i, (input_grid, output_grid) in enumerate(train_examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    predicted = transform(input_grid)
    print(f"  Predicted Output shape: {predicted.shape}")    
    if not np.array_equal(predicted, output_grid):
        print(f"  Mismatch: Predicted output does NOT match expected output.")
    else:
        print("Match")
