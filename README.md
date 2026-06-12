# ShellcodingDream - Advanced Shellcode Obfuscation Framework

Professional-grade shellcode obfuscation and evasion toolkit for penetration testing and red team operations.

## Features

- **7 Advanced Encoders**: XOR, ROT13, Base64, RC4, UUID, IP Address, MAC Address
- **Automated Testing**: Built-in payload validation
- **Multi-Platform**: Linux and Windows (x86/x64)
- **Docker Ready**: One command to run everything
- **OSCP Optimized**: Fast, reliable, exam-ready

## Quick Start

### Installation

```bash
# Clone or download this project
cd ShellcodingDream-Complete

# Build Docker image
docker-compose build

# Run
docker-compose run --rm shellcoding --help
```

### Basic Usage

```bash
# List encoders
docker-compose run --rm shellcoding list

# Encode payload
docker-compose run --rm shellcoding encode \
  --technique xor \
  --input payload.hex \
  --output encoded.c

# Compile
docker-compose run --rm shellcoding compile \
  --technique xor \
  --input encoded.c \
  --platform linux

# Full pipeline (encode → compile → test)
docker-compose run --rm shellcoding pipeline \
  --technique xor \
  --input payload.hex \
  --platform linux
```

## Encoders

| Encoder | Speed | Effectiveness | Use Case |
|---------|-------|----------------|----------|
| XOR | Fastest | Good | Default choice |
| ROT13 | Fast | Good | Simple obfuscation |
| Base64 | Medium | Medium | Hide in plain sight |
| RC4 | Medium | Very Good | Strong encryption |
| UUID | Medium | Good | Network config evasion |
| IP | Medium | Good | Network evasion |
| MAC | Medium | Good | Network evasion |

## OSCP Quick Reference

```bash
# Generate payload (Linux reverse shell)
# Use msfvenom or MSFconsole to generate shellcode first

# Try XOR (fastest, 30 seconds)
docker-compose run --rm shellcoding pipeline \
  --technique xor --input payload.hex --platform linux

# If blocked, try RC4 (30 seconds)
docker-compose run --rm shellcoding pipeline \
  --technique rc4 --input payload.hex --platform linux

# Still blocked? Try others...
docker-compose run --rm shellcoding pipeline \
  --technique base64 --input payload.hex --platform linux
```

## Documentation

- `docs/QUICK_START.md` - Fast reference guide
- `docs/OSCP_GUIDE.md` - OSCP exam tips
- `docs/ADVANCED.md` - Advanced techniques

## File Structure

```
ShellcodingDream-Complete/
├── Dockerfile                 # Docker build instructions
├── docker-compose.yml         # Docker compose config
├── requirements.txt           # Python dependencies
├── app/
│   ├── main.py               # CLI interface
│   ├── encoder.py            # Encoder interface
│   ├── compiler.py           # C compiler wrapper
│   └── validator.py          # Payload validator
├── encoders/                 # Encoding implementations
│   ├── xor.py
│   ├── rot13.py
│   ├── base64.py
│   ├── rc4.py
│   ├── uuid.py
│   ├── ip_address.py
│   └── mac_address.py
├── templates/                # C code templates
├── scripts/                  # Helper scripts
└── docs/                     # Documentation
```

## Commands

### Encoding

```bash
# XOR encoding
docker-compose run --rm shellcoding encode \
  --technique xor --input payload.hex --key 0xAA

# RC4 encoding
docker-compose run --rm shellcoding encode \
  --technique rc4 --input payload.hex
```

### Compilation

```bash
# Linux x64
docker-compose run --rm shellcoding compile \
  --technique xor --input encoded.c --platform linux --arch x64

# Windows x64
docker-compose run --rm shellcoding compile \
  --technique xor --input encoded.c --platform windows --arch x64
```

### Testing

```bash
# Test compiled payload
docker-compose run --rm shellcoding test --payload ./payload
```

### Full Pipeline

```bash
# All-in-one: encode → compile → test
docker-compose run --rm shellcoding pipeline \
  --technique xor --input payload.hex --platform linux --verbose
```

## Troubleshooting

### Docker not found
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Permission denied
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Build fails
```bash
# Force rebuild
docker-compose build --no-cache
```

## OSCP Exam Tips

1. **Pre-build before exam**
   ```bash
   docker-compose build
   docker pull shellcoding-dream:latest
   ```

2. **Test locally first**
   ```bash
   docker-compose run --rm shellcoding list
   docker-compose run --rm shellcoding pipeline \
     --technique xor --input test.hex --platform linux
   ```

3. **Know your commands**
   - Have quick reference written down
   - Practice under time pressure
   - Know which encoder to try first

4. **Decision tree during exam**
   - Try XOR first (fastest)
   - If blocked, try RC4
   - If still blocked, try others
   - Skip if taking >5 minutes per target

## License

Educational use only. Authorized testing only.

## Disclaimer

This tool is for authorized penetration testing only. Unauthorized access to systems is illegal. Always have written permission before testing.
