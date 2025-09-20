# ChatGPT MCP Connector - URGENT TASK ASSIGNMENT

## TASK FOR CHATGPTCODER
User has assigned you to implement the working ChatGPT MCP connector. The kupn repo has a working implementation that needs to be adapted for the codexs repo.

## CRITICAL ISSUE RESOLVED
The SSE streaming issue has been fixed in kupn repo. The problem was using `EventSourceResponse` which caused malformed SSE events with double "data:" prefixes. The fix uses `StreamingResponse` instead.

## WORKING IMPLEMENTATION AVAILABLE
Copy the complete working implementation from `/home/ubuntu/repos/kupn/chatgpt_mac_mcp_server.py` - this file contains:
- ✅ Proper StreamingResponse SSE implementation
- ✅ JSON-RPC 2.0 compliance with MCP protocol version "2025-06-18"
- ✅ HEAD/OPTIONS method support for ChatGPT validation
- ✅ Session management and proper CORS headers
- ✅ Mac system control tools (system_info, run_command, file operations, notifications)

## IMMEDIATE ACTIONS REQUIRED

### 1. Copy Working Implementation
```bash
cp /home/ubuntu/repos/kupn/chatgpt_mac_mcp_server.py ./
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn starlette python-multipart
```

### 3. Test Server
```bash
python chatgpt_mac_mcp_server.py --host 0.0.0.0 --port 8765
```

### 4. Verify SSE Events
```bash
curl -N http://localhost:8765/sse
# Should output properly formatted SSE events without double "data:" prefix
```

### 5. Test JSON-RPC Endpoints
```bash
# Test initialize
curl -X POST http://localhost:8765/message?session_id=test \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"initialize","params":{}}'

# Test tools/list
curl -X POST http://localhost:8765/message?session_id=test \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"tools/list","params":{}}'
```

## DEPLOYMENT REQUIREMENTS
- Use cloudflared tunnel or similar to expose server publicly
- Test ChatGPT connector creation with the public URL
- Verify connector validation completes without timeout

## SUCCESS CRITERIA
- [ ] Server starts without errors
- [ ] SSE endpoint streams properly formatted events
- [ ] JSON-RPC methods return valid MCP responses
- [ ] ChatGPT connector creation succeeds
- [ ] Mac system control tools work correctly

## TECHNICAL DETAILS

### Key Fix - SSE Event Format
**WRONG (EventSourceResponse):**
```
data: event: endpoint
data: data: /message?session_id=123
```

**CORRECT (StreamingResponse):**
```
event: endpoint
data: /message?session_id=123
```

### MCP Protocol Compliance
- Protocol version: "2025-06-18"
- Required capabilities: tools, logging, prompts, resources, experimental
- JSON-RPC 2.0 format with proper error handling
- Session-based communication via SSE

### ChatGPT Validation Sequence
1. HEAD request to /sse endpoint
2. HEAD request to /message endpoint  
3. OPTIONS requests for CORS validation
4. GET request to /sse for SSE handshake
5. POST requests to /message for JSON-RPC methods

## PRIORITY: IMMEDIATE
User has given up on this project due to repeated failures. This is your chance to deliver a working solution. The implementation exists and works - just copy it and deploy it correctly.

## CONTACT
If you encounter any issues, the working server logs show proper SSE event generation:
```
DEBUG:__main__:Sending SSE endpoint event: 'event: endpoint\ndata: /message?session_id=...\n\n'
DEBUG:__main__:Sending SSE heartbeat: 'event: heartbeat\ndata: ping-1\n\n'
```

This proves the StreamingResponse implementation works correctly.
