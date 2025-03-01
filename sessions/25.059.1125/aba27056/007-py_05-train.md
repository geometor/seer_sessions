
## example 1
*input:*
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 6 6 0 6 6 0
0 6 0 0 0 6 0
0 6 6 6 6 6 0
```
*expected output:*
```
0 0 0 4 0 0 0
4 0 0 4 0 0 4
0 4 0 4 0 4 0
0 0 4 4 4 0 0
0 6 6 4 6 6 0
0 6 4 4 4 6 0
0 6 6 6 6 6 0
```
*transformed output:*
```
4 4 4 4 4 4 4
4 4 4 4 4 4 4
4 4 4 4 4 4 4
4 4 4 4 4 4 4
4 6 6 4 6 6 4
4 6 4 4 4 6 4
4 6 6 6 6 6 4
```
size: True
palette: True
color count: False
pixels off: 24
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7
0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 7 0 0 0 7
0 0 0 0 7 7 7 7 7
```
*expected output:*
```
4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 4 0 7 7 7 7 7
0 0 0 4 7 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
0 0 0 4 7 4 4 4 7
0 0 4 0 7 7 7 7 7
```
*transformed output:*
```
4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4
4 4 4 4 7 7 7 7 7
4 4 4 4 7 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 7 4 4 4 7
4 4 4 4 7 7 7 7 7
```
size: True
palette: True
color count: False
pixels off: 28
**FAILED!**

## example 3
*input:*
```
3 3 3 3 3 3
3 0 0 0 0 3
3 0 0 0 0 3
3 3 0 0 3 3
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
3 3 3 3 3 3
3 4 4 4 4 3
3 4 4 4 4 3
3 3 4 4 3 3
0 4 4 4 4 0
4 0 4 4 0 4
```
*transformed output:*
```
3 3 3 3 3 3
3 4 4 4 4 3
3 4 4 4 4 3
3 3 4 4 3 3
4 4 4 4 4 4
4 4 4 4 4 4
```
size: True
palette: True
color count: False
pixels off: 4
**FAILED!**
