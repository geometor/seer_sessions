"""
The transformation rule is as follows:

1.  Locate each azure (8) L-shaped object.
2.  For each one, identify the top-left corner cell.
3.  Change the color of the cell immediately to the right of each identified top-left corner to blue (1).
4.  Keep every other cell in its original state.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Adds a blue (1) pixel to the right of the top-left corner of each azure (8) L-shape.
    """
    input_array = np.array(input_grid)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # Iterate through the grid to find L-shapes
    for i in range(rows):
        for j in range(cols):
            if input_array[i, j] == 8:
                # Check for top-left corner of L-shape (rotated and original)
                if i + 1 < rows and j + 1 < cols:
                    #check for original L shape
                    if input_array[i+1,j] == 8 and input_array[i+1, j+1] == 8:
                         # Found top-left corner, add blue pixel to the right
                        if j + 2 < cols:
                            output_array[i, j+1] = 1
                    #check for rotated L shape
                    elif input_array[i, j+1] == 8 and input_array[i-1, j+1] == 8: #rotated
                        if j + 2 < cols:
                            output_array[i,j+1] = 1



    return output_array.tolist()


if __name__ == '__main__':

    input = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0],
        [0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    expected_output = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 1, 0, 0, 0, 0],
        [0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 1, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

    output = transform(input)

    if output == expected_output:
        print("SUCCESS!\n")
    else:
        print("FAILED!\n")
        print("Expected Output:", expected_output)
        print("Transformed Output:", output)

    print()
    assert output == expected_output, "Transformed output does not match expected output."