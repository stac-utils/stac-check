from stac_check.lint import Linter


def test_geometry_coordinates_order():
    """Test the check_geometry_coordinates_order method for detecting potentially incorrectly ordered coordinates."""
    # Create a test item with coordinates in the correct order (longitude, latitude)
    correct_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-correct",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [10.0, -10.0],  # lon, lat
                    [20.0, -10.0],
                    [20.0, 10.0],
                    [10.0, 10.0],
                    [10.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with coordinates in the wrong order (latitude, longitude)
    # but with values that don't trigger the validation checks
    undetectable_reversed_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-undetectable-reversed",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-10.0, 10.0],  # lat, lon (reversed) but within valid ranges
                    [-10.0, 20.0],
                    [10.0, 20.0],
                    [10.0, 10.0],
                    [-10.0, 10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with coordinates that are clearly reversed (latitude > 90)
    clearly_incorrect_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-clearly-incorrect",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [10.0, 100.0],  # Second value (latitude) > 90
                    [20.0, 100.0],
                    [20.0, 100.0],
                    [10.0, 100.0],
                    [10.0, 100.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with coordinates that may be reversed based on heuristic
    # (first value > 90, second value < 90, first value > second value*2)
    heuristic_incorrect_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-coordinates-heuristic-incorrect",
        "bbox": [10.0, -10.0, 20.0, 10.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [120.0, 40.0],  # First value > 90, second < 90, first > second*2
                    [120.0, 40.0],
                    [120.0, 40.0],
                    [120.0, 40.0],
                    [120.0, 40.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Test with correct coordinates - this should pass both checks
    linter = Linter(correct_item)
    assert linter.check_geometry_coordinates_order() == True
    assert linter.check_geometry_coordinates_definite_errors() == True

    # Test with reversed coordinates that are within valid ranges
    # Current implementation can't detect this case, so both checks pass
    linter = Linter(undetectable_reversed_item)
    assert (
        linter.check_geometry_coordinates_order() == True
    )  # Passes because values are within valid ranges
    assert (
        linter.check_geometry_coordinates_definite_errors() == True
    )  # Passes because values are within valid ranges

    # Test with clearly incorrect coordinates (latitude > 90)
    # This should fail the definite errors check but pass the order check (which now only uses heuristic)
    linter = Linter(clearly_incorrect_item)
    assert (
        linter.check_geometry_coordinates_order() == True
    )  # Now passes because it only checks heuristic

    # Check that definite errors are detected
    result = linter.check_geometry_coordinates_definite_errors()
    assert result is not True  # Should not be True
    assert isinstance(result, tuple)  # Should be a tuple
    assert result[0] is False  # First element should be False
    assert len(result[1]) > 0  # Should have at least one invalid coordinate
    assert result[1][0][1] == 100.0  # The latitude value should be 100.0
    assert "latitude > ±90°" in result[1][0][2]  # Should indicate latitude error

    # Test with coordinates that trigger the heuristic
    # This should fail the order check but pass the definite errors check
    linter = Linter(heuristic_incorrect_item)
    assert (
        linter.check_geometry_coordinates_order() == False
    )  # Fails because of heuristic
    assert (
        linter.check_geometry_coordinates_definite_errors() == True
    )  # Passes because values are within valid ranges

    # Test that the best practices dictionary contains the appropriate error messages
    best_practices = linter.create_best_practices_dict()

    # For heuristic-based detection
    linter = Linter(heuristic_incorrect_item)
    best_practices = linter.create_best_practices_dict()
    assert "geometry_coordinates_order" in best_practices
    assert (
        "may be in the wrong order" in best_practices["geometry_coordinates_order"][0]
    )

    # For definite errors detection
    linter = Linter(clearly_incorrect_item)
    best_practices = linter.create_best_practices_dict()
    assert "geometry_coordinates_definite_errors" in best_practices
    assert (
        "contain invalid values"
        in best_practices["geometry_coordinates_definite_errors"][0]
    )


def test_bbox_antimeridian():
    """Test the check_bbox_antimeridian method for detecting incorrectly formatted bboxes that cross the antimeridian."""
    # Create a test item with an incorrectly formatted bbox that belts the globe
    # instead of properly crossing the antimeridian
    incorrect_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-antimeridian-incorrect",
        "bbox": [
            -170.0,  # west
            -10.0,  # south
            170.0,  # east (incorrect: this belts the globe instead of crossing the antimeridian)
            10.0,  # north
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [170.0, -10.0],
                    [-170.0, -10.0],
                    [-170.0, 10.0],
                    [170.0, 10.0],
                    [170.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Create a test item with a correctly formatted bbox that crosses the antimeridian
    # (west > east for antimeridian crossing)
    correct_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-antimeridian-correct",
        "bbox": [
            170.0,  # west
            -10.0,  # south
            -170.0,  # east (west > east indicates antimeridian crossing)
            10.0,  # north
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [170.0, -10.0],
                    [-170.0, -10.0],
                    [-170.0, 10.0],
                    [170.0, 10.0],
                    [170.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Test with the incorrect item (belting the globe)
    linter = Linter(incorrect_item)
    # The check should return False for the incorrectly formatted bbox
    assert linter.check_bbox_antimeridian() == False

    # Verify that the best practices dictionary contains the appropriate message
    best_practices = linter.create_best_practices_dict()
    assert "check_bbox_antimeridian" in best_practices
    assert len(best_practices["check_bbox_antimeridian"]) == 2

    # Check that the error messages include the west and east longitude values
    west_val = incorrect_item["bbox"][0]
    east_val = incorrect_item["bbox"][2]
    assert (
        f"(found west={west_val}, east={east_val})"
        in best_practices["check_bbox_antimeridian"][0]
    )

    # Test with the correct item - this should pass
    linter = Linter(correct_item)
    # The check should return True for the correctly formatted bbox
    assert linter.check_bbox_antimeridian() == True

    # Test with a normal bbox that doesn't cross the antimeridian
    normal_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-normal-bbox",
        "bbox": [10.0, -10.0, 20.0, 10.0],  # west  # south  # east  # north
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [10.0, -10.0],
                    [20.0, -10.0],
                    [20.0, 10.0],
                    [10.0, 10.0],
                    [10.0, -10.0],
                ]
            ],
        },
        "properties": {"datetime": "2023-01-01T00:00:00Z"},
    }

    # Test with a normal bbox - this should pass
    linter = Linter(normal_item)
    assert linter.check_bbox_antimeridian() == True


def test_bbox_matches_geometry():
    # Test with matching bbox and geometry
    file = "sample_files/1.0.0/core-item.json"
    linter = Linter(file)
    assert linter.check_bbox_matches_geometry() is True

    # Test with mismatched bbox and geometry
    mismatched_item = {
        "stac_version": "1.0.0",
        "stac_extensions": [],
        "type": "Feature",
        "id": "test-item",
        "bbox": [100.0, 0.0, 105.0, 1.0],  # Deliberately wrong bbox
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [172.91173669923782, 1.3438851951615003],
                    [172.95469614953714, 1.3438851951615003],
                    [172.95469614953714, 1.3690476620161975],
                    [172.91173669923782, 1.3690476620161975],
                    [172.91173669923782, 1.3438851951615003],
                ]
            ],
        },
        "properties": {"datetime": "2020-12-11T22:38:32.125Z"},
    }
    linter = Linter(mismatched_item)
    result = linter.check_bbox_matches_geometry()

    # Check that the result is a tuple and the first element is False
    assert isinstance(result, tuple)
    assert result[0] is False

    # Check that the tuple contains the expected elements (calculated bbox, actual bbox, differences)
    assert len(result) == 4
    calc_bbox, actual_bbox, differences = result[1], result[2], result[3]

    # Verify the calculated bbox matches the geometry coordinates
    assert calc_bbox == [
        172.91173669923782,
        1.3438851951615003,
        172.95469614953714,
        1.3690476620161975,
    ]

    # Verify the actual bbox is what we provided
    assert actual_bbox == [100.0, 0.0, 105.0, 1.0]

    # Verify the differences are calculated correctly
    expected_differences = [abs(actual_bbox[i] - calc_bbox[i]) for i in range(4)]
    assert differences == expected_differences

    # Test with null geometry (should return True as check is not applicable)
    null_geom_item = {
        "stac_version": "1.0.0",
        "type": "Feature",
        "id": "test-item-null-geom",
        "bbox": [100.0, 0.0, 105.0, 1.0],
        "geometry": None,
        "properties": {"datetime": "2020-12-11T22:38:32.125Z"},
    }
    linter = Linter(null_geom_item)
    assert linter.check_bbox_matches_geometry() is True

    # Test with missing bbox (should return True as check is not applicable)
    no_bbox_item = {
        "stac_version": "1.0.0",
        "type": "Feature",
        "id": "test-item-no-bbox",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [172.91173669923782, 1.3438851951615003],
                    [172.95469614953714, 1.3438851951615003],
                    [172.95469614953714, 1.3690476620161975],
                    [172.91173669923782, 1.3690476620161975],
                    [172.91173669923782, 1.3438851951615003],
                ]
            ],
        },
        "properties": {"datetime": "2020-12-11T22:38:32.125Z"},
    }
    linter = Linter(no_bbox_item)
    assert linter.check_bbox_matches_geometry() is True
