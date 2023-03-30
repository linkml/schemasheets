from schemasheets.schemasheet_datamodel import SchemaSheet

RECORD = "Record"
FIELD = "Field"
METATYPE = "MetaType"
INFO = "Info"
CV = "CV"
PV = "PV"
SDO_MAPPINGS = "schema.org"
WD_MAPPINGS = "wikidata"
DATATYPE = "Datatype"

CASES = [
    (1,
     [
        {
            RECORD: "> class",
            INFO: " description",
            SDO_MAPPINGS: "exact_mappings: {curie_prefix: sdo}",
            WD_MAPPINGS: "exact_mappings"
        },
        {
            RECORD: ">",
            WD_MAPPINGS: "curie_prefix: wd"
        },
      ]
     ),
    (2,
     [
         {RECORD: "> class", FIELD: " slot", INFO: " description"},
     ]
     ),
    (3,
     [
         {METATYPE: "> metatype", INFO: " description"},
     ]
     ),
    (4,
     [
         {CV: "> enum", PV: "permissible_value", INFO: " description"},
     ]
     ),
    (5,
     [
         {DATATYPE: "> type", INFO: " description"},
     ]
     ),
    # unnecessary/incompatible with the latest meta-model
    # (6,
    #  [
    #      {DATATYPE: "> metaslot.type", INFO: " description"},
    #  ]
    #  ),
]

def test_parse_header():
    print()
    for case_id, case in CASES:
        ss = SchemaSheet.from_dictreader(case)
        tc = ss.table_config
        info_cc = tc.columns[INFO]
        assert info_cc.name == INFO
        assert info_cc.maps_to == "description"
        assert info_cc.metaslot is not None
        assert info_cc.metaslot.name == "description"
        if case_id == 1 or case_id == 2:
            assert tc.metatype_column is None
            record_cc = tc.columns[RECORD]
            assert record_cc.name == RECORD
            assert record_cc.maps_to == "class"
            assert record_cc.metaslot is None
            if case_id == 2:
                field_cc = tc.columns[FIELD]
                assert field_cc.name == FIELD
                assert field_cc.maps_to == "slot"
                assert field_cc.metaslot is None
            if case_id == 1:
                sdo_cc = tc.columns[SDO_MAPPINGS]
                assert sdo_cc.name == SDO_MAPPINGS
                assert sdo_cc.maps_to == "exact_mappings"
                assert sdo_cc.metaslot is not None
                assert sdo_cc.metaslot.name == "exact mappings" or\
                    sdo_cc.metaslot.name == "exact_mappings"
                assert sdo_cc.settings.curie_prefix == "sdo"
                wd_cc = tc.columns[WD_MAPPINGS]
                assert wd_cc.name == WD_MAPPINGS
                assert wd_cc.maps_to == "exact_mappings"
                assert wd_cc.metaslot is not None
                assert wd_cc.metaslot.name == "exact mappings" or \
                       wd_cc.metaslot.name == "exact_mappings"
                assert wd_cc.settings.curie_prefix == "wd"
        if case_id == 3:
            assert tc.metatype_column == METATYPE
            record_cc = tc.columns[METATYPE]
            assert record_cc.name == METATYPE
            assert record_cc.maps_to == "metatype"
            assert record_cc.metaslot is None
        if case_id == 4:
            cv_cc = tc.columns[CV]
            assert cv_cc.name == CV
            assert cv_cc.maps_to == "enum"
            assert cv_cc.metaslot is None
            pv_cc = tc.columns[PV]
            assert pv_cc.name == PV
            assert pv_cc.maps_to == "permissible_value"
            assert pv_cc.metaslot is None
        if case_id == 5:
            dt_cc = tc.columns[DATATYPE]
            #print(dt_cc)
            assert dt_cc.name == DATATYPE
            assert dt_cc.maps_to == "type"
            assert dt_cc.metaslot is None
        if case_id == 6:
            # See https://github.com/linkml/schemasheets/issues/75
            dt_cc = tc.columns[DATATYPE]
            assert dt_cc.name == DATATYPE
            assert dt_cc.maps_to == "type"
            assert dt_cc.metaslot is not None
            assert dt_cc.metaslot.name == "type"



