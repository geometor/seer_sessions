import numpy as np

# Provided code (slightly modified for reporting)
def get_leftmost_nonzero(row):
    """Finds the leftmost non-zero element in a row."""
    for pixel in row:
        if pixel != 0:
            return pixel
    return 0

def transform(input_grid):
    output_grid = np.copy(input_grid)
    special_row_index = 1
    special_row = input_grid[special_row_index]
    replacement_color = get_leftmost_nonzero(special_row)
    output_grid[special_row_index] = np.full(len(special_row), replacement_color)
    return output_grid

# Input grids (from the prompt - manually transcribed)
train_inputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[8, 8, 8, 8, 8, 8, 8, 8],
              [8, 0, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[6, 0, 6, 0, 6, 0, 6, 0],
              [0, 6, 0, 6, 0, 6, 0, 6],
              [6, 0, 6, 0, 6, 0, 6, 0],
              [0, 6, 0, 6, 0, 6, 0, 6]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 8, 8, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]])
]

train_outputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[6, 0, 6, 0, 6, 0, 6, 0],
              [6, 6, 6, 6, 6, 6, 6, 6],
              [6, 0, 6, 0, 6, 0, 6, 0],
              [0, 6, 0, 6, 0, 6, 0, 6]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 8, 8, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]])
]

for i, (input_grid, expected_output) in enumerate(zip(train_inputs, train_outputs)):
    predicted_output = transform(input_grid)
    special_row_index = 1
    special_row = input_grid[special_row_index]
    replacement_color = get_leftmost_nonzero(special_row)
    is_correct = np.array_equal(predicted_output, expected_output)
    print(f"Example {i}:")
    print(f"  Special Row Index (assumed): {special_row_index}")
    print(f"  Replacement Color (assumed): {replacement_color}")
    print(f"  Correct Prediction: {is_correct}")
    if not is_correct:
        # find correct special_row_index
        for j in range(len(input_grid)):
            if not np.array_equal(input_grid[j], expected_output[j]):
                print(f"  Corrected Special Row Index: {j}")
                row = input_grid[j]
                for pixel in row:
                    if not np.all(expected_output[j] == pixel):
                        continue
                    else:
                        print(f" Corrected Replacement color {pixel}")
                        break
                break

    print("-" * 20)