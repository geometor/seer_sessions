def find_internal_color_and_count(grid, bounding_box):
    """Finds the non-background, non-yellow color and counts its occurrences within a bounding box."""
    min_r, min_c, max_r, max_c = bounding_box
    internal_color = None
    count = 0
    found_coords = []

    # First pass: find the color (assuming only one non-yellow/white color type per bbox)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            color = grid[r, c]
            if color != 0 and color != 4:
                internal_color = color
                break # Found the color type
        if internal_color is not None:
            break

    if internal_color is None:
        return None, 0 # No internal color found

    # Second pass: count occurrences of that specific color
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] == internal_color:
                count += 1
                found_coords.append((r, c))


    # print(f"Found internal color {internal_color} at {found_coords}, count={count}") # Debug print
    return internal_color, count
