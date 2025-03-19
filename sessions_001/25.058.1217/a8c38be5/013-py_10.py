def describe_objects(grid):
    """
    Simulates object detection and returns a descriptive string.
    In a real scenario, this would use a modified version of find_objects.
    """
    grid = np.array(grid)
    objects = find_objects(grid)
    descriptions = []
    for color, obj_pixels, orig_row, orig_col in objects:
        min_row, max_row, min_col, max_col = get_object_bounds(obj_pixels)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        descriptions.append(
            f"Color: {color}, Width: {width}, Height: {height}, "
            f"Top-left: ({min_row}, {min_col}), Pixels: {len(obj_pixels)}"
        )
    return ", ".join(descriptions)