
## example 1
*input:*
```
0 4 0 9
0 0 0 0
0 4 6 0
1 0 0 0
```
*expected output:*
```
0 0 0 0
0 0 0 0
0 4 0 0
1 4 6 9
```
*transformed output:*
```
0 0 0 0
0 0 0 0
0 0 0 1
6 4 9 4
```
size: True
palette: True
color count: True
pixels off: 5
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 9
0 0 0 8 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 8 0 9
```
*transformed output:*
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 7 4
8 7 4 4 8 9
```
size: True
palette: True
color count: True
pixels off: 11
**FAILED!**

## example 3
*input:*
```
0 0 0 1 0
0 3 0 0 0
0 3 0 1 2
6 0 0 0 0
0 3 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 0 0 0 0
0 3 0 0 0
0 3 0 1 0
6 3 0 1 2
```
*transformed output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 3 6
2 1 3 3 1
```
size: True
palette: True
color count: True
pixels off: 9
**FAILED!**
