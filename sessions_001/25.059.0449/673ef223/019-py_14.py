def compare_grids(grid1, grid2):
    """Compares two grids and returns a list of mismatched pixels."""
    mismatches = []
    rows, cols = grid1.shape
    for r in range(rows):
        for c in range(cols):
            if grid1[r, c] != grid2[r, c]:
                mismatches.append(((r, c), grid1[r, c], grid2[r, c]))
    return mismatches

def analyze_example(input_grid, output_grid, result_grid):
    """Analyzes an example and returns a dictionary of metrics."""
    analysis = {}

    # Initial Azure
    initial_azure = find_pixels(input_grid, 8)
    analysis['initial_azure_count'] = len(initial_azure)
    analysis['initial_azure_loc'] = initial_azure

    # Expected Azure
    expected_azure = find_pixels(output_grid, 8)
    analysis['expected_azure_count'] = len(expected_azure)
    analysis['expected_azure_loc'] = expected_azure

    # Result Azure
    result_azure = find_pixels(result_grid, 8)
    analysis['result_azure_count'] = len(result_azure)
    analysis['result_azure_loc'] = result_azure

    # Initial Yellow
    initial_yellow = find_pixels(input_grid, 4)
    analysis['initial_yellow_count'] = len(initial_yellow)
    analysis['initial_yellow_loc'] = initial_yellow

    # Expected Yellow
    expected_yellow = find_pixels(output_grid, 4)
    analysis['expected_yellow_count'] = len(expected_yellow)
    analysis['expected_yellow_loc'] = expected_yellow
    
    # Result Yellow
    result_yellow = find_pixels(result_grid, 4)
    analysis['result_yellow_count'] = len(result_yellow)
    analysis['result_yellow_loc'] = result_yellow
    

    # Mismatches
    mismatches = compare_grids(output_grid, result_grid)
    analysis['mismatched_count'] = len(mismatches)
    analysis['mismatched_pixels'] = mismatches

    return analysis

# Example usage (assuming input_grid, output_grid, and result_grid are defined)
# analysis = analyze_example(input_grid, output_grid, result_grid)
# print(analysis)