# Conway's Game of Life
![Preview](docs/preview.gif)

## Usage
### Start game
```bash
python3 conway.py 
```

### Start game with predefined pattern file
```bash
python3 conway.py --file_name test.txt
```

The text file must contain the x and y positions of a cell separated by commas, each cell being on a new line. The values cannot exceed the size of the grid subtracted by 1 (otherwise an `IndexError` exception will be thrown). This repository contains a `test.txt` file as an example.

Example:

```txt
15,23
14,23
13,23
15,24
15,25
14,25
```