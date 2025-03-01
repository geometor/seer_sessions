def analyze_expansion(input_grid, output_grid):
    """
    Analyzes which colors expand horizontally from input to output,
    and checks if any expansion actually occurred.

    Args:
        input_grid: The input grid (2D numpy array).
        output_grid: The output grid (2D numpy array).

    Returns:
        A tuple containing:
            - A dictionary: {color: [row indices where expansion occurred]}.
            - A boolean: True if any expansion was detected, False otherwise.
    """
    expansion_data = {}
    expansion_detected = False

    for row_index, (input_row, output_row) in enumerate(zip(input_grid, output_grid)):
        for col_index, input_color in enumerate(input_row):
            if col_index + 1 < len(input_row):  # Check if there's a pixel to the right
                if all(output_row[col_index+1:] == input_color):
                    if input_color not in expansion_data:
                        expansion_data[input_color] = []
                    expansion_data[input_color].append(row_index)
                    expansion_detected = True

    return expansion_data, expansion_detected


# Example usage with the provided training examples (assuming they are loaded as numpy arrays)
# replace with actual grids
example_grids = [
    (np.array([[0,0,0],[0,1,0],[0,0,0]]),np.array([[0,0,0],[1,1,1],[0,0,0]])),
    (np.array([[5,0,5],[0,5,0],[5,0,5]]),np.array([[5,5,5],[0,5,0],[5,5,5]])),
    (np.array([[8,8,8],[8,0,8],[8,8,8]]),np.array([[8,8,8],[8,0,8],[8,8,8]]))
    ]

results = [analyze_expansion(inp, out) for inp, out in example_grids]
print(results)