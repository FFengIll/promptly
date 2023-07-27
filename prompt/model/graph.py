from typing import List, Any

from prompt.model.node import Node


class Component:
    id: int
    value: Any


class Graph:
    nodes: List[Node]

    def json(self):
        pass

    def is_empty(self):
        pass

    def from_template(self, template: type):
        pass

    def lookup_node(self, node):
        for n in self.nodes:
            if n.id == node:
                return n
        return None

    def update(self, node, id, value):
        # FIXME: may no such id
        n = self.lookup_node(node)
        for c in n.components:
            if c.id == id:
                c.value = value
                break
        return True

    def action(self, node, name):
        n = self.lookup_node(node)

        match name:
            case "run":
                pass

    def run(self, node: Node):
        chain = node.chain()

        data = chain.json()
        res = chain.run(data)

        return res


class Chain:
    def __init__(self):
        pass

    def __default_run(self):
        pass

    def run(self):
        return self.__default_run()
