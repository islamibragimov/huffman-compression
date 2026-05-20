import sys

from huffman import compress, decompress


def help_text():
    print("Huffman File Compression Tool")
    print()
    print("Usage:")
    print("  python main.py compress input.txt output.huff")
    print("  python main.py decompress input.huff output.txt")


def main():
    if len(sys.argv) != 4:
        help_text()
        return

    cmd = sys.argv[1]
    src = sys.argv[2]
    dst = sys.argv[3]

    if cmd == "compress":
        info = compress(src, dst)
        print("Compressed successfully")
        print("Original size:", info["original"], "bytes")
        print("Compressed size:", info["packed"], "bytes")
        print("Unique characters:", info["unique"])

        if info["original"] > 0:
            ratio = info["packed"] / info["original"]
            saved = (1 - ratio) * 100
            print("Compression ratio:", round(ratio, 3))
            print("Space saved:", round(saved, 2), "%")

    elif cmd == "decompress":
        info = decompress(src, dst)
        print("Decompressed successfully")
        print("Output characters:", info["chars"])
        print("Output size:", info["bytes"], "bytes")

    else:
        help_text()


if __name__ == "__main__":
    main()
