
## train_1

**input:**
```
0 0 0 0 0 3 3 3 1 0 0 0
```


**output:**
```
0 0 0 0 0 3 3 3 1 1 1 1
```


## train_2

**input:**
```
0 0 0 2 5 5 5 0 0 0 0 0
```


**output:**
```
2 2 2 2 5 5 5 0 0 0 0 0
```


## train_3

**input:**
```
0 0 9 3 3 3 3 0 0 0 0 0
```


**output:**
```
9 9 9 3 3 3 3 0 0 0 0 0
```


## train_4

**input:**
```
0 7 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
7 7 8 8 8 8 8 0 0 0 0 0
```


## train_5

**input:**
```
0 6 8 8 8 0 0 0 0 0 0 0
```


**output:**
```
6 6 8 8 8 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 2 2 2 2 2 3 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 3 3 3
```


## train_7

**input:**
```
0 0 5 5 5 5 5 5 7 0 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 7 7 7 7
```

Okay, analyzing the input-output pairs to understand the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists or arrays) of single digits (0-9).
2.  **Core Elements:** The sequences contain blocks of zeros (`0 0 ...`) and runs of identical non-zero digits (e.g., `3 3 3`, `5 5 5 5`).
3.  **Key Interaction:** The transformation seems triggered by the adjacency of a *single* non-zero digit (let's call it the "neighbor") next to a *run* of *different* non-zero digits.
4.  **Transformation Action:** The "neighbor" digit expands, replacing adjacent zeros.
5.  **Directionality:** The expansion happens away from the run (if the neighbor is to the right of the run, it expands rightward into zeros; if it's to the left, it expands leftward).
6.  **Expansion Length:** The final length of the contiguous block formed by the expanded neighbor digit seems determined by the digit value of the adjacent *run*, and potentially the relative position (left/right).

**YAML Facts:**


```yaml
Observations:
  InputType: Sequence of digits (0-9)
  OutputType: Sequence of digits (0-9)
  SequenceLength: Preserved between input and output
  KeyObjects:
    - Run:
        Description: A contiguous subsequence of identical, non-zero digits.
        Properties:
          - DigitValue (X): The digit making up the run.
          - StartIndex: Position of the first digit in the run.
          - EndIndex: Position of the last digit in the run.
    - Neighbor:
        Description: A single non-zero digit immediately adjacent (left or right) to a Run.
        Constraint: Neighbor.DigitValue (Y) != Run.DigitValue (X)
        Properties:
          - DigitValue (Y): The digit value of the neighbor.
          - PositionIndex: The index of the neighbor digit.
    - ZeroBlock:
        Description: A contiguous subsequence of zeros ('0').
        Location: Adjacent to the Neighbor, on the side opposite the Run.
  PrimaryAction:
    - Expansion:
        Description: The Neighbor digit replaces elements within the adjacent ZeroBlock.
        Actor: Neighbor digit (Y)
        Target: Adjacent ZeroBlock
        Direction: Determined by the relative position of Neighbor and Run (away from the Run).
        Outcome: The contiguous block containing the original Neighbor digit and the replaced zeros forms a new run of the Neighbor digit (Y).
  RuleForExpansionLength:
    - Dependency: The final length of the expanded Neighbor block (TargetLength) depends on the Run.DigitValue (X) and the relative position of the Neighbor.
    - Specifics:
      - If Neighbor is RIGHT of Run (Run... Neighbor Zero...):
          - If Run.DigitValue (X) = 2, TargetLength = 3
          - If Run.DigitValue (X) = 3, TargetLength = 4
          - If Run.DigitValue (X) = 5, TargetLength = 4
      - If Neighbor is LEFT of Run (...Zero Neighbor Run...):
          - If Run.DigitValue (X) = 3, TargetLength = 3
          - If Run.DigitValue (X) = 5, TargetLength = 4
          - If Run.DigitValue (X) = 8, TargetLength = 2
    - Constraint: Expansion stops if the ZeroBlock ends before TargetLength is reached.
  OverallTransformation:
    - Find the first (or only) instance of a valid Run-Neighbor pair in the input sequence.
    - Apply the Expansion action based on the RuleForExpansionLength.
    - Output the resulting sequence.
```


**Natural Language Program:**

1.  Scan the input sequence to locate a non-zero digit (the `Neighbor`) positioned immediately adjacent to a run of identical non-zero digits (the `Run`), ensuring the `Neighbor` digit's value is different from the `Run` digit's value.
2.  Identify the value of the `Run` digit (`X`) and the value of the `Neighbor` digit (`Y`).
3.  Determine the relative position: is the `Neighbor` to the left or right of the `Run`?
4.  Determine the target length (`TargetLength`) for the final block of `Neighbor` digits based on the `Run` digit (`X`) and the relative position:
    *   If the `Neighbor` is to the **right** of the `Run`: `TargetLength` is 3 if `X`=2, 4 if `X`=3, or 4 if `X`=5.
    *   If the `Neighbor` is to the **left** of the `Run`: `TargetLength` is 3 if `X`=3, 4 if `X`=5, or 2 if `X`=8.
5.  Identify the sequence of zeros directly adjacent to the `Neighbor` on the side *
```python
import math # Not strictly necessary for this logic, but included as per template guide
# No other standard libraries like numpy are needed here.

def get_target_length(run_value, position):
    """
    Calculates the target length of the expanded block based on the 
    adjacent run's value and the relative position of the neighbor.
    
    Args:
        run_value (int): The digit value of the adjacent run.
        position (str): 'left' if the neighbor is left of the run, 
                        'right' if the neighbor is right of the run.
                        
    Returns:
        int: The calculated target length for the final block of neighbor digits,
             or -1 if no specific rule is found.
    """
    if position == 'right': # Neighbor is to the RIGHT of the Run
        if run_value == 2: return 3
        if run_value == 3: return 4
        if run_value == 5: return 4
    elif position == 'left': # Neighbor is to the LEFT of the Run
        if run_value == 3: return 3
        if run_value == 5: return 4
        if run_value == 8: return 2
    return -1 # Indicate no specific rule found for this combination

def find_pattern(grid):
    """
    Scans the grid to find the first occurrence of the pattern where a single 
    non-zero digit (Neighbor) is adjacent to a different non-zero digit (part of a Run)
    and also adjacent to a zero on the other side.

    Args:
        grid (list): The input sequence of digits.

    Returns:
        dict: A dictionary containing pattern details ('neighbor_value', 
              'neighbor_index', 'run_value', 'position') if found, 
              otherwise None.
              'position' indicates if the neighbor is 'left' or 'right' of the run.
    """
    n = len(grid)
    for i in range(n): # i is the index of the potential neighbor
        neighbor_val = grid[i]
        if neighbor_val == 0:
            continue # Neighbor must be non-zero

        # Check for Run-Neighbor-Zero pattern (Run on the left, Zeros on the right)
        # Condition: grid[i-1]=RunVal, grid[i]=NeighborVal, grid[i+1]=0
        # Check boundaries: i > 0 and i + 1 < n
        if i > 0 and i + 1 < n:
            run_val = grid[i-1]
            # Check values: RunVal != 0, RunVal != NeighborVal, grid[i+1] == 0
            if run_val != 0 and run_val != neighbor_val and grid[i+1] == 0:
                 # Found the pattern
                 return {
                     'neighbor_value': neighbor_val,
                     'neighbor_index': i,
                     'run_value': run_val,
                     'position': 'right' # Neighbor is to the right of the Run
                 }

        # Check for Zero-Neighbor-Run pattern (Zeros on the left, Run on the right)
        # Condition: grid[i-1]=0, grid[i]=NeighborVal, grid[i+1]=RunVal
        # Check boundaries: i > 0 and i + 1 < n
        if i > 0 and i + 1 < n: # Re-check necessary boundaries
             run_val = grid[i+1]
             # Check values: grid[i-1] == 0, RunVal != 0, RunVal != NeighborVal
             if grid[i-1] == 0 and run_val != 0 and run_val != neighbor_val:
                 # Found the pattern
                 return {
                     'neighbor_value': neighbor_val,
                     'neighbor_index': i,
                     'run_value': run_val,
                     'position': 'left' # Neighbor is to the left of the Run
                 }
                 
    # Handle edge cases slightly differently if pattern involves grid ends
    # Example: [0, 7, 8...] -> Check i=1, run=8 (right), zero=0 (left at i-1=0)
    if n > 1:
        # Check Zero-Neighbor-Run at start: [0, Neighbor, Run...]
        if grid[0] == 0 and grid[1] != 0 and n > 2 and grid[2] != 0 and grid[1] != grid[2]:
             return {
                 'neighbor_value': grid[1],
                 'neighbor_index': 1,
                 'run_value': grid[2],
                 'position': 'left'
             }
        # Check Run-Neighbor-Zero at end: [...Run, Neighbor, 0]
        if grid[n-1] == 0 and grid[n-2] != 0 and n > 2 and grid[n-3] != 0 and grid[n-2] != grid[n-3]:
            return {
                'neighbor_value': grid[n-2],
                'neighbor_index': n-2,
                'run_value': grid[n-3],
                'position': 'right'
            }

    return None # No pattern found matching the criteria

def transform(input_grid):
    """
    Transforms the input sequence based on the following rule:
    1. Find the first instance of a single non-zero digit (Neighbor) adjacent
       to a different non-zero digit (part of a Run), where the Neighbor is 
       also adjacent to a zero on its other side (away from the Run).
    2. Determine if the Neighbor is to the left ('left' position) or right 
       ('right' position) of the Run digit it's adjacent to.
    3. Determine a target length for the Neighbor's final contiguous block 
       based on the Run's digit value and the relative position ('left'/'right').
       Specific rules map (RunValue, Position) -> TargetLength.
    4. The Neighbor digit expands into the adjacent zeros (in the direction 
       away from the Run) by replacing them. 
    5. The expansion continues until the target block length (including the 
       original Neighbor) is reached, or the sequence of adjacent zeros ends,
       or the boundary of the grid is reached.
    """
    # Ensure input is a list of integers
    grid = list(map(int, input_grid.split())) if isinstance(input_grid, str) else list(map(int, input_grid))
    
    output_grid = list(grid) # Create a mutable copy for the output
    n = len(grid)

    # Find the first occurrence of the pattern
    pattern_info = find_pattern(grid)

    # If a pattern is found, apply the transformation
    if pattern_info:
        neighbor_val = pattern_info['neighbor_value']
        neighbor_idx = pattern_info['neighbor_index']
        run_val = pattern_info['run_value']
        position = pattern_info['position']

        # Determine the target length for the final block of neighbor digits
        target_length = get_target_length(run_val, position)

        # Only proceed if a valid target length rule exists
        if target_length > 0:
            
            if position == 'right':
                # Neighbor is to the right of the run, expand rightwards into zeros
                # The block includes the neighbor, so we need to fill target_length-1 more cells
                current_block_length = 1 # Start with the neighbor itself
                # Iterate from the first zero to the right
                for k in range(neighbor_idx + 1, n):
                    # Stop if target length is reached
                    if current_block_length >= target_length:
                        break
                    # Only replace zeros
                    if grid[k] == 0: 
                        output_grid[k] = neighbor_val
                        current_block_length += 1
                    else: 
                        # Stop expansion if a non-zero is encountered
                        break
                        
            elif position == 'left':
                # Neighbor is to the left of the run, expand leftwards into zeros
                # The block includes the neighbor, so we need to fill target_length-1 more cells
                current_block_length = 1 # Start with the neighbor itself
                # Iterate from the first zero to the left (going backwards)
                for k in range(neighbor_idx - 1, -1, -1):
                    # Stop if target length is reached
                    if current_block_length >= target_length:
                        break
                    # Only replace zeros
                    if grid[k] == 0:
                        output_grid[k] = neighbor_val
                        current_block_length += 1
                    else:
                        # Stop expansion if a non-zero is encountered
                        break

    return output_grid
```
