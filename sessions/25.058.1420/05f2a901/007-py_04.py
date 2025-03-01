def transform(input_grid, example_index): # Added example_index
    output_grid = input_grid.copy()

    red_coords = find_object(input_grid, 2)
    azure_coords = find_object(input_grid, 8)

    for r, c in red_coords:
        output_grid[r, c] = 0

    if len(red_coords) > 0 and len(azure_coords) > 0:
        red_bbox = get_bounding_box(red_coords)
        azure_bbox = get_bounding_box(azure_coords)
        azure_br_row, azure_br_col = azure_bbox[2], azure_bbox[3]
        red_height = red_bbox[2] - red_bbox[0] + 1
        red_width = red_bbox[3] - red_bbox[1] + 1

        print(f"Example {example_index}:")
        print(f"  Red BBox: {red_bbox},  Azure BBox: {azure_bbox}")

        is_inside = all(is_inside_bounding_box((r,c), red_bbox) for r, c in azure_coords)
        print(f"  Azure inside Red: {is_inside}")

        if is_inside:
            center_row_shift = azure_br_row - (red_height // 2) - red_bbox[0]
            center_col_shift = azure_br_col - (red_width // 2) - red_bbox[1]
            print(f"  Inside Shift: ({center_row_shift}, {center_col_shift})")
            
            for r, c in red_coords:
                new_row = r + center_row_shift
                new_col = c + center_col_shift
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                     output_grid[new_row, new_col] = 2

        else:
            row_shift = azure_br_row - red_bbox[0]
            col_shift = azure_br_col - red_bbox[3]
            print(f"  Outside Shift: ({row_shift}, {col_shift})")
            
            for r, c in red_coords:
                new_row = r + row_shift
                new_col = c + col_shift
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                    output_grid[new_row, new_col] = 2
    return output_grid