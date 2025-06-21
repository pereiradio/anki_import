# anki_import
This Python script processes a text file containing questions (`Q:`) and answers (`A:`) and converts them into a tab-separated format suitable for importing into Anki, a popular flashcard application.

## Features

- Reads a text file with `Q:` and `A:` blocks.
- Converts the content into a tab-separated format (`Question<TAB>Answer`).
- Saves the output in a timestamped file in the `output` directory.
- Automatically creates the `output` directory if it doesn't exist.
- Appends to the output file if the script is run multiple times within the same minute.

## Requirements

- Python 3.x
- UTF-8 encoded text file with `Q:` and `A:` blocks.

## Installation

1. Clone this repository or download the script.
2. Ensure Python 3.x is installed on your system.

## Usage

1. Place the input file (`perguntas_respostas`) in the same directory as the script.
2. Run the script:

   ```bash
   python main.py
   ```

3. The output file will be saved in the `output` directory with a name like `import_anki_YYYY-MM-DD_HH-MM.txt`.

## Input File Format

The input file should contain questions and answers in the following format:

```
Q: What is the capital of France?
A: Paris

Q: What is 2 + 2?
A: 4
```

## Output File Format

The output file will contain tab-separated values:

```
What is the capital of France?	Paris
What is 2 + 2?	4
```

## Error Handling

- If the input file is not found, the script will raise a `FileNotFoundError`.
- Ensure the input file is named `perguntas_respostas` and is in the same directory as the script.

## License

This project is licensed under the MIT License.
