def describe_grid(grid, objects=None, highlight=None):
    """
    Provides a string representation of the grid.
    Optionally highlights specified cells.
    """
    desc = ""
    for r in range(grid.shape[0]):
        row_desc = ""
        for c in range(grid.shape[1]):
            cell_value = grid[r, c]
            if objects:
                is_object = False
                for obj in objects:
                    if (r,c) in obj:
                        is_object=True
                        break

                if is_object:
                    row_desc += f"[{cell_value}]"  # Highlight object
                else:
                    row_desc += f" {cell_value} "
            
            elif highlight and (r, c) in highlight:
                row_desc += f"*{cell_value}*"  # Highlight specific cell
            else:
                row_desc += f" {cell_value} "
        desc += row_desc.strip() + "\n"
    return desc

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a list of mismatched coordinates.
    """
    mismatches = []
    if grid1.shape != grid2.shape:
        return "Shapes are different"
    else:
        for r in range(grid1.shape[0]):
            for c in range(grid1.shape[1]):
                if grid1[r,c] != grid2[r,c]:
                    mismatches.append((r,c))
    return mismatches
examples = task_data['train']

for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    actual_output_grid = transform(input_grid.copy())  # Use a copy to avoid modifying the original
    mismatches = compare_grids(expected_output_grid, actual_output_grid)
    
    print(f"Example {i + 1}:")
    print("Input Grid:")
    input_objects = get_objects(input_grid)
    print(describe_grid(input_grid, input_objects))
    print("Expected Output Grid:")
    print(describe_grid(expected_output_grid))    
    print("Actual Output Grid:")    
    print(describe_grid(actual_output_grid))
    print("Mismatches:")
    print(mismatches)    
    print("-" * 20)