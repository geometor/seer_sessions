import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transforms an input grid based on identified patterns: solid 2x2 color prototypes, 
a hollow square defining output block size, and a template grid dictating the output layout.

1.  **Analyze Input Shapes:**
    *   Find the size 'N' of a hollow square (non-white border, white interior) in the input. This N defines the size (NxN) of the blocks used in the output.
    *   Find all solid 2x2 squares. Record the unique colors ('prototype_colors') found in these squares.

2.  **Locate Template Grid:**
    *   Identify the largest rectangular region in the input grid composed *only* of the 'prototype_colors'. This is the template grid. Determine its height 'H' and width 'W'.

3.  **Construct Output Grid:**
    *   Create an output grid of size (H * N) x (W * N).
    *   Iterate through each cell (r, c) of the template grid.
    *   For the color 'K' at template[r, c], place a solid NxN block of color 'K' into the output grid at position (r * N, c * N).

4.  **Finalize:** Return the constructed output grid.
"""

def find_hollow_square_size(grid: np.ndarray) -> Optional[int]:
    """Finds the size N of the first hollow square found."""
    rows, cols = grid.shape
    for N in range(3, min(rows, cols) + 1): # Start checking from 3x3
        for r in range(rows - N + 1):
            for c in range(cols - N + 1):
                subgrid = grid[r:r+N, c:c+N]
                border_color = -1
                is_hollow = True
                
                # Check border
                for i in range(N):
                    for j in range(N):
                        is_border = (i == 0 or i == N - 1 or j == 0 or j == N - 1)
                        pixel = subgrid[i, j]
                        
                        if is_border:
                            if pixel == 0: # Border cannot be white
                                is_hollow = False
                                break
                            if border_color == -1:
                                border_color = pixel
                            elif border_color != pixel: # Border must be uniform color
                                is_hollow = False
                                break
                        else: # Interior
                            if pixel != 0: # Interior must be white
                                is_hollow = False
                                break
                    if not is_hollow:
                        break
                
                if is_hollow and border_color != -1:
                    # print(f"Found hollow square size {N} at ({r}, {c})")
                    return N
    # print("No hollow square found")
    return None

def find_prototype_colors(grid: np.ndarray) -> Set[int]:
    """Finds the colors of solid 2x2 squares."""
    rows, cols = grid.shape
    prototype_colors = set()
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            first_pixel = subgrid[0, 0]
            if first_pixel != 0 and np.all(subgrid == first_pixel):
                prototype_colors.add(first_pixel)
                # print(f"Found 2x2 prototype color {first_pixel} at ({r}, {c})")
    # print(f"Prototype colors: {prototype_colors}")
    return prototype_colors

def find_template_grid(grid: np.ndarray, prototype_colors: Set[int]) -> Optional[np.ndarray]:
    """Finds the largest rectangular grid composed only of prototype colors."""
    rows, cols = grid.shape
    best_template = None
    max_size = 0

    for r1 in range(rows):
        for c1 in range(cols):
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    subgrid = grid[r1:r2+1, c1:c2+1]
                    is_valid_template = True
                    for pixel in np.unique(subgrid):
                        if pixel not in prototype_colors:
                            is_valid_template = False
                            break
                    
                    if is_valid_template:
                        current_size = subgrid.size
                        if current_size > max_size:
                            # Basic check to avoid picking up the 2x2 prototypes themselves if they match
                            # A real template should be larger than the prototypes or have multiple colors usually.
                            # This heuristic might need refinement for edge cases.
                            if subgrid.shape[0] > 2 or subgrid.shape[1] > 2 or len(prototype_colors) > 1 :
                                max_size = current_size
                                best_template = subgrid
                                # print(f"Found candidate template size {subgrid.shape} at ({r1}, {c1})")


    # print(f"Selected template grid with shape: {best_template.shape if best_template is not None else 'None'}")
    return best_template


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by identifying prototype shapes and a template,
    then tiling blocks according to the template.
    """
    grid = np.array(input_grid, dtype=int)

    # 1. Analyze Input Shapes
    # Find hollow square size N
    N = find_hollow_square_size(grid)
    if N is None:
        # Fallback or error handling if no hollow square is found
        # This might indicate a different task type or an issue with assumptions.
        # For now, let's try a default or raise an error. Let's assume N=3 as a guess if needed.
        # Based on examples, N is usually 3 or 5. We need it.
        print("Warning: Hollow square not found. Cannot determine block size.")
        # Trying common sizes might work for some ARC tasks but is brittle.
        # Let's raise error if not found.
        raise ValueError("Hollow square defining block size (N) not found in input grid.")


    # Find solid 2x2 prototype colors
    prototype_colors = find_prototype_colors(grid)
    if not prototype_colors:
        # Fallback or error
        raise ValueError("Solid 2x2 prototype colors not found in input grid.")

    # 2. Locate Template Grid
    template_grid = find_template_grid(grid, prototype_colors)
    if template_grid is None:
        # Fallback or error
         raise ValueError("Template grid not found in input grid.")

    H, W = template_grid.shape

    # 3. Construct Output Grid
    output_rows = H * N
    output_cols = W * N
    output_grid = np.zeros((output_rows, output_cols), dtype=int) # Default background is white (0)

    # Iterate through the template grid
    for r in range(H):
        for c in range(W):
            # Get the color K from the template
            K = template_grid[r, c]

            # Define the target region in the output grid
            start_row, end_row = r * N, (r + 1) * N
            start_col, end_col = c * N, (c + 1) * N

            # Fill the NxN block with color K
            output_grid[start_row:end_row, start_col:end_col] = K

    # 4. Finalize
    return output_grid.tolist()
