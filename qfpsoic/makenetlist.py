
# requires the "sexpdata" package from PyPI.

import sexpdata
import pprint
from sexpdata import Symbol

inf = open("qfpsoic.net.template", "r")
netlist_tree = sexpdata.load(inf)

nets = []

for i in xrange(1, 49):
    net = [
        Symbol('net'),
        [Symbol('code'), i],
        [Symbol('name'), 'PIN%i' % i],
        [
            Symbol('node'),
            [Symbol('ref'), Symbol('P1' if i < 25 else 'P2')],
            [Symbol('pin'), ((i - 1) % 24) + 1],
        ],
        [
            Symbol('node'),
            [Symbol('ref'), Symbol('U1')],
            [Symbol('pin'), i],
        ],
        [
            Symbol('node'),
            [Symbol('ref'), Symbol('U2')],
            [Symbol('pin'), i],
        ],
    ]

    nets.append(net)

def fill_template(node):
    if type(node[0]) is Symbol and node[0].value() == 'nets':
        #pprint.pprint(node)
        node[1:] = nets
    else:
        for child_item in node:
            if type(child_item) is list:
                fill_template(child_item)


fill_template(netlist_tree)

outf = open("qfpsoic.net", "w")
sexpdata.dump(netlist_tree, outf)

