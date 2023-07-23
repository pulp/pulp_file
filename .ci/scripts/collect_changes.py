# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_file' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

import itertools
import os
import re

import toml
from git import GitCommandError, Repo
from pkg_resources import parse_version

# Read Towncrier settings
tc_settings = toml.load("pyproject.toml")["tool"]["towncrier"]

CHANGELOG_FILE = tc_settings.get("filename", "NEWS.rst")
START_STRING = tc_settings.get(
    "start_string",
    "<!-- towncrier release notes start -->\n"
    if CHANGELOG_FILE.endswith(".md")
    else ".. towncrier release notes start\n",
)
TITLE_FORMAT = tc_settings.get("title_format", "{name} {version} ({project_date})")


NAME_REGEX = r".*"
VERSION_REGEX = r"([0-9]+\.[0-9]+\.[0-9][0-9ab]*)"
DATE_REGEX = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
TITLE_REGEX = (
    "("
    + re.escape(
        TITLE_FORMAT.format(name="NAME_REGEX", version="VERSION_REGEX", project_date="DATE_REGEX")
    )
    .replace("NAME_REGEX", NAME_REGEX)
    .replace("VERSION_REGEX", VERSION_REGEX)
    .replace("DATE_REGEX", DATE_REGEX)
    + ")"
)


def get_changelog(repo, branch):
    return repo.git.show(f"{branch}:{CHANGELOG_FILE}") + "\n"


def _tokenize_changes(splits):
    assert len(splits) % 3 == 0
    for i in range(len(splits) // 3):
        title = splits[3 * i]
        version = parse_version(splits[3 * i + 1])
        yield [version, title + splits[3 * i + 2]]


def split_changelog(changelog):
    preamble, rest = changelog.split(START_STRING, maxsplit=1)
    split_rest = re.split(TITLE_REGEX, rest)
    return preamble + START_STRING + split_rest[0], list(_tokenize_changes(split_rest[1:]))


def main():
    repo = Repo(os.getcwd())
    remote = repo.remotes[0]
    branches = [ref for ref in remote.refs if re.match(r"^([0-9]+)\.([0-9]+)$", ref.remote_head)]
    branches.sort(key=lambda ref: parse_version(ref.remote_head), reverse=True)
    branches = [ref.name for ref in branches]

    with open(CHANGELOG_FILE, "r") as f:
        main_changelog = f.read()
    preamble, main_changes = split_changelog(main_changelog)
    old_length = len(main_changes)

    for branch in branches:
        print(f"Looking at branch {branch}")
        try:
            changelog = get_changelog(repo, branch)
        except GitCommandError:
            print("No changelog found on this branch.")
            continue
        dummy, changes = split_changelog(changelog)
        new_changes = sorted(main_changes + changes, key=lambda x: x[0], reverse=True)
        # Now remove duplicates (retain the first one)
        main_changes = [new_changes[0]]
        for left, right in itertools.pairwise(new_changes):
            if left[0] != right[0]:
                main_changes.append(right)

    new_length = len(main_changes)
    if old_length < new_length:
        print(f"{new_length - old_length} new versions have been added.")
        with open(CHANGELOG_FILE, "w") as fp:
            fp.write(preamble)
            for change in main_changes:
                fp.write(change[1])

        repo.git.commit("-m", "Update Changelog", "-m" "[noissue]", CHANGELOG_FILE)


if __name__ == "__main__":
    main()
