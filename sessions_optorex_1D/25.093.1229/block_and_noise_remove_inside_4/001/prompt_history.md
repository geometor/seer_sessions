
## train_1

**input:**
```
0 9 9 9 7 9 8 0 0 0 0 0
```


**output:**
```
0 9 9 9 9 9 9 0 0 0 0 0
```


## train_2

**input:**
```
0 8 3 3 3 3 3 3 3 3 0 0
```


**output:**
```
0 3 3 3 3 3 3 3 3 3 0 0
```


## train_3

**input:**
```
6 3 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 4 4 4 4 4 4 4 3 4 4
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 4 4
```


## train_5

**input:**
```
0 4 4 6 9 4 4 4 4 4 4 0
```


**output:**
```
0 4 4 4 4 4 4 4 4 4 4 0
```


## train_6

**input:**
```
2 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 2 7 7 7 1 7 7 7 0
```


**output:**
```
0 0 0 7 7 7 7 7 7 7 7 0
```

*   **Perception:**
    *   The input and output are sequences of digits, presented as space-separated strings.
    *   The transformation operates on contiguous blocks (islands) of non-zero digits.
    *   Zero digits ('0') act as separators for these islands and remain unchanged in the output.
    *   Within each island of non-zero digits, one digit appears to be "dominant".
    *   All non-zero digits within an island are replaced by the dominant digit for that island.
    *   The dominant digit within an island is the digit that occurs most frequently in that specific island in the input.

*   **Facts:**
    
```yaml
    objects:
      - sequence:
          type: list of digits
          description: Represents the input and output data.
      - digit:
          type: integer (0-9)
          properties:
            - value: the numerical value of the digit.
            - position: the index of the digit in the sequence.
            - is_zero: boolean indicating if the value is 0.
      - island:
          type: contiguous subsequence of non-zero digits
          properties:
            - digits: list of non-zero digits belonging to the island.
            - start_index: position of the first digit in the island.
            - end_index: position of the last digit in the island.
            - dominant_digit: the most frequent digit within the island.
    actions:
      - identify_islands:
          input: sequence
          output: list of islands
          description: Scan the sequence and group consecutive non-zero digits into islands, separated by zeros.
      - find_dominant_digit:
          input: island
          output: digit value
          description: Calculate the frequency of each digit within the island and return the digit with the highest frequency.
      - replace_digits:
          input: sequence, list of islands
          output: modified sequence
          description: Iterate through each island and replace all its constituent non-zero digits in the original sequence with the island's dominant digit.
    relationships:
      - contains: A sequence contains digits.
      - separates: Zero digits separate islands within the sequence.
      - belongs_to: Each non-zero digit belongs to exactly one island (or none if it's zero).
      - determines: The frequency of digits within an island determines the dominant_digit.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of digits.
    2.  Initialize an empty list for the output sequence, having the same length as the input.
    3.  Iterate through the input sequence to identify contiguous subsequences (islands) of non-zero digits. Keep track of the start and end indices and the digits within each island. Zeroes act as delimiters between islands.
    4.  For each identified island:
        a.  Count the occurrences of each distinct non-zero digit within that island.
        b.  Determine the digit that has the highest frequency (the dominant digit).
        c.  For all positions in the output sequence corresponding to the current island's indices in the input sequence, set the value to the dominant digit.
    5.  For all positions in the input sequence that contain a zero, set the corresponding position in the output sequence to zero.
    6.  Join the digits in the output sequence into a space-separated string.
