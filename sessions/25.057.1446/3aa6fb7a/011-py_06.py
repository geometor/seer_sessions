import numpy as np

# Helper function to find contiguous regions (from original code)
def get_contiguous_region(input_grid, start_r, start_c, visited, target_color):
    rows, cols = input_grid.shape
    region = []
    stack = [(start_r, start_c)]

    while stack:
        r, c = stack.pop()

        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r, c] or input_grid[r, c] != target_color):
            continue

        visited[r, c] = True
        region.append((r, c))

        stack.append((r + 1, c))
        stack.append((r - 1, c))
        stack.append((r, c + 1))
        stack.append((r, c - 1))
    return region

# Function adapted from the given transformation code to gather data:
def analyze_example(input_grid, output_grid):
    rows, cols = input_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    azure_regions_data = []

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8 and not visited[r, c]:
                azure_region = get_contiguous_region(input_grid, r, c, visited, 8)
                
                leftmost_col = min(pixel[1] for pixel in azure_region)
                topmost_row = min(pixel[0] for pixel in azure_region)

                leftmost_pixels = [(row, col) for row, col in azure_region if col == leftmost_col]
                topmost_pixels = [(row,col) for row,col in azure_region if row == topmost_row]
                leftmost_pixel = min(leftmost_pixels)
                topmost_pixel = min(topmost_pixels)

                # check for pixel above the leftmost pixel of region
                above_leftmost = (leftmost_pixel[0] -1, leftmost_pixel[1])
                pixel_above_color = input_grid[above_leftmost] if leftmost_pixel[0] > 0 else None

                # check for pixel to the left of the topmost pixel
                left_of_topmost = (topmost_pixel[0], topmost_pixel[1] -1)
                pixel_left_color = input_grid[left_of_topmost] if topmost_pixel[1] > 0 else None
                
                # determine if the azure region changed to blue
                region_changed = all(output_grid[row, col] == 1 for row, col in azure_region)

                azure_regions_data.append({
                    'region': azure_region,
                    'leftmost_pixel': leftmost_pixel,
                    'topmost_pixel': topmost_pixel,
                    'above_leftmost': above_leftmost,
                    'pixel_above_color': pixel_above_color,
                    'left_of_topmost': left_of_topmost,
                    'pixel_left_color': pixel_left_color,
                    'region_changed': region_changed,
                })

    return azure_regions_data

# Example usage with the third training example (replace with actual data)
example_3_input = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
example_3_output = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

analysis_result = analyze_example(example_3_input, example_3_output)
print(analysis_result)
