### Requirements
- Deadlock installed
- Python 3.8 or higher
- dotnet SDK (and Runtime) 8.0 or higher (for extracting vdata files using [deadlockery](https://github.com/ouwou/deadlockery/))

### Data

- `data/heroes.json` - Contains all the heroes in the game and their abilities
- `data/items.json` - Contains all the items in the game
- `data/abilities`, `data/items`, `data/heroes` - Contains the extracted images of the abilities, items and heroes respectively
- `data/vdata` - Contains the extracted data from the game files (Thanks to [deadlockery](https://github.com/ouwou/deadlockery/))
- `DataTypes.py` - Contains the data types of json data files