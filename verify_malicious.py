#!/usr/bin/env python3
"""
Quick verification script to check if malware performs malicious actions.
Usage: python verify_malicious.py [malware.exe]
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def quick_test(exe_path: Path):
    """Quick test of a single malware executable."""
    print(f"[*] Testing: {exe_path.name}")
    
    # Create test environment
    test_dir = Path(tempfile.mkdtemp(prefix="malware_test_"))
    docs_dir = test_dir / "Documents"
    docs_dir.mkdir()
    
    # Create test file
    test_file = docs_dir / "test.txt"
    test_file.write_text("This is a test file that should be encrypted.\n" * 5)
    
    # Copy malware
    test_exe = test_dir / exe_path.name
    shutil.copy2(exe_path, test_exe)
    test_exe.chmod(0o755)
    
    try:
        # Run with wine
        env = os.environ.copy()
        env['USERPROFILE'] = str(test_dir)
        
        result = subprocess.run(
            ['wine64', str(test_exe)],
            cwd=str(test_dir),
            env=env,
            capture_output=True,
            timeout=10
        )
        
        import time
        time.sleep(1)
        
        # Check results
        encrypted_files = list(docs_dir.glob("*.encrypted"))
        ransom_note = docs_dir / "README_ENCRYPTED.txt"
        
        print(f"  Exit code: {result.returncode}")
        print(f"  Files encrypted: {len(encrypted_files)}")
        print(f"  Ransom note created: {ransom_note.exists()}")
        
        if encrypted_files:
            print(f"  Encrypted files: {[f.name for f in encrypted_files]}")
        
        if ransom_note.exists():
            print(f"  Ransom note size: {ransom_note.stat().st_size} bytes")
            print(f"  Preview: {ransom_note.read_text()[:80]}...")
        
        # Verify malicious behavior
        is_malicious = len(encrypted_files) > 0 or ransom_note.exists()
        
        if is_malicious:
            print(f"  [✓] MALICIOUS BEHAVIOR CONFIRMED")
            return True
        else:
            print(f"  [!] No malicious behavior detected")
            return False
            
    except Exception as e:
        print(f"  [!] Error: {e}")
        return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == '__main__':
    import os
    
    if len(sys.argv) > 1:
        exe_path = Path(sys.argv[1])
        if not exe_path.exists():
            print(f"[!] File not found: {exe_path}")
            sys.exit(1)
        quick_test(exe_path)
    else:
        # Test all executables
        malware_dir = Path("generated_malware")
        exe_files = sorted(malware_dir.glob("*.exe"))
        
        if not exe_files:
            print("[!] No .exe files found in generated_malware/")
            sys.exit(1)
        
        print(f"[*] Testing {len(exe_files)} malware variants\n")
        malicious_count = 0
        
        for exe_file in exe_files:
            if quick_test(exe_file):
                malicious_count += 1
            print()
        
        print(f"[*] Summary: {malicious_count}/{len(exe_files)} variants demonstrated malicious behavior")
        
        if malicious_count == len(exe_files):
            print("[✓] All variants are clearly malicious (Task point 5: PASSED)")
        else:
            print("[!] Some variants did not demonstrate malicious behavior")

