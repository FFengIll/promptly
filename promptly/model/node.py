from typing import List


class NodeType:
    def __init__(self, *args):
        pass


message = NodeType("role", ["dropdown", "text"])
runner = NodeType("runner", ["output"])


class Node:
    id: str
    components: List["Component"]

    def __init__(self):
        self.prev = None
        self.post = None

    def chain(self):
        """
        FIXME: here assume it is only a sequence chain (not tree or graph)

        search all nodes related in current one, to build a chain

        and of course, here should be one node to run

        :return:
        """

        prev = []
        post = []
        from promptly.model.graph import Chain

        chain = Chain()

        for n in post:
            if n.runable():
                chain.run = n.runable
                break

        return chain
