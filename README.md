# OneTrust Api - A2A | AG-UI | MCP

![PyPI - Version](https://img.shields.io/pypi/v/onetrust-api)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/onetrust-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/onetrust-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/onetrust-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/onetrust-api)
![PyPI - License](https://img.shields.io/pypi/l/onetrust-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/onetrust-api)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/onetrust-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/onetrust-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/onetrust-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/onetrust-api)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/onetrust-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/onetrust-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/onetrust-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/onetrust-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/onetrust-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/onetrust-api)

*Version: 0.1.0*

## Overview

**OneTrust Api MCP Server + A2A Agent**

Python OneTrust API client + MCP server + A2A agent with 100% API coverage

This repository is actively maintained - Contributions are welcome!

## MCP

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access).

#### Environment Variables

*   `ONETRUST_URL`: The URL of the target service.
*   `ONETRUST_TOKEN`: The API token or access token.

#### Run in stdio mode (default):
```bash
export ONETRUST_URL="http://localhost:8080"
export ONETRUST_TOKEN="your_token"
onetrust-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export ONETRUST_URL="http://localhost:8080"
export ONETRUST_TOKEN="your_token"
onetrust-mcp --transport "http" --host "0.0.0.0" --port "8000"
```

## A2A Agent

### Run A2A Server
```bash
export ONETRUST_URL="http://localhost:8080"
export ONETRUST_TOKEN="your_token"
onetrust-agent --provider openai --model-id gpt-4o --api-key sk-...
```

## Docker

### Build

```bash
docker build -t onetrust-api .
```

### Run MCP Server

```bash
docker run -d \
  --name onetrust-api \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e ONETRUST_URL="http://your-service:8080" \
  -e ONETRUST_TOKEN="your_token" \
  knucklessg1/onetrust-api:latest
```

### Deploy with Docker Compose

```yaml
services:
  onetrust-api:
    image: knucklessg1/onetrust-api:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - ONETRUST_URL=http://your-service:8080
      - ONETRUST_TOKEN=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "onetrust": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "onetrust-api",
        "onetrust-mcp"
      ],
      "env": {
        "ONETRUST_URL": "http://your-service:8080",
        "ONETRUST_TOKEN": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install onetrust-api
```
```bash
uv pip install onetrust-api
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)
