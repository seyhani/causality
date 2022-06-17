from expression_parser import Tree, Variable, Exponent, Plus, Times, Node
from event_structure import ES


def parse_tree(node: Node) -> ES:
    if isinstance(node, Variable):
        return ES().prefix(node.name)
    else:
        root = node
        if isinstance(node, Tree):
            root = node.root
        if isinstance(root, Variable):
            return parse_tree(root)
        left = parse_tree(root.left)
        right = parse_tree(root.right)
        if isinstance(root, Exponent):
            return left.product(right)
        elif isinstance(root, Plus):
            return right.sum(left)
        elif isinstance(root, Times):
            return right.prefix(root.left.name)
        else:
            raise Exception("Unknown node")


class ProcessParser:
    def parse(self, expression) -> ES:
        tree = Tree()
        tree.parse(expression)
        return parse_tree(tree)
