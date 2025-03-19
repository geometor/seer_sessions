import numpy as np

def examine_example(input_grid, output_grid, predicted_output):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)
    
    input_dims = input_grid.shape
    output_dims = output_grid.shape
    predicted_dims = predicted_output.shape
    
    input_unique_colors = np.unique(input_grid)
    output_unique_colors = np.unique(output_grid)
    predicted_unique_colors = np.unique(predicted_output)
    
    correct = np.array_equal(output_grid, predicted_output)

    print(f"  Input Dims: {input_dims}, Unique Colors: {input_unique_colors}")
    print(f"  Output Dims: {output_dims}, Unique Colors: {output_unique_colors}")
    print(f"  Predicted Dims: {predicted_dims}, Unique Colors: {predicted_unique_colors}")
    print(f"Correct: {correct}")
    print("---")
    

examples = [
    (
        [[3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 0, 0, 0, 0, 0, 0, 0, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3]],
        [[3, 0]]
    ),
    (
        [[8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 5, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 2, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 0, 0, 0, 0, 0, 0, 0, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8]],
        [[8, 0, 5, 2]]
    ),
    (
       [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 4, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 3, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 7, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]],
        [[1, 0, 4, 3, 7]]
    )
]

# the transform function from the prompt
def transform(input_grid):
    """Transforms a 9x9 input grid into a 1x5 output grid by extracting a sequence of colors from the first and last rows."""

    # Initialize the output grid as a 1x5 array filled with zeros (white).
    output_grid = np.zeros((1, 5), dtype=int)

    # Extract the first and last rows of the input grid.
    first_row = input_grid[0, :]
    last_row = input_grid[-1, :]

    # Combine both rows into a single sequence for easier processing.
    combined_rows = np.concatenate((first_row, last_row))

    # Find unique colors in order of appearance.
    unique_colors = []
    for color in combined_rows:
        if color not in unique_colors:
            unique_colors.append(color)

    # Populate the output grid with the unique colors, up to its capacity.
    for i in range(min(len(unique_colors), 5)):
        output_grid[0, i] = unique_colors[i]
        

    return output_grid

for input_grid, output_grid in examples:
    predicted_output = transform(input_grid)
    examine_example(input_grid, output_grid, predicted_output)