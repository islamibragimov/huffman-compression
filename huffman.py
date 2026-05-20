import heapq
import json
import os


class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right


def make_freq(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def make_tree(freq):
    heap = []
    num = 0

    for ch in freq:
        heapq.heappush(heap, (freq[ch], num, Node(ch, freq[ch])))
        num += 1

    if len(heap) == 0:
        return None

    while len(heap) > 1:
        f1, n1, left = heapq.heappop(heap)
        f2, n2, right = heapq.heappop(heap)
        root = Node(None, f1 + f2, left, right)
        heapq.heappush(heap, (root.freq, num, root))
        num += 1

    return heap[0][2]


def make_codes(root):
    codes = {}

    def walk(node, code):
        if node.ch is not None:
            if code == "":
                code = "0"
            codes[node.ch] = code
            return

        walk(node.left, code + "0")
        walk(node.right, code + "1")

    if root is not None:
        walk(root, "")

    return codes


def make_bytes(bits):
    pad = (8 - len(bits) % 8) % 8
    bits = bits + "0" * pad
    data = bytearray()

    for i in range(0, len(bits), 8):
        data.append(int(bits[i:i + 8], 2))

    return bytes(data), pad


def make_bits(data, pad):
    bits = ""

    for b in data:
        bits += format(b, "08b")

    if pad > 0:
        bits = bits[:-pad]

    return bits


def read_bits(bits, root):
    if root is None:
        return ""

    if root.ch is not None:
        return root.ch * len(bits)

    text = []
    node = root

    for bit in bits:
        if bit == "0":
            node = node.left
        else:
            node = node.right

        if node.ch is not None:
            text.append(node.ch)
            node = root

    return "".join(text)


def compress(src, dst):
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()

    freq = make_freq(text)
    root = make_tree(freq)
    codes = make_codes(root)
    bits = ""

    for ch in text:
        bits += codes[ch]

    data, pad = make_bytes(bits)
    head = {"freq": freq, "pad": pad}
    head_data = json.dumps(head, ensure_ascii=False).encode("utf-8")

    with open(dst, "wb") as f:
        f.write(len(head_data).to_bytes(4, "big"))
        f.write(head_data)
        f.write(data)

    original = len(text.encode("utf-8"))
    packed = os.path.getsize(dst)

    return {
        "original": original,
        "packed": packed,
        "unique": len(freq)
    }


def decompress(src, dst):
    with open(src, "rb") as f:
        size_data = f.read(4)
        head_size = int.from_bytes(size_data, "big")
        head = json.loads(f.read(head_size).decode("utf-8"))
        data = f.read()

    root = make_tree(head["freq"])
    bits = make_bits(data, head["pad"])
    text = read_bits(bits, root)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)

    return {
        "chars": len(text),
        "bytes": os.path.getsize(dst)
    }
