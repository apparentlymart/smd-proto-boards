
import os.path
import sexpdata
from sexpdata import Symbol

class Footprint(object):
    def __init__(self, name):
        self.name = name
        self.pin1_label_pos = (0, 0)
        self.pads = []

    def add_pad(self, x, y, w, h):
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

        def pad_sexp(num, x, y, w, h):
            return [
                Symbol("pad"),
                num,
                Symbol("smd"),
                Symbol("rect"),
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
            [
                Symbol("fp_circle"),
                [
                    Symbol("center"),
                    self.pin1_label_pos[0],
                    self.pin1_label_pos[1],
                ],
                [
                    Symbol("end"),
                    self.pin1_label_pos[0] + 0.15,
                    self.pin1_label_pos[1] + 0.15,
                ],
                [Symbol("layer"), Symbol("F.SilkS")],
            ]
        ]

        for num, pad in enumerate(self.pads):
            sexp.append(pad_sexp(num + 1, *pad))

        return sexp


def make_quad48_footprint(name, pitch, pad_width, row_spacing):
    fp = Footprint(name)
    pad_array_width = 11.0 * float(pitch)
    pad_length = 1.73

    fp.pin1_label_pos = (-row_spacing / 2.0, -row_spacing / 2.0)

    def ext_pad_length(i):
        return (
            (pitch / 2.0) +
            (pad_width / 2.0) +
            pad_array_width +
            (row_spacing - pad_array_width) / 2 -
            (i + 1) * pitch
        )

    # Left row, pins 1-12
    for i in xrange(0, 12):
        fp.add_pad(
            -row_spacing / 2.0, (-pad_array_width / 2.0) + (float(i) * pitch),
            pad_length, pad_width,
        )

    # Bottom row, pins 13-24
    for i in xrange(0, 12):
        fp.add_pad(
            (-pad_array_width / 2.0) + (float(i) * pitch),
            pitch / 2.0 - ext_pad_length(i) / 2 + row_spacing / 2.0,
            pad_width, ext_pad_length(i),
        )

    # Right row, pins 25-36
    for i in xrange(11, -1, -1):
        fp.add_pad(
            pitch / 2.0 - ext_pad_length(i) / 2 + row_spacing / 2.0,
            (-pad_array_width / 2.0) + (float(i) * pitch),
            ext_pad_length(i), pad_width,
        )

    # Top row, pins 37-48
    for i in xrange(11, -1, -1):
        fp.add_pad(
            (-pad_array_width / 2.0) + (float(i) * pitch), -row_spacing / 2,
            pad_width, pad_length,
        )

    return fp


footprints = [
    make_quad48_footprint("PROTOQFP", 0.8, 0.5, 13.03),
    make_quad48_footprint("PROTOTQFP", 0.5, 0.3, 9.4),
]

for footprint in footprints:
    outf = open(footprint.filename, 'w')
    # sexpdata's s-expression format doesn't quite agree with KiCad's, so
    # we need to un-escape the periods in the layer names as we save.
    outf.write(
        sexpdata.dumps(footprint.as_sexp).replace("\.", ".")
    )
