import numpy as np

"""
The transformation involves mapping color-coded shape templates defined in the upper part of the input grid onto a grid structure defined by 'L' shaped markers in the lower part.

1.  **Template Extraction**: Scan the upper part of the input grid (above the first row containing grey). Identify marker pixels (colors other than white(0), blue(1), grey(5)). For each marker pixel at `(r, c)`, extract the 2x2 shape directly below it (`rows r+1` to `r+2`, `cols c` to `c+1`). Convert this 2x2 shape into a binary template (1 where the color is blue(1), 0 otherwise). Store a mapping from the marker color to its binary template.

2.  **Instance Identification**: Scan the lower part of the input grid (starting from the first row containing grey(5)). Find all 2x2 blocks that consist of exactly 3 grey(5) pixels forming an 'L' shape, surrounding a single non-grey 'content' pixel. Record the color of the content pixel and the top-left coordinates `(y, x)` of the 2x2 block for each valid instance.

3.  **Layout Calculation**: If no instances are found, return a 1x1 grid containing white(0). Otherwise, determine the top-most (`min_y`) and left-most (`min_x`) coordinates among all found instance blocks. Calculate the relative row (`rel_r`) and column (`rel_c`) for each instance based on its position relative to `(min_y, min_x)`, assuming a grid spacing of 3 pixels (i.e., `rel_r = (y - min_y) // 3`, `rel_c = (x - min_x) // 3`). Find the maximum relative row (`max_rel_r`) and column (`max_rel_c`) across all instances.

4.  **Output Grid Construction**: Define the size of the template shapes (assumed to be 2x2, `shape_h=2`, `shape_w=2`) and the spacing/block size (`BLOCK_SIZE=3`). Calculate the output grid dimensions: `height = max_rel_r * BLOCK_SIZE + shape_h`, `width = max_rel_c * BLOCK_SIZE + shape_w`. Initialize an output grid of this size with white pixels (0).

5.  **Drawing Shapes**: Iterate through the found instances. For each instance `(color, y, x)` with relative coordinates `(rel_r, rel_c)`:
    *   Check if a template exists for the instance `color`.
    *   If a template exists, retrieve the binary template.
    *   Calculate the top-left drawing position in the output grid: `out_y = rel_r * BLOCK_SIZE`, `out_x = rel_c * BLOCK_SIZE`.
    *   Draw the template onto the output grid at `(out_y, out_x)`. Where the template has a 1, place the instance `color` in the output grid cell `(out_y + template_row, out_x + template_col)`.

6.  **Return** the final output grid.
"""

def find_templates(grid):
    """
    Scans the upper part of the grid to find color->shape template mappings.
    A template is defined by a non-white/grey/blue color pixel, and the
    2x2 pattern of blue pixels directly below it.
    """
    templates = {}
    height, width = grid.shape
    
    # Determine the boundary row (heuristic: first row with a grey pixel)
    split_row = height
    for r in range(height):
        if 5 in grid[r, :]:
            split_row = r
            break
            
    # Scan for template markers above the split row
    for r in range(split_row - 1): # Need space for the 2x2 below
        for c in range(width - 1): # Need space for the 2x2 below
            template_color = grid[r, c]
            # Check if it's a potential template color marker
            if template_color not in [0, 1, 5]: 
                # Check if there's space for the 2x2 area below
                if r + 2 < height and c + 1 < width:
                    # Extract the 2x2 area below
                    sub_grid = grid[r+1:r+3, c:c+2]
                    # Store the shape (1 for blue, 0 otherwise)
                    # Only store if there is at least one blue pixel? Examples suggest yes.
                    if np.any(sub_grid == 1):
                        shape = (sub_grid == 1).astype(int)
                        templates[template_color] = shape
                        # print(f"Found template: color={template_color} at ({r},{c}), shape=\n{shape}") # Debug
    return templates

def find_instances(grid):
    """
    Scans the lower part of the grid to find grey L-shapes and their content pixels.
    Returns a list of tuples: (content_color, top_left_y, top_left_x) for valid instances.
    A grey L is 3 grey pixels in a 2x2 block. The content pixel is the non-grey one.
    Ignores instances where the content pixel is grey (shouldn't happen with 3 greys).
    """
    instances = []
    height, width = grid.shape
    
    # Determine the start row (heuristic: first row with a grey pixel)
    start_row = 0
    for r in range(height):
        if 5 in grid[r, :]:
            start_row = r
            break

    # Iterate through potential top-left corners of 2x2 blocks containing grey Ls
    for r in range(start_row, height - 1):
        for c in range(width - 1):
            sub_grid = grid[r:r+2, c:c+2]
            
            # Check for exactly 3 grey pixels (value 5)
            if np.count_nonzero(sub_grid == 5) == 3:
                # Find the non-grey pixel's value (content color)
                content_color = -1
                is_L_shape = False
                for sr in range(2):
                    for sc in range(2):
                        if sub_grid[sr, sc] != 5:
                            content_color = sub_grid[sr, sc]
                            # Verify L-shape by checking neighbors within the 2x2
                            adj_grey_count = 0
                            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: 
                                 nr, nc = sr + dr, sc + dc
                                 if 0 <= nr < 2 and 0 <= nc < 2 and sub_grid[nr, nc] == 5:
                                     adj_grey_count += 1
                            if adj_grey_count == 2: # Content pixel must touch 2 grey pixels in L
                                is_L_shape = True
                            break # Found the non-grey pixel
                    if content_color != -1:
                        break
                
                # Ensure it was a valid L and content color is not grey itself
                if is_L_shape and content_color != 5 and content_color != -1: 
                    instances.append((content_color, r, c))
                    # print(f"Found instance: color={content_color} at block top-left ({r},{c})") # Debug

    return instances

def draw_shape(output_grid, color, shape, y, x):
    """Draws the shape onto the output grid at position (y, x) using the given color."""
    shape_h, shape_w = shape.shape
    grid_h, grid_w = output_grid.shape
    for r in range(shape_h):
        for c in range(shape_w):
            if shape[r, c] == 1: # If the template shape has a pixel here
                out_r, out_c = y + r, x + c
                if 0 <= out_r < grid_h and 0 <= out_c < grid_w:
                    output_grid[out_r, out_c] = color

def transform(input_grid):
    """
    Transforms the input grid based on templates found in the upper part
    and instances found in the lower part.
    """
    input_np = np.array(input_grid)
    
    # 1. Find color-to-shape templates
    templates = find_templates(input_np)
    # print(f"Templates found: {templates}") # Debug

    # 2. Find instances (content_color, absolute_y, absolute_x of the 2x2 block)
    instances = find_instances(input_np)
    # print(f"Instances found: {instances}") # Debug

    # Handle case where no instances are found
    if not instances:
        return np.zeros((1, 1), dtype=int).tolist() 

    # 3. Determine relative layout and output grid size
    min_y = min(inst[1] for inst in instances)
    min_x = min(inst[2] for inst in instances)
    max_rel_r = 0
    max_rel_c = 0
    
    relative_instances = []
    BLOCK_SIZE = 3 # Spacing between instance blocks
    SHAPE_H, SHAPE_W = 2, 2 # Assumed dimensions of the template shapes
    
    for color, y, x in instances:
        # Calculate relative row/col based on block spacing
        rel_r = (y - min_y) // BLOCK_SIZE 
        rel_c = (x - min_x) // BLOCK_SIZE
        
        relative_instances.append((color, rel_r, rel_c))
        max_rel_r = max(max_rel_r, rel_r)
        max_rel_c = max(max_rel_c, rel_c)

    # 4. Calculate output grid dimensions
    # Height = (number of rows of blocks * block size) - overlap adjustment
    # Height = (max_rel_r + 1) * BLOCK_SIZE - (BLOCK_SIZE - SHAPE_H) 
    # Height = max_rel_r * BLOCK_SIZE + BLOCK_SIZE - BLOCK_SIZE + SHAPE_H
    # Height = max_rel_r * BLOCK_SIZE + SHAPE_H
    output_height = max_rel_r * BLOCK_SIZE + SHAPE_H
    output_width = max_rel_c * BLOCK_SIZE + SHAPE_W
    
    # Ensure minimum size just in case
    output_height = max(1, output_height)
    output_width = max(1, output_width)

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 5. Construct output grid by drawing shapes
    for color, rel_r, rel_c in relative_instances:
        if color in templates:
            shape = templates[color]
            # Calculate top-left corner for drawing the 2x2 shape within its conceptual 3x3 block
            output_y = rel_r * BLOCK_SIZE
            output_x = rel_c * BLOCK_SIZE
            # Draw the shape using the instance color
            draw_shape(output_grid, color, shape, output_y, output_x)
        else:
             # This case might indicate an issue if task assumes all instance colors have templates
             print(f"Warning: No template found for color {color} from instance at relative ({rel_r},{rel_c})")

    # 6. Return the final grid
    return output_grid.tolist()