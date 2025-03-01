import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find columns with red pixels
    red_cols = []
    for c in range(cols):
        for r in range(rows):
            if output_grid[r,c] == 2:
                red_cols.append(c)
                break;

    # Fill those columns with red
    for c in red_cols:
        for r in range(rows):
            output_grid[r, c] = 2

    # Iterate through gray pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5:
                # Fill current column with red up to the gray pixel
                for r_above in range(r):
                  output_grid[r_above,c] = 2
                
                #Fill to left with red.
                for c_left in range(c):
                    output_grid[r,c_left] = 2
                
                # Check left and right and fill the columns
                if c > 0:
                    for r_index in range(rows):
                        output_grid[r_index,c-1] = 2

                if c < cols-1:
                    for r_index in range(rows):
                        output_grid[r_index, c+1] = 2


    return output_grid

# Example data (replace with actual data from the task)
examples = [
    (np.array([[0, 0, 0], [0, 5, 0], [0, 2, 0]]), np.array([[2, 2, 2], [2, 5, 2], [2, 2, 2]])),
    (np.array([[0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 2, 0], [0,0,0,0]]), np.array([[2, 2, 2, 2], [2, 2, 5, 2], [2, 2, 2, 2], [2,2,2,2]])),
    (np.array([[0, 0, 0, 0, 0], [0, 0, 0, 5, 0], [0, 2, 0, 0, 0]]), np.array([[2, 2, 2, 2, 2], [2, 2, 2, 5, 2], [2, 2, 2, 2, 2]])),
]

for i, (input_grid, expected_output) in enumerate(examples):
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print("Input:\n", input_grid)
    print("Expected Output:\n", expected_output)
    print("Predicted Output:\n", predicted_output)
    print("Correct:", np.array_equal(predicted_output, expected_output))
    print("-" * 20)