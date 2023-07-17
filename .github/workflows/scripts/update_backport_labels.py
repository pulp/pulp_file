# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_file' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

import requests
import yaml
import random
import os


def random_color():
    """Generates a random 24-bit number in hex"""
    color = random.randrange(0, 2**24)
    return format(color, "06x")


session = requests.Session()
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
session.headers.update(headers)

# get all labels from the repository's current state
response = session.get("https://api.github.com/repos/pulp/pulp_file/labels", headers=headers)
assert response.status_code == 200
old_labels = set([x["name"] for x in response.json() if x["name"].startswith("backport-")])

# get ci_update_branches from template_config.yml
with open("./template_config.yml", "r") as f:
    plugin_template = yaml.safe_load(f)
new_labels = set(["backport-" + x for x in plugin_template["ci_update_branches"]])

# delete old labels that are not in new labels
for label in old_labels.difference(new_labels):
    response = session.delete(
        f"https://api.github.com/repos/pulp/pulp_file/labels/{label}", headers=headers
    )
    assert response.status_code == 204

# create new labels that are not in old labels
for label in new_labels.difference(old_labels):
    color = random_color()
    response = session.post(
        "https://api.github.com/repos/pulp/pulp_file/labels",
        headers=headers,
        json={"name": label, "color": color},
    )
    assert response.status_code == 201
