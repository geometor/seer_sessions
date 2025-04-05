*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of 12 integers.
    *   The integers involved seem to primarily be 0, 2, and other non-zero digits (1, 4, 5, 6, 8, 9 in the examples).
    *   The transformation involves rearranging elements within the sequence based on specific patterns involving the numbers 0 and 2.
    *   The number 0 acts as empty space or a placeholder that can be swapped or filled.
    *   The number 2 appears to act as a special boundary or condition marker.
    *   Other non-zero numbers (not 2) seem to be movable elements or blocks of elements.
    *   The core transformation appears to be either a local swap of a non-zero number (not 2) with an adjacent 0 when followed by a 2, or a leftward shift of a block of non-zero numbers (not 2) over adjacent zeros when preceded by a 2.
    *   If neither of these specific patterns is present, the sequence remains unchanged.

*   **Facts:**
    
```yaml
    Task: Rearrange elements in a sequence based on local patterns involving 0 and 2.

    Objects:
      - Sequence: A list of 12 integers.
      - Element: An integer within the sequence.
      - Number_Zero: The integer 0, acting as space.
      - Number_Two: The integer 2, acting as a boundary/condition.
      - Non_Zero_Element: Any integer X != 0 and X != 2.
      - Non_Zero_Block: A contiguous sub-sequence Y containing only Non_Zero_Elements.

    Properties:
      - Position: The index of an element in the sequence.
      - Value: The integer value of an element.
      - Adjacency: Elements immediately next to each other.
      - Precedence: An element or block coming before another in the sequence.

    Relationships/Patterns:
      - Pattern_Swap: A Non_Zero_Element X followed immediately by 0, followed immediately by 2 (X, 0, 2).
      - Pattern_Shift: A 2 followed immediately by one or more 0s, followed immediately by a Non_Zero_Element or a Non_Zero_Block Y (2, 0..., 0, Y).

    Actions:
      - Scan: Iterate through the sequence to find patterns.
      - Identify: Recognize specific patterns (Pattern_Swap, Pattern_Shift).
      - Swap: Exchange the positions of two adjacent elements (X and 0 in Pattern_Swap).
      - Move_Block: Relocate a Non_Zero_Block Y to a new position (immediately after 2 in Pattern_Shift).
      - Fill_Zeros: Place zeros in the positions previously occupied by the moved block.
      - Halt: Stop processing after the first applicable transformation.
      - No_Change: Output the sequence unmodified if no patterns are found.
    ```


*   **Natural Language Program:**
    1.  Examine the input sequence from left to right.
    2.  Search for the first occurrence of the pattern: a non-zero integer `X` (where `X` is not 2) immediately followed by a 0, which is immediately followed by a 2 (i.e., the sub-sequence `X, 0, 2`).
    3.  If this pattern (`X, 0, 2`) is found, modify the sequence by swapping the positions of `X` and 0 to create the sub-sequence `0, X, 2`. Leave the rest of the sequence unchanged relative to this triplet. Stop processing and output the modified sequence.
    4.  If the pattern `X, 0, 2` is *not* found anywhere in the sequence, then search for the first occurrence of the pattern: the integer 2 followed by one or more consecutive 0s, followed immediately by a non-zero integer or a contiguous block `Y` of non-zero integers (where none of the integers in `Y` are 2).
    5.  If this pattern (`2, 0..., 0, Y`) is found, modify the sequence by moving the entire block `Y` to the position immediately following the 2. Fill the original positions of the zeros (that were between 2 and `Y`) and the original positions of block `Y` with zeros, placing them after the moved block `Y`. Stop processing and output the modified sequence.
    6.  If neither the `X, 0, 2` pattern nor the `2, 0..., 0, Y` pattern is found in the sequence, output the original input sequence without any modifications.