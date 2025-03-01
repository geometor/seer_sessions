"""
The transformation rule can be described as follows:

1.  **Identify Objects:** Find all contiguous blocks of non-zero pixels of the same color. Each block is considered an object.
2.  **Determine Movement**:
    *   If an object is present in the input, check its color and position.
    *   Compare the object's position in the input to its position in the output.
        * In example 1 and 2 the colored objects are shifted vertically downward.
        * The number of rows the object is shifted is consistent for all objects of the same color within a single example, but variable between examples.
        * In example 3, the objects remain unchanged.
3. **Apply rule to the Test Input**:
    * Based on review of the three examples, apply the transformation rule to move objects vertically downwards based on their color, or retain the input in the output if the objects do not move.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (non-zero pixels of the same color) in a grid.

    Args:
        grid: A NumPy array representing the grid.

    Returns:
        A dictionary where keys are colors and values are lists of positions.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, positions):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        positions.append((row, col))
        dfs(row + 1, col, color, positions)
        dfs(row - 1, col, color, positions)
        dfs(row, col + 1, color, positions)
        dfs(row, col - 1, color, positions)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                positions = []
                dfs(row, col, color, positions)
                if color not in objects:
                    objects[color] = []
                objects[color].append(positions)  # Store positions of the object
    return objects

def calculate_shift(input_objects, output_objects):
    """
    Calculates the vertical shift for each color.

    Args:
      input_objects: A dictionary of objects in the input grid
      output_objects: A dictionary of objects in the output grid.

    Returns:
        A dictionary where keys are colors and values are the vertical shift.
    """
    shifts = {}
    for color, input_positions_list in input_objects.items():
      if color in output_objects:
        output_positions_list = output_objects[color]

        #Handle multiple objects of the same color
        for input_positions, output_positions in zip(input_positions_list, output_positions_list):
          # Assuming only one object of each color, take the first position
          input_row = input_positions[0][0]
          output_row = output_positions[0][0]
          shifts[color] = output_row - input_row # Calculate vertical shift
          break #process only the first object of each colour
    return shifts

def transform(input_grid):
    """
    Transforms the input grid based on observed object movements.

    Args:
        input_grid: The input grid as a NumPy array.

    Returns:
        The transformed output grid as a NumPy array.
    """
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Handle the case where no transformation is required (example 3)
    # Create dummy output_grid and objects to represent no change (example 3 like behavior)
    all_shifts_zero = True
    for i in range(1,4):

        input_grid_local = globals()[f'input_grid{i}']
        output_grid_local = globals()[f'output_grid{i}']

        input_objects_local = find_objects(input_grid_local)
        output_objects_local = find_objects(output_grid_local)

        shifts_local = calculate_shift(input_objects_local, output_objects_local)
        
        if any(shift != 0 for shift in shifts_local.values()):
            all_shifts_zero = False
            break

    if all_shifts_zero:
        return output_grid

    # Find objects in the input grid
    input_objects = find_objects(input_grid)

    # Dummy output for determining shift - based on example 1 & 2
    example_input_grid = input_grid1
    example_output_grid = output_grid1
    example_input_objects = find_objects(example_input_grid)
    example_output_objects = find_objects(example_output_grid)
    shifts = calculate_shift(example_input_objects, example_output_objects)

    # Apply the transformation
    for color, input_positions_list in input_objects.items():
        if color in shifts:
            shift = shifts[color]
            for input_positions in input_positions_list:
              for r, c in input_positions:
                output_grid[r, c] = 0  # Clear original position
                new_r = r + shift
                # Ensure new position is within bounds
                if 0 <= new_r < output_grid.shape[0]:
                    output_grid[new_r, c] = color # set color in new position

    return output_grid