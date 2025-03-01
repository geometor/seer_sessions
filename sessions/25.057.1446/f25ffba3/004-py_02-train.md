
## example 1
*input:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 9
0 0 3 9
0 0 3 9
2 0 3 9
2 4 3 9
```
*expected output:*
```
2 4 3 9
2 0 3 9
0 0 3 9
0 0 3 9
0 0 0 9
0 0 0 9
0 0 3 9
0 0 3 9
2 0 3 9
2 4 3 9
```
*transformed output:*
```
3 4 2 9
3 0 2 9
3 0 0 9
3 0 0 9
0 0 0 9
0 0 0 9
3 0 0 9
3 0 0 9
3 0 2 9
3 4 2 9
```
size: True
palette: True
color count: True
pixels off: 16
**FAILED!**

## example 2
*input:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 2
0 0 0 2
0 8 0 2
0 3 8 2
3 3 8 2
```
*expected output:*
```
3 3 8 2
0 3 8 2
0 8 0 2
0 0 0 2
0 0 0 2
0 0 0 2
0 0 0 2
0 8 0 2
0 3 8 2
3 3 8 2
```
*transformed output:*
```
2 3 0 3
2 3 0 0
2 8 0 0
2 0 0 0
2 0 0 0
2 0 0 0
2 0 0 0
2 8 0 0
2 3 8 0
2 3 8 3
```
size: True
palette: True
color count: False
pixels off: 22
**FAILED!**
