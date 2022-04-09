KEY_W = 55
KEY_H = 45
KEY_RX = 6
KEY_RY = 6
INNER_PAD_W = 2
INNER_PAD_H = 2
OUTER_PAD_W = KEY_W / 2
OUTER_PAD_H = KEY_H / 2
LINE_SPACING = 18

STYLE = """
    svg {
        font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
        font-size: 14px;
        font-kerning: normal;
        text-rendering: optimizeLegibility;
        fill: #24292e;
    }

    rect {
        fill: #f6f8fa;
    }

    .held {
        fill: #fdd;
    }

    .trans+text {
        opacity: 30%;
    }

    .small+text {
        font-size: 10px;
    }
"""


def held(key):
    return {"key": key, "class": "held"}

def trans(key):
    return {"key": key, "class": "trans"}

def small(key):
    return {"key": key, "class": "small"}

KEYMAP = [
    {
        "left": [
            ["esc", "1", "2", "3", "4", "5"],
            ["tab", "q", "w", "e", "r", "t"],
            ["ctrl", "a", "s", "d", "f", "g"],
            ["shift", "z", "x", "c", "v", "b", "["],
        ],
        "right": [
            ["", "6", "7", "8", "9", "0", "`🔒"],
            ["", "y", "u", "i", "o", "p", "-"],
            ["", "h", "j", "k", "l", ";", "'"],
            ["]", "n", "m", ",", ".", "/", "shift"],
        ],
        "thumbs": {
            "left": ["alt", "gui", "lower", "space"],
            "right": ["enter", "raise", "bspc", "gui"]
        },
    },
    {
        "left": [
            ["BT_CLR", "BT1", "BT2", "BT3", "BT4", "BT5"],
            ["f1", "f2", "f3", "f4", "f5", "f6"],
            ["`", "!", "@", "#", "$", "%"],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
        ],
        "right": [
            ["", trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            ["", "f7", "f8", "f9", "f10", "f11", "f12"],
            ["", "^", "&#38;", "*", "(", ")", "~"],
            [trans(""), trans(""), "-", "+", "{", "}", "|"],
        ],
        "thumbs": {
            "left": [trans(""), trans(""), held("lower"), trans("space")],
            "right": [trans("enter"), trans("raise"), trans(""), trans("")]
        },
    },
    {
        "left": [
            [trans("esc"), trans(""), trans(""), trans(""), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
        ],
        "right": [
            ["", "⧉", trans(""), "⏯", "🔈", "🔊", trans("`🔒")],
            ["", trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            ["", "←", "↓", "↑", "→", trans(""), trans("")],
            [trans(""), "+", "-", "=", "*", "\\", trans("")],
        ],
        "thumbs": {
            "left": [trans(""), trans(""), trans("lower"), trans("space")],
            "right": [trans("enter"), held("raise"), trans(""), trans("")]
        },
    },
    {
        "left": [
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
        ],
        "right": [
            ["", trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            ["", trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
            ["", small("alt_gui_←"), small("alt_gui_↑"), small("alt_gui_↓"), small("alt_gui_→"), trans(""), trans("")],
            [trans(""), trans(""), trans(""), trans(""), trans(""), trans(""), trans("")],
        ],
        "thumbs": {
            "left": [trans(""), trans(""), held("lower"), trans("space")],
            "right": [trans("enter"), held("raise"), trans(""), trans("")]
        },
    },
]

KEYSPACE_W = KEY_W + 2 * INNER_PAD_W
KEYSPACE_H = KEY_H + 2 * INNER_PAD_H
HAND_W = 7 * KEYSPACE_W
HAND_H = 5 * KEYSPACE_H
LAYER_W = 2 * HAND_W + OUTER_PAD_W
LAYER_H = HAND_H
BOARD_W = LAYER_W + 2 * OUTER_PAD_W
BOARD_H = 4 * LAYER_H + 5 * OUTER_PAD_H


def print_key(x, y, key):
    key_class = ""
    if type(key) is dict:
        key_class = key["class"]
        key = key["key"]
    elif not key.strip():
        return
    print(
        f'<rect rx="{KEY_RX}" ry="{KEY_RY}" x="{x + INNER_PAD_W}" y="{y + INNER_PAD_H}" width="{KEY_W}" height="{KEY_H}" class="{key_class}" />'
    )
    words = key.split()
    y += (KEYSPACE_H - (len(words) - 1) * LINE_SPACING) / 2
    for word in key.split():
        print(
            f'<text text-anchor="middle" dominant-baseline="middle" x="{x + KEYSPACE_W / 2}" y="{y}">{word}</text>'
        )
        y += LINE_SPACING


def print_row(x, y, row):
    for key in row:
        print_key(x, y, key)
        x += KEYSPACE_W


def print_block(x, y, block):
    for row in block:
        print_row(x, y, row)
        y += KEYSPACE_H


def print_layer(x, y, layer):
    print_block(x, y, layer["left"])
    print_block(
        x + HAND_W + OUTER_PAD_W, y, layer["right"],
    )
    print_row(
        x + 3 * KEYSPACE_W, y + 4 * KEYSPACE_H, layer["thumbs"]["left"],
    )
    print_row(
        x + HAND_W + OUTER_PAD_W, y + 4 * KEYSPACE_H, layer["thumbs"]["right"],
    )


def print_board(x, y, keymap):
    x += OUTER_PAD_W
    for layer in keymap:
        y += OUTER_PAD_H
        print_layer(x, y, layer)
        y += LAYER_H


print(
    f'<svg width="{BOARD_W}" height="{BOARD_H}" viewBox="0 0 {BOARD_W} {BOARD_H}" xmlns="http://www.w3.org/2000/svg">'
)
print(f"<style>{STYLE}</style>")
print_board(0, 0, KEYMAP)
print("</svg>")
