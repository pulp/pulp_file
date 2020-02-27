from pulp_file.tests.functional.utils.s3 import create_bucket


def pytest_runtest_setup(item):
    """Create bucket if needed."""
    create_bucket()
