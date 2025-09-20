#!/usr/bin/env python3
"""HTTP MCP server exposing Mac control tools for ChatGPT.

This module hosts a Model Context Protocol (MCP) server that speaks the
JSON-RPC-over-SSE transport expected by ChatGPT.  The server exposes a
handful of automation primitives for Mac control.

Two HTTP endpoints are provided:

``GET /sse``
    Establishes the Server-Sent Events stream used to push JSON-RPC
    responses back to ChatGPT.  The initial event sent on the stream tells
    the client where to POST subsequent JSON-RPC requests.

``POST /message?session_id=...``
    Receives JSON-RPC requests from ChatGPT for the corresponding SSE
    session.  Each request is validated and dispatched through the MCP
    runtime.

``HEAD /message``
    Returns 200 OK for ChatGPT validation checks.

The :func:`create_app` helper exposes the underlying Starlette ASGI
application so the server can be run by any ASGI-capable host.  When run as
``__main__`` this script starts an embedded Uvicorn instance that defaults to
``127.0.0.1:8765``.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import io
import json
import logging
import os
import platform
import subprocess
from dataclasses import dataclass
from typing import Iterable, Sequence, Dict, Any

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ScreenshotResult:
    """Structured response returned by :func:`capture_screenshot`."""

    mime_type: str
    data: str


def _ensure_positive_int(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative (received {value})")


def _validate_button(button: str) -> str:
    allowed = {"left", "right", "middle"}
    normalized = button.lower()
    if normalized not in allowed:
        raise ValueError(f"button must be one of {sorted(allowed)} (received {button!r})")
    return normalized


async def _run_command(cmd: list[str]) -> dict[str, str]:
    """Run a shell command and return the result."""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": process.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }


def create_app(host: str = "127.0.0.1", port: int = 8765) -> FastAPI:
    """Create FastAPI app with proper HEAD method support for ChatGPT validation."""
    
    app = FastAPI(title="ChatGPT Mac Control MCP Server")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    active_connections: Dict[str, Any] = {}
    
    tools = [
        {
            "name": "get_system_info",
            "description": "Get basic system information",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "execute_command", 
            "description": "Execute a shell command",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"]
            }
        },
        {
            "name": "list_directory",
            "description": "List files in a directory", 
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path", "default": "."}
                },
                "required": []
            }
        },
        {
            "name": "read_file",
            "description": "Read contents of a text file",
            "inputSchema": {
                "type": "object", 
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"]
            }
        },
        {
            "name": "write_file",
            "description": "Write content to a text file",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        },
        {
            "name": "send_notification",
            "description": "Send desktop notification (macOS only)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Notification title"},
                    "message": {"type": "string", "description": "Notification message"}
                },
                "required": ["title", "message"]
            }
        }
    ]
    
    async def execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with given arguments."""
        try:
            if name == "get_system_info":
                return {
                    "platform": platform.system(),
                    "platform_version": platform.version(), 
                    "architecture": platform.architecture()[0],
                    "hostname": platform.node(),
                    "python_version": platform.python_version()
                }
            elif name == "execute_command":
                command = arguments.get("command", "")
                if not command.strip():
                    raise ValueError("Command cannot be empty")
                result = await _run_command(["sh", "-c", command])
                return result
            elif name == "list_directory":
                path = arguments.get("path", ".")
                try:
                    items = []
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        is_dir = os.path.isdir(item_path)
                        items.append({
                            "name": item,
                            "type": "directory" if is_dir else "file", 
                            "path": item_path
                        })
                    return {"items": items, "path": path}
                except Exception as e:
                    return {"error": str(e), "path": path, "items": []}
            elif name == "read_file":
                path = arguments.get("path", "")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return {"content": content, "path": path}
                except Exception as e:
                    return {"error": str(e), "path": path, "content": ""}
            elif name == "write_file":
                path = arguments.get("path", "")
                content = arguments.get("content", "")
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return {"success": True, "path": path, "message": "File written successfully"}
                except Exception as e:
                    return {"success": False, "path": path, "error": str(e)}
            elif name == "send_notification":
                title = arguments.get("title", "")
                message = arguments.get("message", "")
                if platform.system() != "Darwin":
                    return {"success": False, "error": "Notifications only supported on macOS"}
                try:
                    cmd = ["osascript", "-e", f'display notification "{message}" with title "{title}"']
                    result = await _run_command(cmd)
                    if result["returncode"] == 0:
                        return {"success": True, "title": title, "message": message}
                    else:
                        return {"success": False, "error": result["stderr"]}
                except Exception as e:
                    return {"success": False, "error": str(e)}
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            return {"error": str(e)}
    
    @app.get("/sse")
    async def sse_endpoint(request: Request):
        """SSE endpoint for ChatGPT MCP connection."""
        import uuid
        session_id = str(uuid.uuid4())
        
        async def event_stream():
            try:
                endpoint_data = f"/message?session_id={session_id}"
                event_data = f"event: endpoint\ndata: {endpoint_data}\n\n"
                LOGGER.debug(f"Sending SSE endpoint event: {repr(event_data)}")
                yield event_data
                
                import asyncio
                counter = 0
                while True:
                    try:
                        await asyncio.sleep(15)
                        if await request.is_disconnected():
                            LOGGER.debug("SSE client disconnected")
                            break
                        counter += 1
                        heartbeat_data = f"event: heartbeat\ndata: ping-{counter}\n\n"
                        LOGGER.debug(f"Sending SSE heartbeat: {repr(heartbeat_data)}")
                        yield heartbeat_data
                    except Exception as e:
                        LOGGER.error(f"SSE heartbeat error: {e}")
                        break
            except Exception as e:
                LOGGER.error(f"SSE event_stream error: {e}")
                yield f"event: error\ndata: {str(e)}\n\n"
        
        return StreamingResponse(
            event_stream(), 
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
    
    @app.head("/sse")
    async def sse_head():
        """HEAD method for SSE endpoint validation."""
        return JSONResponse({"status": "ok"})
    
    @app.options("/sse") 
    async def sse_options():
        """OPTIONS method for SSE endpoint."""
        return JSONResponse({"status": "ok"})
    
    @app.post("/message")
    async def message_endpoint(request: Request):
        """Handle JSON-RPC messages from ChatGPT."""
        try:
            body = await request.json()
            LOGGER.debug(f"Received JSON-RPC request: {body}")
            
            if not isinstance(body, dict) or "jsonrpc" not in body:
                raise HTTPException(status_code=400, detail="Invalid JSON-RPC request")
            
            method = body.get("method")
            params = body.get("params", {})
            request_id = body.get("id")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "ChatGPT Mac Control",
                            "version": "1.0.0"
                        }
                    }
                }
            elif method == "ping":
                response = {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {}
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": tools
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if not tool_name:
                    raise HTTPException(status_code=400, detail="Tool name required")
                
                result = await execute_tool(tool_name, arguments)
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            LOGGER.debug(f"Sending JSON-RPC response: {response}")
            return JSONResponse(response)
            
        except Exception as e:
            LOGGER.exception(f"Error handling message: {e}")
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": body.get("id") if isinstance(body, dict) else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }, status_code=500)
    
    @app.head("/message")
    async def message_head():
        """HEAD method for message endpoint validation."""
        return JSONResponse({"status": "ok"})
    
    @app.options("/message")
    async def message_options():
        """OPTIONS method for message endpoint."""
        return JSONResponse({"status": "ok"})
    
    @app.get("/")
    async def root_get():
        """Root GET endpoint for ChatGPT validation."""
        return JSONResponse({"status": "ok", "name": "ChatGPT Mac Control", "version": "1.0.0"})
    
    @app.head("/")
    async def root_head():
        """Root HEAD endpoint for ChatGPT validation."""
        return JSONResponse({"status": "ok"})
    
    @app.options("/")
    async def root_options():
        """Root OPTIONS endpoint for ChatGPT validation."""
        return JSONResponse({"status": "ok"})
    
    return app


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the ChatGPT MCP Mac control server.")
    parser.add_argument("--host", default="127.0.0.1", help="Interface to bind the HTTP server")
    parser.add_argument("--port", default=8765, type=int, help="Port to bind the HTTP server")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity for the Uvicorn server",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    app = create_app(args.host, args.port)
    LOGGER.info(
        "Starting ChatGPT MCP server on http://%s:%d (SSE: /sse, messages: /message)",
        args.host,
        args.port,
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level.lower())


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
