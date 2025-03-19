
## example 1
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 1 0 5 0 2 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
6 6 6 5 7 7 7 5 6 6 6
6 6 6 5 7 7 7 5 6 6 6
6 6 6 5 7 7 7 5 6 6 6
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 2 0 5 0 3 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
7 7 7 5 8 8 8 5 6 6 6
7 7 7 5 8 8 8 5 6 6 6
7 7 7 5 8 8 8 5 6 6 6
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 0 1 0 5 0 4 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
8 8 8 5 6 6 6 5 9 9 9
8 8 8 5 6 6 6 5 9 9 9
8 8 8 5 6 6 6 5 9 9 9
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 4
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 4 0 5 0 1 0 5 0 2 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 2 0 5 0 3 0 5 0 4 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
9 9 9 5 6 6 6 5 7 7 7
9 9 9 5 6 6 6 5 7 7 7
9 9 9 5 6 6 6 5 7 7 7
5 5 5 5 5 5 5 5 5 5 5
7 7 7 5 8 8 8 5 9 9 9
7 7 7 5 8 8 8 5 9 9 9
7 7 7 5 8 8 8 5 9 9 9
```
*transformed output:*
```
6 6 6 5 8 8 8 5 9 9 9
6 6 6 5 8 8 8 5 9 9 9
6 6 6 5 8 8 8 5 9 9 9
5 5 5 5 5 5 5 5 5 5 5
9 9 9 5 7 7 7 5 6 6 6
9 9 9 5 7 7 7 5 6 6 6
9 9 9 5 7 7 7 5 6 6 6
```
size: True
palette: True
color count: False
pixels off: 54
**FAILED!**
