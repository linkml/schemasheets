from schemasheets.schemasheet_datamodel import SchemaSheet

CASES = [
    (6,
     [
         {"Datatype": "> metaslot.type", "Info": " description"},
     ]
     ),
]


def test_parse_header():
    print()
    for case_id, case in CASES:
        ss = SchemaSheet.from_dictreader(case)

# OK up to LinkML 1.4.11
# but in 1.5.0
#             if self.maps_to.startswith("metaslot."):
#                 maps_to = self.maps_to.replace("metaslot.", "")
# >               self.metaslot = snmap[maps_to]
# E               KeyError: 'type'
#
# schemasheets/schemasheet_datamodel.py:102: KeyError
