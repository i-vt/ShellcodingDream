# Bloat

## How to use
1. Create bloated code
```
python3 bloat_c.py -f 100000 -v 100000 -s 10000 ;
```

2. Insert interesting code somewhere in the middle of the bloated code. **do not use notepad** - it will lag out like crazy, but vi works amazing.


3. Compile it
```
gcc -fno-stack-protector -z execstack -O0 -fno-inline -fno-unroll-loops -fno-optimize-sibling-calls -fno-omit-frame-pointer -fno-tree-ccp -fno-strength-reduce -g -o rand random_code.c 
```


### Stats
- Lines printed: `280496`
- Lines of code: `900008`
- Entropy: `4.996713673731774`
- Filesize: `41M`


## Samples
(Basic Linux TCP shell tested on 2024/09/17)

### Before bloat:
**Virus total detections: 20/66 = 30.30**
- ALYac - Trojan.Linux.Getshell.P
- Arcabit - Trojan.Linux.Getshell.P
- Avast - ELF:Shellshock-C [Expl]
- AVG - ELF:Shellshock-C [Expl]
- Avira (no cloud) - LINUX/Small.194.S
- BitDefender - Trojan.Linux.Getshell.P
- ClamAV - Unix.Backdoor.Msfvenom-10006778-1
- CTX - Elf.trojan.getshell
- Cynet - Malicious (score: 99)
- Elastic - Linux.Trojan.Metasploit
- Emsisoft - Trojan.Linux.Getshell.P (B)
- eScan - Trojan.Linux.Getshell.P
- GData - Trojan.Linux.Getshell.P
- Google - Detected
- Microsoft - Backdoor:Linux/GetShell.A!xp
- Sophos - Mal/Behav-175
- Tencent - Trojan.Linux.MSF.yo
- Trellix (HX) - Trojan.Linux.Getshell.P
- VIPRE - Trojan.Linux.Getshell.P
- WithSecure - Malware.LINUX/Small.194.S

### After bloat:
**Virus total detections: 7/66 = 10.61**
- Avira (no cloud) - LINUX/Small.194.S
- ClamAV - Unix.Backdoor.Msfvenom-10006778-1
- Cynet - Malicious (score: 99)
- Elastic - Linux.Trojan.Metasploit
- Google - Detected
- Microsoft - Backdoor:Linux/GetShell.A!xp
- WithSecure - Malware.LINUX/Small.194.S

### Bloat Detection Difference:
- ALYac - Trojan.Linux.Getshell.P
- Arcabit - Trojan.Linux.Getshell.P
- Avast - ELF:Shellshock-C [Expl]
- AVG - ELF:Shellshock-C [Expl]
- BitDefender - Trojan.Linux.Getshell.P
- CTX - Elf.trojan.getshell
- Emsisoft - Trojan.Linux.Getshell.P (B)
- eScan - Trojan.Linux.Getshell.P
- GData - Trojan.Linux.Getshell.P
- Sophos - Mal/Behav-175
- Tencent - Trojan.Linux.MSF.yo
- Trellix (HX) - Trojan.Linux.Getshell.P
- VIPRE - Trojan.Linux.Getshell.P


