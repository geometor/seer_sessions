import numpy as np
from scipy.ndimage import label, find_objects

COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

OUTPUT_COLOR_MAPPING = {
    1: 8,  # blue -> azure
    2: 9,  # red -> maroon
    3: 7,  # green -> orange
    4: 6,  # yellow -> magenta
}

def get_connected_regions(grid):
    """
    Finds connected regions (blobs) of the same color, excluding gray and white.
    Returns a list of bounding box tuples: (row_start, row_end, col_start, col_end, color)
    """
    filtered_grid = np.where((grid != 5) & (grid != 0), grid, 0)
    labeled_grid, num_labels = label(filtered_grid)
    regions = find_objects(labeled_grid)

    region_data = []
    for i, region_slice in enumerate(regions):
        if region_slice is not None:
            row_start, row_end = region_slice[0].start, region_slice[0].stop
            col_start, col_end = region_slice[1].start, region_slice[1].stop
            # Extract a representative color from the region (assuming homogeneity)
            color = grid[row_start, col_start]
            region_data.append((row_start, row_end, col_start, col_end, color))

    return region_data

def transform(input_grid):
    # Initialize output_grid with white background
    output_grid = np.full_like(input_grid, 0)

    # Preserve the gray line
    output_grid[3, :] = input_grid[3, :]

    # Get connected regions
    regions = get_connected_regions(input_grid)

    # Transform each region
    for row_start, row_end, col_start, col_end, color in regions:
        output_color = OUTPUT_COLOR_MAPPING.get(color)
        if output_color:
            output_grid[row_start:row_end, col_start:col_end] = output_color

    return output_grid

def calculate_accuracy(predicted_grid, expected_grid):
    return np.all(predicted_grid == expected_grid)

def test_transform(task_data):
    all_correct=True
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)
        if not calculate_accuracy(predicted_output, expected_output):
            all_correct = False
            print("Incorrect Example:")
            print("Input:\n", input_grid)
            print("Expected Output:\n", expected_output)
            print("Predicted Output:\n", predicted_output)
            print("-" * 20)
    if all_correct: print("all correct")

# Example usage (replace with actual task data)
# test_transform(task)
