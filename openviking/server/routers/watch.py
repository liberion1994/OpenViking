# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0
"""Watch task management endpoints for OpenViking HTTP Server."""

from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict

from openviking.server.auth import get_request_context
from openviking.server.dependencies import get_service
from openviking.server.identity import RequestContext
from openviking.server.models import Response

router = APIRouter(prefix="/api/v1/watch", tags=["watch"])


class UpdateWatchTaskRequest(BaseModel):
    """Request model for watch task update."""

    model_config = ConfigDict(extra="forbid")

    path: Optional[str] = None
    to_uri: Optional[str] = None
    parent_uri: Optional[str] = None
    reason: Optional[str] = None
    instruction: Optional[str] = None
    watch_interval: Optional[float] = None
    build_index: Optional[bool] = None
    summarize: Optional[bool] = None
    processor_kwargs: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


@router.get("/tasks")
async def list_watch_tasks(
    active_only: bool = Query(False, description="Only return active watch tasks"),
    _ctx: RequestContext = Depends(get_request_context),
):
    """List watch tasks visible to the current caller."""
    service = get_service()
    result = await service.resources.list_watch_tasks(ctx=_ctx, active_only=active_only)
    return Response(status="ok", result=result).model_dump(exclude_none=True)


@router.get("/tasks/by-uri")
async def get_watch_task_by_uri(
    to_uri: str = Query(..., description="Target URI bound to the watch task"),
    _ctx: RequestContext = Depends(get_request_context),
):
    """Get a watch task by target URI."""
    service = get_service()
    result = await service.resources.get_watch_task_by_uri(to_uri=to_uri, ctx=_ctx)
    return Response(status="ok", result=result).model_dump(exclude_none=True)


@router.get("/tasks/{task_id}")
async def get_watch_task(
    task_id: str,
    _ctx: RequestContext = Depends(get_request_context),
):
    """Get a watch task by task ID."""
    service = get_service()
    result = await service.resources.get_watch_task(task_id=task_id, ctx=_ctx)
    return Response(status="ok", result=result).model_dump(exclude_none=True)


@router.patch("/tasks/{task_id}")
async def update_watch_task(
    task_id: str,
    request: UpdateWatchTaskRequest,
    _ctx: RequestContext = Depends(get_request_context),
):
    """Update a watch task."""
    service = get_service()
    result = await service.resources.update_watch_task(
        task_id=task_id,
        ctx=_ctx,
        **request.model_dump(exclude_none=True),
    )
    return Response(status="ok", result=result).model_dump(exclude_none=True)


@router.delete("/tasks/{task_id}")
async def delete_watch_task(
    task_id: str,
    _ctx: RequestContext = Depends(get_request_context),
):
    """Delete a watch task."""
    service = get_service()
    result = await service.resources.delete_watch_task(task_id=task_id, ctx=_ctx)
    return Response(status="ok", result={"deleted": result, "task_id": task_id}).model_dump(
        exclude_none=True
    )
