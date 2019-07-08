import numpy as np
import matplotlib.pyplot as plt

# x, y ,z => so far content spreads across x-dimension
origin = 0
nodes = []
count = 0
# node


# Creates Node with any number of key, values 
# adds a dimension 
class Node:
    def __init__(self, **kwargs):
        global origin
        for attr in kwargs.keys():
            self.__dict__[attr] = kwargs[attr]
        self.dimension = np.linspace(0, 100, len(list(kwargs)))

# list holds all nodes in order, starting from 0 = Origin
nodes = []
def create(**kwargs):
    o = Node(**kwargs)
    nodes.append(o)
    return "Node created"

create(a='mathemathics', b='physics', c='chemistry', d='music', x = 'python', u = 'bash')
create(a='calendar', b='unity', c='webapp', d='flask', x = 'cerati', u = 'campo')


def plot():
    fig, ax = plt.subplots()
    count = 0
    for node in nodes:
        contents = []
        for txt in node.__dict__.values():
            if str(txt) != 'dimension':
                contents.append(txt)

        indexes = [count for i in node.dimension]
        heights = node.dimension
        ax.scatter(heights, indexes)
        for h, i, txt in zip(heights, indexes, contents):
            ax.annotate(txt, (h,i))
            ax.annotate(txt, (h,i))
        count += 1
    plt.title("Mind-Map")
    plt.show()

