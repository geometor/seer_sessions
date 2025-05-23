def get_object_data(grid):
    """
    Identifies contiguous horizontal lines as simplified objects.
    Returns a list of objects, with position and size.
    """
    objects = []
    for row_idx, row in enumerate(grid):
        current_object = []
        for col_idx, pixel in enumerate(row):
            if not current_object:
                current_object.append((col_idx, pixel))
            elif pixel == current_object[-1][1]:  # Same color, extend the object
                current_object.append((col_idx, pixel))
            else:  # Different color, end the object
                if len(current_object) > 0:
                    objects.append({
                        'row': row_idx,
                        'start_col': current_object[0][0],
                        'end_col': current_object[-1][0],
                        'color': current_object[0][1],  # Color of the object
                        'length': len(current_object)
                    })
                current_object = [(col_idx, pixel)]
        # Handle any object that extends to the end of the row
        if len(current_object) > 0:
            objects.append({
                'row': row_idx,
                'start_col': current_object[0][0],
                'end_col': current_object[-1][0],
                'color': current_object[0][1],
                'length': len(current_object)
            })
    return objects

def grid_differences(grid1, grid2):
    """
    Compares two grids and returns a list of differences.
    """
    if len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        return "Grids have different dimensions"
    diffs = []

    for i in range(len(grid1)):
        for j in range(len(grid1[0])):
            if grid1[i][j] != grid2[i][j]:
                diffs.append(f"Pixel mismatch at ({i},{j}): {grid1[i][j]} vs {grid2[i][j]}")
    return diffs
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0]],
        }
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 6, 6, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        }
    ]
}

def revised_get_object_data(grid):
    """Identifies contiguous horizontal *and* vertical lines."""
    objects = []

    # Detect horizontal lines
    for row_idx, row in enumerate(grid):
        current_object = []
        for col_idx, pixel in enumerate(row):
            if pixel != 0:  # Consider only non-background pixels
                if not current_object:
                    current_object.append((col_idx, pixel))
                elif pixel == current_object[-1][1]:
                    current_object.append((col_idx, pixel))
                else:
                    if len(current_object) > 0:
                        objects.append({
                            'type': 'horizontal',
                            'row': row_idx,
                            'start_col': current_object[0][0],
                            'end_col': current_object[-1][0],
                            'color': current_object[0][1],
                            'length': len(current_object)
                        })
                    current_object = [(col_idx, pixel)]
            elif current_object: #end the object if it hits background
                objects.append({
                    'type': 'horizontal',
                    'row': row_idx,
                    'start_col': current_object[0][0],
                    'end_col': current_object[-1][0],
                    'color': current_object[0][1],
                    'length': len(current_object)
                    })
                current_object = []
        if current_object:
            objects.append({
                'type': 'horizontal',
                'row': row_idx,
                'start_col': current_object[0][0],
                'end_col': current_object[-1][0],
                'color': current_object[0][1],
                'length': len(current_object)
            })


    # Detect vertical lines
    for col_idx in range(len(grid[0])):
        current_object = []
        for row_idx, row in enumerate(grid):
            pixel = row[col_idx]
            if pixel != 0:  # Consider only non-background pixels
                if not current_object:
                    current_object.append((row_idx, pixel))
                elif pixel == current_object[-1][1]:
                    current_object.append((row_idx, pixel))
                else:
                    if len(current_object) > 0:
                        objects.append({
                            'type': 'vertical',
                            'col': col_idx,
                            'start_row': current_object[0][0],
                            'end_row': current_object[-1][0],
                            'color': current_object[0][1],
                            'length': len(current_object)
                        })
                    current_object = [(row_idx, pixel)]
            elif current_object:
                objects.append({
                            'type': 'vertical',
                            'col': col_idx,
                            'start_row': current_object[0][0],
                            'end_row': current_object[-1][0],
                            'color': current_object[0][1],
                            'length': len(current_object)
                        })
                current_object = []

        if current_object:
            objects.append({
                        'type': 'vertical',
                        'col': col_idx,
                        'start_row': current_object[0][0],
                        'end_row': current_object[-1][0],
                        'color': current_object[0][1],
                        'length': len(current_object)
                    })

    return objects



for example in task["train"]:
    input_grid = example['input']
    output_grid = example['output']
    input_objects = revised_get_object_data(input_grid)
    output_objects = revised_get_object_data(output_grid)
    print(f"Example Input Objects: {input_objects}")
    print(f"Example Output Objects: {output_objects}")
    print("---")
