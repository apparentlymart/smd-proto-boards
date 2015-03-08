
import os.path
import sexpdata
from sexpdata import Symbol

class Footprint(object):
    def __init__(self, name):
        self.name = name
        self.pads = []

    def add_pad(x, y, w, h):
        self.pads.append((x, y, w, h))

    @property
    def filename(self):
        return os.path.join(
            os.path.dirname(__file__),
            "%s.kicad_mod" % self.name,
        )

    @property
    def as_sexp(self):
        def fp_text_sexp(text_type, text, x, y, layer):
            return [
                Symbol("fp_text"),
                Symbol(text_type),
                Symbol(text),
                [Symbol("at"), x, y],
                [Symbol("layer"), Symbol(layer)],
                [
                    Symbol("effects"),
                    [
                        Symbol("font"),
                        [Symbol("size"), 1, 1],
                        [Symbol("thickness"), 0.15],
                    ]
                ]
            ]

        def pad_sexp(x, y, w, h):
            return [
                Symbol("pad"),
                1,
                Symbol("smd"),
                [Symbol("at"), x, y],
                [Symbol("size"), w, h],
                [
                    Symbol("layers"),
                    Symbol("F.Cu"),
                    Symbol("F.Paste"),
                    Symbol("F.Mask"),
                ]
            ]

        sexp = [
            Symbol("module"),
            Symbol(self.name),
            [Symbol("layer"), Symbol("F.Cu")],
            [Symbol("tedit"), Symbol("54FBEBDA")],
            fp_text_sexp("reference", "REF**", 0, -7.62, "F.SilkS"),
            fp_text_sexp("value", self.name, 0, 5.08, "F.Fab"),
        ]

        for pad in self.pads:
            sexp.append(pad_sexp(*pad))

        return sexp


tqfp = Footprint("PROTOTQFP")
outf = open(tqfp.filename, 'w')
sexpdata.dump(tqfp.as_sexp, outf)

qfp = Footprint("PROTOQFP")
outf = open(qfp.filename, 'w')
sexpdata.dump(qfp.as_sexp, outf)
