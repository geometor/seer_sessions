
## example 1
*input:*
```
1 1 2 5 0 0 0 5 0 0 0
4 1 1 5 0 0 0 5 0 0 0
4 4 1 5 0 0 0 5 0 0 0
```
*expected output:*
```
1 1 2 5 4 4 1 5 1 4 4
4 1 1 5 4 1 1 5 1 1 4
4 4 1 5 1 1 2 5 2 1 1
```
*transformed output:*
```
2 1 1 5 0 5 0 0 0 0 0
1 1 4 5 0 5 0 0 0 0 0
1 4 4 5 0 5 0 0 0 0 0
```
size: True
palette: False
color count: False
pixels off: 27
**FAILED!**

## example 2
*input:*
```
6 3 3 5 0 0 0 5 0 0 0
6 3 3 5 0 0 0 5 0 0 0
6 3 2 5 0 0 0 5 0 0 0
```
*expected output:*
```
6 3 3 5 6 6 6 5 2 3 6
6 3 3 5 3 3 3 5 3 3 6
6 3 2 5 2 3 3 5 3 3 6
```
*transformed output:*
```
3 3 6 5 0 5 0 0 0 0 0
3 3 6 5 0 5 0 0 0 0 0
2 3 6 5 0 5 0 0 0 0 0
```
size: True
palette: False
color count: False
pixels off: 27
**FAILED!**

## example 3
*input:*
```
2 7 8 5 0 0 0 5 0 0 0
7 7 8 5 0 0 0 5 0 0 0
8 8 8 5 0 0 0 5 0 0 0
```
*expected output:*
```
2 7 8 5 8 7 2 5 8 8 8
7 7 8 5 8 7 7 5 8 7 7
8 8 8 5 8 8 8 5 8 7 2
```
*transformed output:*
```
8 7 2 5 0 5 0 0 0 0 0
8 7 7 5 0 5 0 0 0 0 0
8 8 8 5 0 5 0 0 0 0 0
```
size: True
palette: False
color count: False
pixels off: 25
**FAILED!**
