"""Tests that CRUD file remotes."""
import json
import pytest
import uuid

from pulp_smash.pulp3.bindings import monitor_task

from pulpcore.client.pulpcore.exceptions import ApiException


@pytest.mark.parallel
def test_sam_create(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    # Empty SAM
    sam_data = {"name": str(uuid.uuid4())}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert sam.name == sam_data["name"]

    # Just entities
    remote_data = {"name": str(uuid.uuid4()), "url": "http://example.com"}
    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)
    sam_data = {"name": str(uuid.uuid4()), "managed_entities": [remote.pulp_href]}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert sam.managed_entities
    assert len(sam.managed_entities) == 1
    assert sam.managed_entities[0] == remote.pulp_href

    # Just attributes
    attrs = {"name": "newname", "bar": 1, "url": "http://newurl.baz"}
    sam_data = {"name": str(uuid.uuid4()), "managed_attributes": attrs}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert sam.managed_attributes
    assert sam.managed_attributes["name"] == attrs["name"]

    # Both
    attrs = {"name": "newname", "bar": 1, "url": "http://newurl.baz"}
    remote_data = {"name": str(uuid.uuid4()), "url": "http://example.com"}
    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)
    sam_data = {
        "name": str(uuid.uuid4()),
        "managed_attributes": attrs,
        "managed_entities": [remote.pulp_href],
    }
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert sam.managed_attributes
    assert sam.managed_entities


@pytest.mark.parallel
def test_sam_bad_create(shared_attribute_managers_api_client, gen_object_with_cleanup):
    # No name
    sam_data = {}
    with pytest.raises(ApiException) as exc:
        gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert exc.value.status == 400
    err = json.loads(exc.value.body)
    assert "name" in err
    assert any("required" in sub for sub in err["name"])

    # Not JSON attrs
    attrs = "THIS IS NOT JSON"
    sam_data = {"name": str(uuid.uuid4()), "managed_attributes": attrs}
    with pytest.raises(ApiException) as exc:
        gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert exc.value.status == 400
    err = json.loads(exc.value.body)
    assert "managed_attributes" in err
    assert any("Expected" in sub for sub in err["managed_attributes"])

    # Not list[str,] entities
    entities = "THIS IS NOT A LIST"
    sam_data = {"name": str(uuid.uuid4()), "managed_entities": entities}
    with pytest.raises(ApiException) as exc:
        gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert exc.value.status == 400
    err = json.loads(exc.value.body)
    assert "managed_entities" in err
    assert any("Expected" in sub for sub in err["managed_entities"])

    # Nonexistent entity-href
    entities = ["/pulp/api/v3/remotes/file/file/THISISNOTANHREF/"]
    sam_data = {"name": str(uuid.uuid4()), "managed_entities": entities}
    with pytest.raises(ApiException) as exc:
        gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    assert exc.value.status == 400
    err = json.loads(exc.value.body)
    assert "managed_entities" in err
    assert any("URIs not found" in sub for sub in err["managed_entities"])


@pytest.mark.parallel
def test_sam_apply_one(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    attrs = {"url": "https://valid.url", "policy": "on_demand", "retain_repo_versions": 666}
    remote_data = {"name": str(uuid.uuid4()), "url": "http://example.com", "policy": "immediate"}
    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)
    sam_data = {
        "name": str(uuid.uuid4()),
        "managed_attributes": attrs,
        "managed_entities": [remote.pulp_href],
    }
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    monitor_task(shared_attribute_managers_api_client.apply(sam.pulp_href, sam).task)
    chgd_remote = file_remote_api_client.read(remote.pulp_href)
    assert chgd_remote.url == attrs["url"]
    assert chgd_remote.policy == attrs["policy"]


@pytest.mark.parallel
def test_sam_apply_multi(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    attrs = {
        "url": "https://valid.url",
        "policy": "on_demand",
        "retain_repo_versions": 666,
        "bar": "blech",
    }
    remote_1_data = {"name": str(uuid.uuid4()), "url": "http://one.foo", "policy": "immediate"}
    remote_2_data = {"name": str(uuid.uuid4()), "url": "http://two.bar", "policy": "streamed"}

    remote_1 = gen_object_with_cleanup(file_remote_api_client, remote_1_data)
    remote_2 = gen_object_with_cleanup(file_remote_api_client, remote_2_data)
    sam_data = {
        "name": str(uuid.uuid4()),
        "managed_attributes": attrs,
        "managed_entities": [remote_1.pulp_href, remote_2.pulp_href],
    }
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    monitor_task(shared_attribute_managers_api_client.apply(sam.pulp_href, sam).task)
    chgd_remote_1 = file_remote_api_client.read(remote_1.pulp_href)
    chgd_remote_2 = file_remote_api_client.read(remote_2.pulp_href)

    assert chgd_remote_1.url == attrs["url"]
    assert chgd_remote_1.policy == attrs["policy"]
    assert chgd_remote_2.url == attrs["url"]
    assert chgd_remote_2.policy == attrs["policy"]


@pytest.mark.parallel
def test_sam_apply_diff_types(
    shared_attribute_managers_api_client,
    file_remote_api_client,
    file_repo_api_client,
    gen_object_with_cleanup,
):
    attrs = {
        "url": "https://valid.url",
        "policy": "on_demand",
        "retain_repo_versions": 666,
        "bar": "blech",
        "description": "Return of the Jedi",
    }
    remote_data = {"name": str(uuid.uuid4()), "url": "http://one.foo", "policy": "immediate"}
    repo_data = {"name": str(uuid.uuid4()), "description": "A New Hope", "retain_repo_versions": 5}

    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)
    repo = gen_object_with_cleanup(file_repo_api_client, repo_data)
    sam_data = {
        "name": str(uuid.uuid4()),
        "managed_attributes": attrs,
        "managed_entities": [remote.pulp_href, repo.pulp_href],
    }
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    monitor_task(shared_attribute_managers_api_client.apply(sam.pulp_href, sam).task)
    chgd_remote = file_remote_api_client.read(remote.pulp_href)
    chgd_repo = file_repo_api_client.read(repo.pulp_href)

    assert chgd_remote.url == attrs["url"]
    assert chgd_remote.policy == attrs["policy"]
    assert chgd_repo.retain_repo_versions == attrs["retain_repo_versions"]
    assert chgd_repo.description == attrs["description"]


@pytest.mark.parallel
def test_sam_bad_apply(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    attrs = {"url": "https://valid.url", "policy": "on_demand", "retain_repo_versions": 666}
    remote_data = {"name": str(uuid.uuid4()), "url": "http://example.com", "policy": "immediate"}
    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)

    # No attrs
    sam_data = {"name": str(uuid.uuid4()), "managed_entities": [remote.pulp_href]}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    with pytest.raises(ApiException) as exc:
        apply_result = shared_attribute_managers_api_client.apply(sam.pulp_href, sam)
        monitor_task(apply_result.task)
    assert exc.value.status == 400
    assert "attributes" in exc.value.body

    # No entities
    sam_data = {"name": str(uuid.uuid4()), "managed_attributes": attrs}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    with pytest.raises(ApiException) as exc:
        apply_result = shared_attribute_managers_api_client.apply(sam.pulp_href, sam)
        monitor_task(apply_result.task)
    assert exc.value.status == 400
    assert "entities" in exc.value.body

    # Neither
    sam_data = {"name": str(uuid.uuid4())}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    with pytest.raises(ApiException) as exc:
        apply_result = shared_attribute_managers_api_client.apply(sam.pulp_href, sam)
        monitor_task(apply_result.task)
    assert exc.value.status == 400
    assert "attributes" in exc.value.body
    assert "entities" in exc.value.body


@pytest.mark.parallel
def test_sam_add(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    attrs = {
        "url": "https://valid.url",
        "policy": "on_demand",
        "retain_repo_versions": 666,
        "bar": "blech",
    }
    remote_1_data = {"name": str(uuid.uuid4()), "url": "http://one.foo", "policy": "immediate"}
    remote_2_data = {"name": str(uuid.uuid4()), "url": "http://two.bar", "policy": "streamed"}

    remote_1 = gen_object_with_cleanup(file_remote_api_client, remote_1_data)
    remote_2 = gen_object_with_cleanup(file_remote_api_client, remote_2_data)
    sam_data = {
        "name": str(uuid.uuid4()),
        "managed_attributes": attrs,
        "managed_entities": [remote_1.pulp_href],
    }
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    add_result = shared_attribute_managers_api_client.add(
        sam.pulp_href, {"entity_href": remote_2.pulp_href}
    )
    monitor_task(add_result.task)
    new_sam = shared_attribute_managers_api_client.read(sam.pulp_href)
    assert new_sam.managed_entities
    assert 2 == len(new_sam.managed_entities)
    assert remote_2.pulp_href in new_sam.managed_entities


@pytest.mark.parallel
def test_sam_bad_add(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    remote_data = {"name": str(uuid.uuid4()), "url": "http://one.foo", "policy": "immediate"}
    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)

    sam_data = {"name": str(uuid.uuid4()), "managed_entities": [remote.pulp_href]}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)

    # object doesn't exist
    with pytest.raises(ApiException) as exc:
        shared_attribute_managers_api_client.add(sam.pulp_href, {"entity_href": "NOT AN HREF"})
    assert exc.value.status == 400
    assert "Could not find" in exc.value.body

    # object already being managed
    with pytest.raises(ApiException) as exc:
        shared_attribute_managers_api_client.add(sam.pulp_href, {"entity_href": remote.pulp_href})
    assert exc.value.status == 400
    assert "already being managed" in exc.value.body


@pytest.mark.parallel
def test_sam_remove(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    attrs = {
        "url": "https://valid.url",
        "policy": "on_demand",
        "retain_repo_versions": 666,
        "bar": "blech",
    }
    remote_1_data = {"name": str(uuid.uuid4()), "url": "http://one.foo", "policy": "immediate"}
    remote_1 = gen_object_with_cleanup(file_remote_api_client, remote_1_data)
    sam_data = {
        "name": str(uuid.uuid4()),
        "managed_attributes": attrs,
        "managed_entities": [remote_1.pulp_href],
    }
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    rmv_result = shared_attribute_managers_api_client.remove(
        sam.pulp_href, {"entity_href": remote_1.pulp_href}
    )
    assert "Removed" in rmv_result
    new_sam = shared_attribute_managers_api_client.read(sam.pulp_href)
    assert not new_sam.managed_entities


@pytest.mark.parallel
def test_sam_bad_remove(
    shared_attribute_managers_api_client, file_remote_api_client, gen_object_with_cleanup
):
    # not being managed
    remote_1 = gen_object_with_cleanup(
        file_remote_api_client, {"name": str(uuid.uuid4()), "url": "http://one.foo"}
    )
    remote_2 = gen_object_with_cleanup(
        file_remote_api_client, {"name": str(uuid.uuid4()), "url": "http://two.foo"}
    )
    sam_data = {"name": str(uuid.uuid4()), "managed_entities": [remote_1.pulp_href]}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    with pytest.raises(ApiException) as exc:
        shared_attribute_managers_api_client.remove(
            sam.pulp_href, {"entity_href": remote_2.pulp_href}
        )
    assert exc.value.status == 400
    assert "not being managed" in exc.value.body


@pytest.mark.parallel
def test_sam_update(
    shared_attribute_managers_api_client,
    file_remote_api_client,
    file_repo_api_client,
    gen_object_with_cleanup,
):
    attrs = {
        "url": "https://valid.url",
        "policy": "on_demand",
        "retain_repo_versions": 666,
        "bar": "blech",
        "description": "Return of the Jedi",
    }
    remote_data = {"name": str(uuid.uuid4()), "url": "http://one.foo", "policy": "immediate"}
    repo_data = {"name": str(uuid.uuid4()), "description": "A New Hope", "retain_repo_versions": 5}

    remote = gen_object_with_cleanup(file_remote_api_client, remote_data)
    repo = gen_object_with_cleanup(file_repo_api_client, repo_data)

    # Set attrs
    sam_data = {"name": str(uuid.uuid4()), "managed_entities": [remote.pulp_href, repo.pulp_href]}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    sam.managed_attributes = attrs
    upd_result = shared_attribute_managers_api_client.update(sam.pulp_href, sam)
    assert upd_result.managed_attributes == attrs
    new_sam = shared_attribute_managers_api_client.read(sam.pulp_href)
    assert new_sam.managed_attributes == attrs

    # Set entities
    second_attrs = {
        "url": "https://second.url",
        "policy": "on_demand",
        "retain_repo_versions": 555,
        "bar": "blech",
        "description": "Empire Strikes Back",
    }
    sam_data = {"name": str(uuid.uuid4()), "managed_attributes": second_attrs}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    sam.managed_entities = [remote.pulp_href, repo.pulp_href]
    upd_result = shared_attribute_managers_api_client.update(sam.pulp_href, sam)
    assert upd_result.managed_entities == [remote.pulp_href, repo.pulp_href]
    new_sam = shared_attribute_managers_api_client.read(sam.pulp_href)
    assert new_sam.managed_entities == [remote.pulp_href, repo.pulp_href]


@pytest.mark.parallel
def test_sam_delete(shared_attribute_managers_api_client, gen_object_with_cleanup):
    sam_data = {"name": str(uuid.uuid4())}
    sam = gen_object_with_cleanup(shared_attribute_managers_api_client, sam_data)
    try:
        shared_attribute_managers_api_client.delete(sam.pulp_href)
    except Exception as exc:
        raise pytest.fail("raised exception {0}".format(exc))
