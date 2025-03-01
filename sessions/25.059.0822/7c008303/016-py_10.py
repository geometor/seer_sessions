"""
1.  **Identify Key Colors:** Focus on the colors azure (8), green (3), red(2), yellow(4), magenta(6) and gray(5) in the input grid.
2.  **Vertical Line Replacement:** The vertical line of azure (8) on the left side of the input grid is represented by red (2) and yellow (4) colors on output grid. First two rows of the output grid contain red(2) followed by two zeros and then yellow(4).
3.  **Scattered Color Replacement:** The scattered green (3) pixels in the input grid seem to relate to the positions of gray (5) and magenta (6) colors.
4.  **Color Position Mapping:**
    *   The azure(8) color is mapped to red(2) and yellow(4) color. The leftmost column containing 8 is mapped to 2, and third column is mapped to 4. The relative postion from top is maintained.
    *   The green(3) color is mapped to gray(5) and magenta(6).
    *   The colors red(2), yellow(4), magenta(6) and gray(5) are mapped to themseves maintaining relative input position.
5. Dimension Reduction: Reduce the input grid from 9X9 to output 6X6 grid while perserving the original locations of the colors.
"""

import numpy as np

def get_positions(grid, color):
    """
    Returns a list of (row, col) tuples representing the positions of a given color in the grid.
    """
    return [(row, col) for row in range(grid.shape[0]) for col in range(grid.shape[1]) if grid[row, col] == color]


def transform(input_grid):
    """
    Transforms the input grid to output grid based on color mapping and position.
    """
    # initialize output_grid
    output_grid = np.zeros((6, 6), dtype=int)

    # Color Position Mapping and Dimension Reduction
    color_map = {
      8 : [2,4],
      3 : [5,6],
      2 : [2],
      4 : [4],
      6 : [6],
      5 : [5]
    }

    input_positions = {}

    for color in color_map:
        input_positions[color] = get_positions(input_grid, color)

    # build output based on relative locations
    # iterate through color_map and their corresponding input positions
    # calculate target positions in output
    for color, output_colors in color_map.items():
        if len(input_positions[color])>0:
            if color == 8:  # Handle azure (8)
                
                # first occurance of 8
                first_occurance = [pos for pos in input_positions[8] if pos[1] == 2][0]
                output_row_8_1 = first_occurance[0] if first_occurance[0] < 6 else first_occurance[0] % 6
                output_grid[output_row_8_1,0] = output_colors[0]

                # second occurance of 8
                second_occurance = [pos for pos in input_positions[8] if pos[1] == 8][0]
                output_row_8_2 =  second_occurance[0] if second_occurance[0] < 6 else second_occurance[0] % 6
                output_grid[output_row_8_2, 5] = output_colors[1]
            
            elif color == 3: #Handle green(3)
                first_occurance = [pos for pos in input_positions[3] if pos[1] >=3 and pos[1] <=5 and pos[0]<=5 and pos[0] >= 3 ]

                if len(first_occurance)>0:
                        first_occurance_pos = first_occurance[0]
                        output_row_3_1 = first_occurance_pos[0] if first_occurance_pos[0] < 6 else first_occurance_pos[0] % 6
                        output_col_3_1 = first_occurance_pos[1] if first_occurance_pos[1] < 6 else first_occurance_pos[1] % 6
                        output_grid[output_row_3_1,output_col_3_1 ] = output_colors[0]
                
                second_occurance = [pos for pos in input_positions[3] if pos[1] >=6 and pos[0]<=5 and pos[0] >= 3 ]

                if len(second_occurance) > 0:
                    second_occurance_pos = second_occurance[0]
                    output_row_3_2 = second_occurance_pos[0] if second_occurance_pos[0] < 6 else second_occurance_pos[0] % 6
                    output_col_3_2 = second_occurance_pos[1] if second_occurance_pos[1] < 6 else second_occurance_pos[1] % 6 -3
                    output_grid[output_row_3_2 ,output_col_3_2] = output_colors[1]
            
            else: #remaining colors
                for pos in input_positions[color]:
                    if pos[0] < 6 and pos[1] < 6:
                        output_grid[pos[0], pos[1]] = output_colors[0]


    return output_grid