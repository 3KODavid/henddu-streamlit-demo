from src.data.readers.boundaries_reader import should_use_shapefile


def test_should_use_shapefile_keeps_primary_admin_layers() -> None:
    assert should_use_shapefile("civ_admin1")
    assert should_use_shapefile("civ_admin2")
    assert not should_use_shapefile("civ_admin1_em")
    assert not should_use_shapefile("civ_admin3")
