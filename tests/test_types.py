import pytest

from mcp.types import (
    LATEST_PROTOCOL_VERSION,
    ClientRequest,
    JSONRPCMessage,
    JSONRPCRequest,
    Tool,
    ToolAnnotations,
)


@pytest.mark.anyio
async def test_jsonrpc_request():
    json_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": LATEST_PROTOCOL_VERSION,
            "capabilities": {"batch": None, "sampling": None},
            "clientInfo": {"name": "mcp", "version": "0.1.0"},
        },
    }

    request = JSONRPCMessage.model_validate(json_data)
    assert isinstance(request.root, JSONRPCRequest)
    ClientRequest.model_validate(request.model_dump(by_alias=True, exclude_none=True))

    assert request.root.jsonrpc == "2.0"
    assert request.root.id == 1
    assert request.root.method == "initialize"
    assert request.root.params is not None
    assert request.root.params["protocolVersion"] == LATEST_PROTOCOL_VERSION


def test_tool_annotations():
    annotations = ToolAnnotations(
        title="Echo Tool",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    )
    echo_tool = Tool(
        name="echo",
        inputSchema={"type": "object"},
        annotations=annotations,
    )
    assert echo_tool.annotations.title == "Echo Tool"
    assert echo_tool.annotations.readOnlyHint is True
    assert echo_tool.annotations.destructiveHint is False
    assert echo_tool.annotations.idempotentHint is True
    assert echo_tool.annotations.openWorldHint is False

    data = echo_tool.model_dump()
    assert "annotations" in data
    assert data["annotations"]["title"] == "Echo Tool"
    assert data["annotations"]["readOnlyHint"]
    assert not data["annotations"]["destructiveHint"]
    assert data["annotations"]["idempotentHint"]
    assert not data["annotations"]["openWorldHint"]
