"""Payload validation"""

import subprocess
import os

class PayloadValidator:
    """Validate payload execution"""
    
    def test(self, binary_path, verbose=False):
        """Test if payload executes"""
        
        if not os.path.exists(binary_path):
            return {'success': False, 'error': f'Binary not found: {binary_path}'}
        
        try:
            # Run with timeout
            result = subprocess.run(
                [binary_path],
                capture_output=True,
                timeout=5,
                text=True
            )
            
            return {
                'success': True,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            # Timeout is actually success (payload running)
            return {'success': True, 'message': 'Payload executed (timeout)'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
