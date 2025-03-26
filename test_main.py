from main import process_cities


def test_process_cities_with_non_existing_file():
    try:
        ret = process_cities('tests/no_such_file.csv', 'out/uscities_neighbors.csv', 50, False)
        assert ret == 1, 'Should return 1 for file not found'
    except Exception as e:
        assert False, f'Should not throw exception: {e}'


def test_process_cities_with_empty():
    try:
        ret = process_cities('tests/empty', 'out/uscities_neighbors.csv', 50, False)
        assert ret == 2, 'Should return 2 for empty file'
    except Exception as e:
        assert False, f'Should not throw exception: {e}'


def test_process_cities_with_bad_input():
    try:
        ret = process_cities('tests/error.csv', 'out/uscities_neighbors.csv', 50, False)
        assert ret == 3, 'Should return 3 for malformed file'
    except Exception as e:
        assert False, f'Should not throw exception: {e}'


def test_process_cities_with_missing_columns():
    try:
        ret = process_cities('tests/missing.csv', 'out/uscities_neighbors.csv', 50, False)
        assert ret == 4, 'Should return 4 for missing columns'
    except Exception as e:
        assert False, f'Should not throw exception: {e}'


def test_process_cities_with_bad_output_file():
    try:
        ret = process_cities('assets/uscities.csv', '/:should_not_be_able_to_create.csv', 50, False)
        assert ret == 6, 'Should return 6 for output errors'
    except Exception as e:
        assert False, f'Should not throw exception: {e}'
