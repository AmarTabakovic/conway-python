# Conway's Game of Life
![Preview](docs/preview.gif)

## Usage
### Start game
```bash
$ python3 conway.py 
```

### Start game with predefined pattern file
```bash
$ python3 conway.py --file_name [file_name]
```

The text file must contain the x and y coordinates of a cell separated by a comma, with each cell being on a new line. Each coordinate must be between 0 and 99 (otherwise an `IndexError` exception will be thrown). This repository contains examples in the `examples` directory.

Example:

```txt
17,19
16,20
17,20
18,20
16,21
18,21
```

### Keys

- `Esc`: Exit the game
- `Space`: Pause/Unpause the game
- `R`: Restart the game with a random pattern (if no text file was passed) or with the given text file