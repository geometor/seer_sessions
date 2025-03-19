def get_green_region_coords(grid):
    """Returns the coordinates of all green pixels in the grid."""
    return np.argwhere(grid == 3).tolist()

def get_pixel(grid, row, col):
    """Safely gets the pixel value at the given coordinates, handling out-of-bounds cases."""
    if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
        return grid[row, col]
    else:
        return None

for i, (input_grid, output_grid) in enumerate(task["train"]):
    input_np = np.array(input_grid['input'])
    output_np = np.array(input_grid['output'])
    green_pixels_input = get_green_region_coords(input_np)
    green_pixels_output = get_green_region_coords(output_np)

    print(f"Example {i+1}:")
    print(f"  Input Green Pixels: {green_pixels_input}")
    print(f"  Output Green Pixels: {green_pixels_output}")

    cross_center = find_cross_center(input_np)
    print(f" cross center {cross_center}")
    if cross_center is not None:
        row, col = cross_center
        print(f" value at cross center {get_pixel(input_np, row, col)}")