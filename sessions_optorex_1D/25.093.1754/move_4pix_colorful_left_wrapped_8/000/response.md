*   **Perception of Task Elements:**
    *   The input and output are sequences of numbers represented as strings, separated by spaces.
    *   All input sequences have a length of 12 elements.
    *   All output sequences also have a length of 12 elements.
    *   The transformation appears to be a rearrangement of the input sequence elements.
    *   Specifically, the input sequence seems to be split into two segments, and these segments are swapped in the output.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input:
      type: string
      format: space-separated numbers
      length: 12
      elements:
        type: number (represented as string character)
    output:
      type: string
      format: space-separated numbers
      length: 12
      elements:
        type: number (represented as string character)
    transformation:
      action: split_and_swap
      split_point: after the 4th element
      segments:
        - segment_1: first 4 elements of the input
        - segment_2: last 8 elements of the input
      output_construction: concatenate segment_2 followed by segment_1
    constraints:
      - Input sequence length is always 12.
      - Element order within each segment is preserved.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of 12 number strings.
    2.  Extract the first 4 elements into a 'first segment' list.
    3.  Extract the elements from index 4 to the end (the last 8 elements) into a 'second segment' list.
    4.  Create the output list by concatenating the 'second segment' followed by the 'first segment'.
    5.  Join the elements of the output list with spaces to form the final output string.