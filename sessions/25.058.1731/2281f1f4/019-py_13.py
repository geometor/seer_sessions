import numpy as np

def check_border_and_infill(grid):
    """
    Checks the grid's border characteristics and presence of the specific blue infill.

    Returns:
        A dictionary containing:
        - has_solid_border (bool): True if the grid has a solid border of any color.
        - border_color (int or None): The color of the border if solid, otherwise None.
        - has_blue_infill (bool): True if the specific blue infill is present.
        - infill_coords: coordinates of infill
    """
    rows, cols = grid.shape
    border_color = None
    has_solid_border = False
    has_blue_infill = False
    infill_coords = None

    # Check top and bottom rows, assuming they have a consistent color
    top_row_color = grid[0, 0]
    bottom_row_color = grid[rows - 1, 0]
    
    top_row_uniform = all(grid[0, col] == top_row_color for col in range(cols))
    bottom_row_uniform = all(grid[rows - 1, col] == bottom_row_color for col in range(cols))

    if not (top_row_uniform and bottom_row_uniform):
        return {
            "has_solid_border": False,
            "border_color": None,
            "has_blue_infill": False,
            "infill_coords": None,
        }
    
    left_col_color = grid[0,0]
    right_col_color = grid[0, cols - 1]
    
    left_col_uniform = all(grid[row, 0] == left_col_color for row in range(rows))
    right_col_uniform = all(grid[row, cols - 1] == right_col_color for row in range(rows))

    if not (left_col_uniform and right_col_uniform):
           return {
            "has_solid_border": False,
            "border_color": None,
            "has_blue_infill": False,
               "infill_coords": None,
        }    

    # check for complete border
    if top_row_color == bottom_row_color and top_row_color == left_col_color and top_row_color == right_col_color:
      has_solid_border = True
      border_color = top_row_color #all border colors same, so pick any

    # Check for the specific blue infill
    if rows > 1 and cols > 1 and grid[rows - 2, 1] == 1:
        has_blue_infill = True
        infill_coords = (rows - 2, 1)

    return {
        "has_solid_border": has_solid_border,
        "border_color": border_color,
        "has_blue_infill": has_blue_infill,
        "infill_coords": infill_coords,
    }

# Get data for all examples provided
examples_data = []
for i, (input_grid, output_grid) in enumerate(zip(task_json['train']['input'], task_json['train']['output'])):
    input_grid_np = np.array(input_grid)
    output_grid_np = np.array(output_grid)
    
    input_data = check_border_and_infill(input_grid_np)
    output_data = check_border_and_infill(output_grid_np)
    
    examples_data.append({
      "example_index": i,
      "input": input_data,
      "output": output_data
    })
    
for ex in examples_data:
    print(ex)