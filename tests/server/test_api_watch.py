# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Tests for watch task management endpoints."""


async def _create_watch_task(client, sample_markdown_file):
    resp = await client.post(
        "/api/v1/resources",
        json={
            "temp_file_id": sample_markdown_file.name,
            "to": "viking://resources/watch-test",
            "watch_interval": 30.0,
        },
    )
    assert resp.status_code == 200


async def test_list_watch_tasks(
    client,
    sample_markdown_file,
    upload_temp_dir,
):
    await _create_watch_task(client, sample_markdown_file)

    resp = await client.get("/api/v1/watch/tasks")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert len(body["result"]) == 1
    assert body["result"][0]["to_uri"] == "viking://resources/watch-test"


async def test_get_watch_task_by_uri(
    client,
    sample_markdown_file,
    upload_temp_dir,
):
    await _create_watch_task(client, sample_markdown_file)

    resp = await client.get(
        "/api/v1/watch/tasks/by-uri",
        params={"to_uri": "viking://resources/watch-test"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["result"]["watch_interval"] == 30.0


async def test_update_watch_task(
    client,
    sample_markdown_file,
    upload_temp_dir,
):
    await _create_watch_task(client, sample_markdown_file)

    list_resp = await client.get("/api/v1/watch/tasks")
    task_id = list_resp.json()["result"][0]["task_id"]

    resp = await client.patch(
        f"/api/v1/watch/tasks/{task_id}",
        json={
            "watch_interval": 45.0,
            "reason": "updated watch",
            "is_active": True,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["result"]["watch_interval"] == 45.0
    assert body["result"]["reason"] == "updated watch"


async def test_delete_watch_task(
    client,
    sample_markdown_file,
    upload_temp_dir,
):
    await _create_watch_task(client, sample_markdown_file)

    list_resp = await client.get("/api/v1/watch/tasks")
    task_id = list_resp.json()["result"][0]["task_id"]

    resp = await client.delete(f"/api/v1/watch/tasks/{task_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["result"]["deleted"] is True

    list_resp = await client.get("/api/v1/watch/tasks")
    assert list_resp.status_code == 200
    assert list_resp.json()["result"] == []
