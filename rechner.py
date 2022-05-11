import enum
import operator


class Type(enum.Enum):
    num = 0
    plus = 1
    minus = 2
    mult = 3
    div = 4
    linke_klammer = 5
    rechte_klammer = 6
    is_not = 7
    equal = 8
    unknown = -1
    end = 99


class Node:
    def __init__(self, op_type: Type, value=None):
        self.op_type = op_type
        self.value = value
        self.kinders = []


mapping = {
    "+": Type.plus,
    "-": Type.minus,
    "*": Type.mult,
    "/": Type.div,
    "!": Type.is_not,
    "=": Type.equal,
    "(": Type.linke_klammer,
    ")": Type.rechte_klammer
}

operationen = {
    Type.plus: operator.add,
    Type.minus: operator.sub,
    Type.mult: operator.mul,
    Type.div: operator.truediv,
    Type.is_not: operator.is_not,
    Type.equal: operator.is_
}

level1 = [
    Type.plus,
    Type.minus,
    Type.is_not,
    Type.equal
]

level2 = [
    Type.mult,
    Type.div
]


def normalize(s: str) -> str:
    return s.strip().replace(" ", "")


def lex(s: str) -> list:
    global mapping

    nodes = []
    for char in s:
        if char in mapping:
            op_type = mapping[char]
            node = Node(op_type, char)
        elif char.isnumeric():
            node = Node(Type.num, value=int(char))
        else:
            node = Node(Type.unknown)
        nodes.append(node)
    nodes.append(Node(Type.end))
    return nodes


def match(nodes: list, type: Type) -> None:
    if nodes[0].op_type == type:
        nodes.pop(0)
    return None


def level_1(nodes: list) -> Node:
    left_node = level_2(nodes)

    while nodes[0].op_type in level1:
        node = nodes.pop(0)
        node.kinders.append(left_node)
        node.kinders.append(level_2(nodes))
        left_node = node
    return left_node


def level_2(nodes: list) -> Node:
    left_node = level_3(nodes)

    while nodes[0].op_type in level2:
        node = nodes.pop(0)
        node.kinders.append(left_node)
        node.kinders.append(level_3(nodes))
        left_node = node
    return left_node


def level_3(nodes: list) -> Node:
    if nodes[0].op_type == Type.num:
        return nodes.pop(0)

    match(nodes, Type.linke_klammer)
    node = level_1(nodes)
    match(nodes, Type.rechte_klammer)

    return node


def evaluate(node: Node) -> int:
    if node.op_type == Type.num:
        return node.value

    left = evaluate(node.kinders[0])
    right = evaluate(node.kinders[1])

    operation = operationen[node.op_type]
    return operation(left, right)


if __name__ == "__main__":
    s = normalize(input(": "))
    nodes = lex(s)
    node = level_1(nodes)
    match(nodes, Type.end)
    print(evaluate(node))
