"""EVA analysis application.

Modules, by responsibility:
    data_source   - reading the raw data file
    preparation   - validating raw records and converting them to EvaRecords
    models        - the EvaRecord type shared by preparation and analysis
    analysis      - calculations over EvaRecords (no I/O)
    presentation  - plots and text output
    user_input    - prompting the user and parsing what they type
    app           - coordinating the above
"""
