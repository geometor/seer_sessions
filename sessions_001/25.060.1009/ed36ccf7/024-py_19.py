"""
Attempts to discern and apply a transformation rule from an input grid to an output grid,
handling various cases including transpositions, reflections, and size changes.  This is
a more general approach than a fixed transformation, adapting to the specific
input/output relationship.
"""

import numpy as np

def _transpose(grid):
    """Transposes a grid (swaps rows and columns)."""
    return np.array(grid).T.tolist()

def _reflect_horizontal(grid):
  """Reflect a grid horizontally"""
  return np.flip(grid, axis=1).tolist()
  
def _reflect_vertical(grid):
    """Reflects a grid vertically"""
    return np.flip(grid, axis=0).tolist()

def _reshape(input_grid, output_shape):
  """
  Takes the input grid and reshapes to output shape
  """
  input_array = np.array(input_grid)
  try:
     output_array = input_array.reshape(output_shape)
  except ValueError:
     return None # cannot reshape
  output_grid = output_array.tolist()
  return output_grid  

def transform(input_grid):
    """
    Transforms the input grid based on an analysis of its relationship to a
    (hypothetical) output grid. This function currently implements:
      - Transposition (for square grids)
      - Reshaping from row to column if output grid shape can be inferred

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        A transformed grid as a list of lists, or the original grid if no
        supported transformation is identified.
    """
    input_array = np.array(input_grid)
    input_shape = input_array.shape
    
    # --- Transpose ---
    if len(input_shape) == 2 and input_shape[0] == input_shape[1]:
        # Square grid: Try transposing
        output_grid = _transpose(input_grid)
        return output_grid
      
    # --- Reshape row to column vector ---
    if len(input_shape) == 2 and input_shape[0] == 1:
      output_shape = (input_shape[1], 1)
      output_grid = _reshape(input_grid, output_shape)
      if output_grid: # Check if reshape succeeded
        return output_grid
      
    # --- Reshape col to row vector ---
    if len(input_shape) == 2 and input_shape[1] == 1:
      output_shape = (1, input_shape[0])
      output_grid = _reshape(input_grid, output_shape)
      if output_grid:
          return output_grid
        
    # --- Horizontal reflection ----
    # output_grid = _reflect_horizontal(input_grid)
    # return output_grid
    
    # --- Vertical reflection ---
    # output_grid = _reflect_vertical(input_grid)
    # return output_grid
    
    # If no specific transformation identified, return the original grid
    return input_grid