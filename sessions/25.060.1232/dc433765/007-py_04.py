# Assume this is a placeholder for actual code execution
# In a real environment, this would involve running the `transform` function
# and numpy operations on each input/output pair.

def analyze_example(input_grid, output_grid, example_num):
    import numpy as np

    def find_object_extents(grid, color):
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            return None, None, None, None  # No object found
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        
        # get object shape for reporting
        obj_pixels = []
        for row, col in coords:
            obj_pixels.append((row,col))

        return min_row, min_col, height, width, obj_pixels

    def calculate_center(grid):
        rows, cols = grid.shape
        return rows // 2, cols // 2

    input_green = find_object_extents(input_grid, 3)
    input_yellow = find_object_extents(input_grid, 4)
    output_green = find_object_extents(output_grid, 3)
    output_yellow = find_object_extents(output_grid, 4)

    center_row, center_col = calculate_center(input_grid)  # input/output dimensions are same

    print(f"Example {example_num}:")
    print(f"  Input Green: TopLeft={input_green[0:2] if input_green[0] is not None else None}, Size={input_green[2:4] if input_green[0] is not None else None} Pixels={input_green[4] if input_green[0] is not None else None}")
    print(f"  Input Yellow: TopLeft={input_yellow[0:2] if input_yellow[0] is not None else None}, Size={input_yellow[2:4] if input_yellow[0] is not None else None} Pixels={input_yellow[4] if input_yellow[0] is not None else None}")
    print(f"  Output Green: TopLeft={output_green[0:2] if output_green[0] is not None else None}, Size={output_green[2:4] if output_green[0] is not None else None} Pixels={output_green[4] if output_green[0] is not None else None}")
    print(f"  Output Yellow: TopLeft={output_yellow[0:2] if output_yellow[0] is not None else None}, Size={output_yellow[2:4] if output_yellow[0] is not None else None} Pixels={output_yellow[4] if output_yellow[0] is not None else None}")    
    print(f"  Grid Center: {center_row, center_col}")
    print(f"  Input Grid Size: {input_grid.shape}")
    print(f"  Output Grid Size: {output_grid.shape}")    
    print("-" * 20)
    return

# fake input and output example grids created to match the provided task
example1_input = np.array([[0,0,0,0,0,0],[0,0,0,0,3,0],[0,0,0,0,3,0],[0,0,0,0,3,0],[0,4,0,0,0,0],[0,0,0,0,0,0]])
example1_output = np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,3,0,0],[0,0,0,3,0,0],[0,4,0,3,0,0],[0,0,0,0,0,0]])
analyze_example(example1_input, example1_output, 1)

example2_input = np.array([[0,0,0,0,0,0,0],[0,0,3,3,3,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,4,0],[0,0,0,0,0,0,0]])
example2_output = np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,3,3,3,0],[0,0,0,0,0,0,0],[0,0,0,0,0,4,0],[0,0,0,0,0,0,0]])
analyze_example(example2_input, example2_output, 2)

example3_input = np.array([[0,0,0,0,0],[0,3,0,0,0],[0,3,0,4,0],[0,0,0,0,0],[0,0,0,0,0]])
example3_output = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,3,4,0],[0,0,3,0,0],[0,0,0,0,0]])
analyze_example(example3_input, example3_output, 3)
