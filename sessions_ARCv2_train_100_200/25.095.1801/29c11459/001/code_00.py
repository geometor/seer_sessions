import copy

def find_anchors(row: list[int]) -> list[tuple[int, int]]:
    """
    Finds non-zero elements (anchors) in a row.

    Args:
        row: A list of integers representing a grid row.

    Returns:
        A list of tuples, where each tuple contains (value, column_index)
        for a non-zero element, sorted by column_index.
    """
    anchors = []
    for c, value in enumerate(row):
        if value != 0:
            anchors.append((value, c))
    # Anchors are naturally sorted by column index due to iteration order
    return anchors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling horizontal segments between non-zero 
    numbers ("anchors") based on proximity.

    For each row with two or more anchors:
    1. Identify the non-zero anchors and their positions.
    2. For each segment between adjacent anchors (val1, c1) and (val2, c2):
       - Iterate through the columns 'c' between c1 and c2.
       - Calculate the distance from 'c' to c1 (dist_left) and to c2 (dist_right).
       - If dist_left < dist_right, fill the cell (r, c) with val1.
       - If dist_right < dist_left, fill the cell (r, c) with val2.
       - If dist_left == dist_right, fill the cell (r, c) with 5.
    3. Cells outside these segments and original anchor cells remain unchanged.
    Rows with less than two anchors remain unchanged.
    """
    # Initialize output_grid as a deep copy to preserve original values initially
    output_grid = copy.deepcopy(input_grid)
    midpoint_fill_value = 5

    # Iterate through each row of the input grid
    for r, row in enumerate(input_grid):
        # Find all non-zero numbers ("anchors") in the current row
        anchors = find_anchors(row)

        # Only process rows with two or more anchors
        if len(anchors) >= 2:
            # Iterate through adjacent pairs of anchors
            for i in range(len(anchors) - 1):
                val1, c1 = anchors[i]
                val2, c2 = anchors[i+1]

                # Iterate through the columns strictly between the anchors
                for c in range(c1 + 1, c2):
                    # Calculate distances to the left and right anchors
                    dist_left = c - c1
                    dist_right = c2 - c

                    # Apply the filling logic based on proximity
                    if dist_left < dist_right:
                        output_grid[r][c] = val1
                    elif dist_right < dist_left:
                        output_grid[r][c] = val2
                    else:  # dist_left == dist_right
                        output_grid[r][c] = midpoint_fill_value
            
            # Note: The anchor values themselves are already preserved
            # because we started with a copy and only modified cells *between* them.
            # Zeros outside the segments are also preserved from the copy.

    # Return the completed output grid
    return output_grid