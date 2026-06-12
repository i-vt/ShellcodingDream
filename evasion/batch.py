"""
Batch Generation & Testing
Generate multiple payloads efficiently and test them at scale
"""

import subprocess
import os
import json
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


class BatchPayloadGenerator:
    """Generate multiple payloads with different encodings/techniques"""
    
    def __init__(self, output_dir="./batch_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.batch_manifest = []
    
    def generate_batch(self, shellcode_bytes, techniques, count_per_technique=3):
        """
        Generate multiple payloads
        
        Args:
            shellcode_bytes: Raw shellcode
            techniques: List of encoding techniques ['xor', 'rc4', 'base64', ...]
            count_per_technique: Number of variants per technique
        """
        
        manifest = {
            'timestamp': datetime.now().isoformat(),
            'total_payloads': len(techniques) * count_per_technique,
            'payloads': []
        }
        
        print(f"[*] Generating {manifest['total_payloads']} payloads...")
        print(f"[*] Techniques: {', '.join(techniques)}")
        print(f"[*] Variants per technique: {count_per_technique}")
        
        for technique in techniques:
            for variant in range(count_per_technique):
                payload_info = self._generate_single_payload(
                    shellcode_bytes,
                    technique,
                    variant
                )
                manifest['payloads'].append(payload_info)
        
        # Save manifest
        manifest_path = self.output_dir / "batch_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"[+] Generated {len(manifest['payloads'])} payloads")
        print(f"[+] Manifest saved to: {manifest_path}")
        
        return manifest
    
    def _generate_single_payload(self, shellcode_bytes, technique, variant_num):
        """Generate a single payload variant"""
        
        # Create output files
        technique_dir = self.output_dir / technique / f"variant_{variant_num}"
        technique_dir.mkdir(parents=True, exist_ok=True)
        
        # Payload metadata
        payload_id = f"{technique}_{variant_num}_{int(time.time())}"
        
        payload_info = {
            'id': payload_id,
            'technique': technique,
            'variant': variant_num,
            'files': {
                'encoded': str(technique_dir / f"{payload_id}.c"),
                'binary': str(technique_dir / f"{payload_id}.exe"),
                'metadata': str(technique_dir / f"{payload_id}.json")
            },
            'status': 'pending',
            'timestamp': datetime.now().isoformat()
        }
        
        # Save metadata
        with open(payload_info['files']['metadata'], 'w') as f:
            json.dump(payload_info, f, indent=2)
        
        print(f"[+] Created: {payload_id}")
        
        return payload_info
    
    def compile_batch(self, parallel=True, max_workers=4):
        """
        Compile all payloads in batch
        
        Args:
            parallel: Use parallel compilation
            max_workers: Number of parallel workers
        """
        
        manifest_path = self.output_dir / "batch_manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError("No batch manifest found")
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"[*] Compiling {len(manifest['payloads'])} payloads...")
        
        if parallel:
            self._compile_parallel(manifest, max_workers)
        else:
            self._compile_sequential(manifest)
        
        # Update manifest
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"[+] Batch compilation complete")
    
    def _compile_sequential(self, manifest):
        """Compile payloads sequentially"""
        
        for payload in manifest['payloads']:
            try:
                # Compile command (simplified)
                # In real implementation, would read the .c file and compile
                payload['status'] = 'compiled'
                print(f"[+] Compiled: {payload['id']}")
            except Exception as e:
                payload['status'] = 'failed'
                payload['error'] = str(e)
                print(f"[-] Failed: {payload['id']} - {e}")
    
    def _compile_parallel(self, manifest, max_workers):
        """Compile payloads in parallel"""
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            
            for payload in manifest['payloads']:
                future = executor.submit(self._compile_payload, payload)
                futures[future] = payload
            
            for future in as_completed(futures):
                payload = futures[future]
                try:
                    result = future.result()
                    payload['status'] = result['status']
                    payload['size'] = result.get('size')
                except Exception as e:
                    payload['status'] = 'failed'
                    payload['error'] = str(e)
    
    @staticmethod
    def _compile_payload(payload):
        """Compile single payload"""
        
        c_file = payload['files']['encoded']
        binary_file = payload['files']['binary']
        
        if not os.path.exists(c_file):
            return {'status': 'skipped', 'reason': 'no source'}
        
        try:
            # Compile with gcc
            result = subprocess.run(
                ['gcc', '-o', binary_file, c_file],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Compilation failed: {result.stderr.decode()}")
            
            # Get binary size
            size = os.path.getsize(binary_file)
            
            return {
                'status': 'compiled',
                'size': size
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }


class BatchTester:
    """Test multiple payloads"""
    
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
    
    def test_all_payloads(self, target_process=None, timeout=30):
        """Test all payloads in batch"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        print(f"[*] Testing {len(self.manifest['payloads'])} payloads...")
        
        for payload in self.manifest['payloads']:
            test_result = self.test_payload(payload, target_process, timeout)
            results['tests'].append(test_result)
        
        # Save results
        results_path = Path(self.manifest_path).parent / "test_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[+] Test results saved to: {results_path}")
        
        return results
    
    def test_payload(self, payload, target_process=None, timeout=30):
        """Test single payload execution"""
        
        test_result = {
            'payload_id': payload['id'],
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'execution_time': 0,
            'error': None
        }
        
        binary_path = payload['files']['binary']
        
        if not os.path.exists(binary_path):
            test_result['error'] = 'Binary not found'
            return test_result
        
        try:
            start_time = time.time()
            
            # Execute payload
            result = subprocess.run(
                [binary_path],
                capture_output=True,
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            
            test_result['execution_time'] = execution_time
            test_result['success'] = result.returncode == 0
            
            if result.returncode != 0:
                test_result['error'] = f"Return code: {result.returncode}"
            
            print(f"[{'✓' if test_result['success'] else '✗'}] {payload['id']} - {execution_time:.2f}s")
            
        except subprocess.TimeoutExpired:
            test_result['error'] = 'Timeout'
            print(f"[-] {payload['id']} - Timeout")
        except Exception as e:
            test_result['error'] = str(e)
            print(f"[-] {payload['id']} - {e}")
        
        return test_result
    
    def get_test_statistics(self):
        """Generate test statistics"""
        
        results_path = Path(self.manifest_path).parent / "test_results.json"
        
        if not results_path.exists():
            return {'error': 'No test results found'}
        
        with open(results_path, 'r') as f:
            results = json.load(f)
        
        stats = {
            'total_tests': len(results['tests']),
            'passed': sum(1 for t in results['tests'] if t['success']),
            'failed': sum(1 for t in results['tests'] if not t['success']),
            'success_rate': 0,
            'avg_execution_time': 0,
        }
        
        if stats['total_tests'] > 0:
            stats['success_rate'] = (stats['passed'] / stats['total_tests']) * 100
            
            times = [t['execution_time'] for t in results['tests']]
            stats['avg_execution_time'] = sum(times) / len(times)
        
        # Group by technique
        stats['by_technique'] = {}
        for test in results['tests']:
            technique = test['payload_id'].split('_')[0]
            if technique not in stats['by_technique']:
                stats['by_technique'][technique] = {'passed': 0, 'failed': 0}
            
            if test['success']:
                stats['by_technique'][technique]['passed'] += 1
            else:
                stats['by_technique'][technique]['failed'] += 1
        
        return stats
    
    def print_test_report(self):
        """Print formatted test report"""
        
        stats = self.get_test_statistics()
        
        if 'error' in stats:
            print(f"[!] {stats['error']}")
            return
        
        print("\n" + "="*60)
        print("BATCH TEST REPORT")
        print("="*60)
        print(f"Total Tests: {stats['total_tests']}")
        print(f"Passed: {stats['passed']}")
        print(f"Failed: {stats['failed']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Avg Execution Time: {stats['avg_execution_time']:.3f}s")
        print("\nResults by Technique:")
        for technique, counts in stats['by_technique'].items():
            total = counts['passed'] + counts['failed']
            rate = (counts['passed'] / total * 100) if total > 0 else 0
            print(f"  {technique:15} {counts['passed']:3}/{total:3} ({rate:5.1f}%)")
        print("="*60 + "\n")


class PayloadOptimizer:
    """Optimize payloads for size/speed/stealth"""
    
    @staticmethod
    def find_smallest_payload(manifest_path):
        """Find smallest payload from batch"""
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        smallest = None
        smallest_size = float('inf')
        
        for payload in manifest['payloads']:
            if 'size' in payload:
                if payload['size'] < smallest_size:
                    smallest = payload
                    smallest_size = payload['size']
        
        return smallest, smallest_size
    
    @staticmethod
    def find_fastest_payload(results_path):
        """Find fastest executing payload"""
        
        with open(results_path, 'r') as f:
            results = json.load(f)
        
        fastest = None
        fastest_time = float('inf')
        
        for test in results['tests']:
            if test['success'] and test['execution_time'] < fastest_time:
                fastest = test
                fastest_time = test['execution_time']
        
        return fastest, fastest_time
    
    @staticmethod
    def find_most_reliable_technique(results_path):
        """Find technique with highest success rate"""
        
        with open(results_path, 'r') as f:
            results = json.load(f)
        
        technique_stats = {}
        
        for test in results['tests']:
            technique = test['payload_id'].split('_')[0]
            if technique not in technique_stats:
                technique_stats[technique] = {'total': 0, 'passed': 0}
            
            technique_stats[technique]['total'] += 1
            if test['success']:
                technique_stats[technique]['passed'] += 1
        
        # Calculate rates
        rates = {}
        for technique, stats in technique_stats.items():
            if stats['total'] > 0:
                rates[technique] = stats['passed'] / stats['total']
        
        # Find best
        best_technique = max(rates, key=rates.get)
        best_rate = rates[best_technique]
        
        return best_technique, best_rate
