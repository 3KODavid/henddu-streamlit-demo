from src.data.readers.cams_reader import CamsReader


def test_cams_reader_metadata_has_source_key() -> None:
    reader = CamsReader.__new__(CamsReader)
    frame = CamsReader.load_metadata(reader)
    assert frame.iloc[0]["source"] == "cams_reanalysis"


def test_cams_reader_maps_pm25_variable_name() -> None:
    reader = CamsReader.__new__(CamsReader)
    assert CamsReader.get_variable_name(reader, "PM2.5") == "pm2p5"
