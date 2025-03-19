"""
1.  **Initialization:** The output grid is always a 2x2 grid initialized with all zeros (white).

2.  **Quadrant Mapping:** The input grid (which appears to always be 4x8) is conceptually divided into four quadrants, each corresponding to a cell in the 2x2 output grid. These quadrants are:
    *   Top-Left (TL): Input rows 0-1, columns 0-3  -> Output cell [0, 0]
    *   Top-Right (TR): Input rows 0-1, columns 4-7 -> Output cell [0, 1]
    *   Bottom-Left (BL): Input rows 2-3, columns 0-3 -> Output cell [1, 0]
    *   Bottom-Right (BR): Input rows 2-3, columns 4-7 -> Output cell [1, 1]

3.  **Object Detection:** Within the input grid, identify if there is *exactly one* non-white pixel. If not present transformation is all 0.

4. **Color Assignment:** The cell at output[1,1] is assigned to red (2) IFF there is one object in the input grid in the Bottom-Right quadrant

5. **Color Assignment.** The cell at output[1,0] is assigned red (2) IFF there is one object in the input grid in the Bottom-Left quandrant.
6. **Color Assignment.** The cell at output[0,1] is assigned to red (2) IFF there is one object in the input grid in the *either* Top-Right *or* Top-Left quadrant

7.  **Default:** If there isn't a non-white pixel in the corresponding input quadrant, the output cell remains 0 (white).
"""

import numpy as np

def get_quadrant(input_grid, quadrant_name):
    """
    Extracts a quadrant from the input grid.
    """
    if quadrant_name == "TL":
        return input_grid[0:2, 0:4]
    elif quadrant_name == "TR":
        return input_grid[0:2, 4:8]
    elif quadrant_name == "BL":
        return input_grid[2:4, 0:4]
    elif quadrant_name == "BR":
        return input_grid[2:4, 4:8]
    else:
        return None

def find_object(quadrant):
    """
    Finds the location of a single non-white pixel within a quadrant.
    Returns None if there isn't exactly one non-white pixel.
    """
    non_white_pixels = np.argwhere(quadrant != 0)
    if len(non_white_pixels) == 1:
        return non_white_pixels[0]
    else:
        return None

def transform(input_grid):
    # Initialize output grid (2x2, all zeros)
    output_grid = np.zeros((2, 2), dtype=int)
    input_grid = np.array(input_grid)

    # Define quadrants
    quadrants = {
        "TL": get_quadrant(input_grid, "TL"),
        "TR": get_quadrant(input_grid, "TR"),
        "BL": get_quadrant(input_grid, "BL"),
        "BR": get_quadrant(input_grid, "BR"),
    }

    # Check for object in each quadrant and update output accordingly
    
    # Bottom Right
    if find_object(quadrants["BR"]) is not None:
            output_grid[1, 1] = 2
            
    # Bottom Left
    if find_object(quadrants["BL"]) is not None:
        output_grid[1,0] = 2

    # Top Right or Top Left
    if (find_object(quadrants["TR"]) is not None) or (find_object(quadrants["TL"]) is not None):
        output_grid[0, 1] = 2

    return output_grid