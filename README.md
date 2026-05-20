# Huffman File Compression Tool

This project compresses and decompresses text files using Huffman coding.

## Files

- `main.py` runs the program from the command line.
- `huffman.py` contains the Huffman coding functions.
- `samples/input.txt` is a sample text file for testing.

## Run

Compress a file:

```bash
python main.py compress samples/input.txt samples/output.huff
```

Decompress a file:

```bash
python main.py decompress samples/output.huff samples/result.txt
```

Check if the decompressed file is the same:

```bash
diff samples/input.txt samples/result.txt
```

Another sample that usually compresses better:

```bash
python main.py compress samples/repeated.txt samples/repeated.huff
python main.py decompress samples/repeated.huff samples/repeated_result.txt
diff samples/repeated.txt samples/repeated_result.txt
```

For very small files, the compressed file can become larger because it also stores the frequency table.

## Main ideas used

- Dictionary for counting character frequencies
- Min heap for choosing the two smallest frequency nodes
- Binary tree for storing the Huffman tree
- Variable length binary codes for compression

## Complexity

If `n` is the number of characters and `k` is the number of unique characters:

- Frequency counting: `O(n)`
- Building the Huffman tree: `O(k log k)`
- Generating codes: `O(k)`
- Encoding: `O(n)`
- Decoding: `O(n)`
