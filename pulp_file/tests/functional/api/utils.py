# coding=utf-8
"""Utilities for file plugin tests."""
from pulp_smash import utils
from pulp_smash.pulp3.utils import get_content


def gen_publisher(**kwargs):
    """Return a semi-random dict for use in creating a publisher."""
    data = {'name': utils.uuid4()}
    data.update(kwargs)
    return data


def get_content_unit_paths(repo):
    """Return the relative path of content units present in a file repository.

    :param repo: A dict of information about the repository.
    :returns: A list with the paths of units present in a given repository.
    """
    # The "relative_path" is actually a file path and name
    return [content_unit['relative_path'] for content_unit in get_content(repo)]
