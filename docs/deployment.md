# Deployment

## Docker

```bash
docker build -t onetrust-api .
```

```bash
docker run -d --name onetrust-api -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e ONETRUST_URL="https://acme.my.onetrust.com" \
  -e ONETRUST_TOKEN="your_token" \
  example/onetrust-api@sha256:<digest>
```

## Docker Compose

```yaml
services:
  onetrust-api:
    image: example/onetrust-api@sha256:<digest>
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
      - ONETRUST_URL=https://acme.my.onetrust.com
      - ONETRUST_TOKEN=your_token
    ports:
      - 8000:8000
```

## Scoping the tool surface

Disable domains you don't need with `{TAG}TOOL=False` (e.g. `ESGTOOL=False`,
`TRAININGTOOL=False`). All domains default to `True`.
