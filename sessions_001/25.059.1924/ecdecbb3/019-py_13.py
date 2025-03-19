def check_solution(index, input_grid, expected_output, generated_output):
    """Checks the solution against the expected output and prints relevant information."""
    print(f"Example {index}:")

    if np.array_equal(generated_output, expected_output):
        print("  Result: Correct")
    else:
        print("  Result: Incorrect")
        print("  Differences:")
        diff = generated_output != expected_output
        diff_coords = np.where(diff)
        for r, c in zip(diff_coords[0], diff_coords[1]):
            print(
                f"    ({r}, {c}): Expected {expected_output[r, c]}, Got {generated_output[r, c]}"
            )

    print("  Input Grid:")
    print(input_grid)
    print("  Expected Output:")
    print(expected_output)
    print("  Generated Output:")
    print(generated_output)

    # red columns
    red_cols = get_red_pixel_columns(input_grid)
    print(f"  Red Columns: {red_cols}")

    # azure rows
    azure_lines = get_azure_lines(input_grid)
    print(f"  Azure Lines: {azure_lines}")

    # azure pixels in generated output
    azure_pixels = np.where(generated_output == 8)
    if len(azure_pixels[0]) > 0:
      print(f"  Azure pixels at: {list(zip(azure_pixels[0], azure_pixels[1]))}")
    else:
      print("  No azure pixels found in generated output")

    print("-" * 20)

def get_red_pixel_columns(input_grid):
    """Finds the columns containing red pixels."""
    red_cols = []
    for col in range(input_grid.shape[1]):
        for row in range(input_grid.shape[0]):
            if input_grid[row, col] == 2:
                red_cols.append(col)
                break  # Move to the next column after finding a red pixel
    return red_cols

def get_azure_lines(input_grid):
    """Finds the rows containing azure lines."""
    azure_rows = []
    for row in range(input_grid.shape[0]):
        if all(input_grid[row, :] == 8):
            azure_rows.append(row)
    return azure_rows

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Red Pixel Column Extension
    red_columns = get_red_pixel_columns(input_grid)
    for col in red_columns:
        for row in range(rows):
            output_grid[row, col] = 2

    # 2. Azure Line Identification
    azure_lines = get_azure_lines(input_grid)

    # 3. Azure Pixel Placement, with Red Column Interaction
    for azure_row in azure_lines:
        azure_pixel_placed = False  # Flag to track if an azure pixel has been placed for the current line
        for col in range(cols):
          if col not in red_columns:
            output_grid[azure_row, col] = 8
            azure_pixel_placed = True
            break # only place one azure pixel per line, then exit

    return output_grid

# Example usage (replace with actual task data)
task_data = [
    (
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 2],
                  [8, 8, 8, 8, 8, 8, 8, 8, 2]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [8, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2]])
    ),
    (
        np.array([[8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 2],
                  [8, 8, 8, 8, 8, 2]]),
        np.array([[0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 2],
                  [8, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 2]])
    ),
    (
        np.array([[8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8],
                  [8, 8, 8, 2, 8],
                  [8, 8, 8, 2, 8],
                  [8, 8, 8, 8, 8]]),
        np.array([[0, 0, 0, 2, 0],
                  [8, 0, 0, 2, 0],
                  [0, 0, 0, 2, 0],
                  [0, 0, 0, 2, 0],
                  [0, 0, 0, 0, 0]])
    ),
        (
        np.array([[8, 8, 8, 8],
                  [8, 8, 8, 2],
                  [8, 8, 8, 8],
                  [8, 8, 8, 2]]),
        np.array([[8, 0, 0, 2],
                  [0, 0, 0, 2],
                  [0, 0, 0, 2],
                  [0, 0, 0, 2]])
    )
]

for i, (input_grid, expected_output) in enumerate(task_data):
    generated_output = transform(input_grid)
    check_solution(i + 1, input_grid, expected_output, generated_output)