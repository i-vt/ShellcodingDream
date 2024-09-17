# Bloat

## How to use
```
python3 bloat_c.py -f 100000 -v 100000 -s 10000 ;
gcc -O0 -fno-inline -fno-unroll-loops -fno-optimize-sibling-calls -fno-omit-frame-pointer -fno-tree-ccp -fno-strength-reduce -g -o rand random_code.c 
```
Lines printed: `280496`
Lines of code: `900008`
Entropy: `4.996713673731774`
Filesize: `41M`


## Samples
(tested on 2024/09/17)

### Before bloat:
Virus total detections: 28/73 = 38.36
ALYac - Generic.ShellCode.Marte.4.DDE1EBB9
Arcabit - Generic.ShellCode.Marte.4.DDE1EBB9
Avast - Win32:MsfShell-V [Hack]
AVG - Win32:MsfShell-V [Hack]
BitDefender - Generic.ShellCode.Marte.4.DDE1EBB9
Bkav Pro - W64.AIDetectMalware
CrowdStrike Falcon - Win/malicious_confidence_60% (D)
CTX - Exe.unknown.marte
DeepInstinct - MALICIOUS
Elastic - Windows.Trojan.Metasploit
Emsisoft - Generic.ShellCode.Marte.4.DDE1EBB9 (B)
eScan - Generic.ShellCode.Marte.4.DDE1EBB9
ESET-NOD32 - A Variant Of Win64/Rozena.M
GData - Generic.ShellCode.Marte.4.DDE1EBB9
Google - Detected
Huorong - Backdoor/W64.Meterpreter.f
Ikarus - Trojan.Win64.Meterpreter
Kaspersky - HEUR:Trojan.Win32.Generic
McAfee Scanner - Ti!C2867A617E71
Microsoft - Trojan:Win64/Meterpreter.B
SecureAge - Malicious
Skyhigh (SWG) - BehavesLike.Win64.Downloader.cm
Symantec - Meterpreter
Tencent - Trojan.Win64.Rozena.16001343
Trellix (HX) - Generic.ShellCode.Marte.4.DDE1EBB9
Varist - W64/Rozena.HV.gen!Eldorado
VIPRE - Generic.ShellCode.Marte.4.DDE1EBB9
ZoneAlarm by Check Point - HEUR:Trojan.Win32.Generic

### After bloat:
**Virus total detections: 7/66 = 10.61**
Avast - ELF:Shellshock-C [Expl]
AVG - ELF:Shellshock-C [Expl]
Avira (no cloud) - LINUX/Small.194.S
ClamAV - Unix.Backdoor.Msfvenom-10006778-1
Cynet - Malicious (score: 99)
Elastic -Linux.Trojan.Metasploit
Google -Detected 
Microsoft -Backdoor:Linux/GetShell.A!xp
Tencent - Trojan.Linux.MSF.yo
WithSecure - Malware.LINUX/Small.194.S
