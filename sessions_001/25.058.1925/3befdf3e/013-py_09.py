import numpy as np

def describe_grid(grid):
    """Provides a textual description of a grid."""
    unique, counts = np.unique(grid, return_counts=True)
    description = ""
    for color, count in zip(unique, counts):
        description += f"Color {color}: {count} pixels, "
    description += f"Shape: {grid.shape}"
    return description

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and its prediction."""

    print("Input Grid:")
    print(describe_grid(input_grid))
    print(input_grid)

    print("\nExpected Output Grid:")
    print(describe_grid(output_grid))
    print(output_grid)

    print("\nPredicted Output Grid:")
    print(describe_grid(predicted_grid))
    print(predicted_grid)

    # Find red square in input
    red_min_row, red_max_row, red_min_col, red_max_col = find_object(input_grid, 2)
    if red_min_row is not None:
        red_size = (red_max_row - red_min_row + 1, red_max_col - red_min_col + 1)
        print(f"\nRed Square in Input: Top-left=({red_min_row},{red_min_col}), Size={red_size}")
    else:
      print("\nNo Red Square Found")

    #Find orange
    orange_min_row, orange_max_row, orange_min_col, orange_max_col = find_object(input_grid, 7)
    if orange_min_row is not None:
        print(f"Orange Pixel in Input: ({orange_min_row},{orange_min_col})")
    else:
       print("\nNo Orange Pixel Found")

    # Find red square in the expected output
    red_min_row_out, red_max_row_out, red_min_col_out, red_max_col_out = find_object(output_grid, 2)
    if red_min_row_out is not None:
        red_size_out = (red_max_row_out - red_min_row_out + 1, red_max_col_out - red_min_col_out + 1)
        print(f"\nRed Square in Expected Output: Top-left=({red_min_row_out},{red_min_col_out}), Size={red_size_out}")
    else:
        print("\nNo Red Square in Output")

    #Find orange
    orange_min_row_out, orange_max_row_out, orange_min_col_out, orange_max_col_out = find_object(output_grid, 7)
    if orange_min_row_out is not None:
      orange_size = (orange_max_row_out - orange_min_row_out + 1, orange_max_col_out - orange_min_col_out + 1)
      print(f"Orange object in Output: Top-left=({orange_min_row_out}, {orange_min_col_out}), Size: {orange_size}")

    else:
       print("\nNo Orange Pixel Found in Output")
    print("-" * 40)

task = "db3e9e28"

train_input_0 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 7, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_output_0 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 7, 2, 7, 2, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_input_1 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 7, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_output_1 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 7, 2, 7, 2, 2, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_input_2 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 5, 5, 5, 5, 5], [5, 5, 5, 2, 7, 2, 5, 5, 5, 5], [5, 5, 5, 2, 2, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_output_2 = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 5, 5, 5, 5, 5], [5, 5, 5, 2, 7, 2, 7, 2, 5, 5], [5, 5, 5, 2, 2, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])

predicted_output_0 = transform(train_input_0)
predicted_output_1 = transform(train_input_1)
predicted_output_2 = transform(train_input_2)

analyze_example(train_input_0, train_output_0, predicted_output_0)
analyze_example(train_input_1, train_output_1, predicted_output_1)
analyze_example(train_input_2, train_output_2, predicted_output_2)
