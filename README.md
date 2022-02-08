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

The text file must contain the x and y coordinates of a cell separated by a comma, with each cell being on a new line. Each value must be between 0 and 99 (otherwise an `IndexError` exception will be thrown). This repository contains a `test.txt` file as an example.

Example:

```txt
15,23
14,23
13,23
15,24
15,25
14,25
```