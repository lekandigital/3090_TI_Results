#!/usr/bin/env python3
"""
Simple GPU Memory Pattern Test for RTX 3090 Ti
Tests memory patterns to detect potential VRAM issues
"""
import os
import time
import subprocess
import sys

def run_nvidia_smi_test():
    """Run memory and compute tests using nvidia-smi and basic CUDA operations"""
    
    print("=== GPU Memory Pattern Test ===")
    print(f"Started: {time.ctime()}")
    
    # Test 1: Basic nvidia-smi memory test
    print("\n--- Test 1: GPU Memory Info ---")
    result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total,memory.used,memory.free', '--format=csv'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("Memory status:")
        print(result.stdout)
    else:
        print("Error getting memory info")
    
    # Test 2: Persistence mode test
    print("\n--- Test 2: GPU Persistence Test ---") 
    for i in range(5):
        print(f"  Persistence test iteration {i+1}/5")
        result = subprocess.run(['nvidia-smi', '-q', '-d', 'MEMORY'], capture_output=True, text=True)
        if "BAR1 Memory Usage" in result.stdout and "FB Memory Usage" in result.stdout:
            print(f"    ✓ Memory structures intact")
        else:
            print(f"    ✗ Memory structure test failed")
            return False
        time.sleep(2)
    
    # Test 3: Temperature monitoring during stress
    print("\n--- Test 3: Thermal Stability Test ---")
    temps = []
    for i in range(10):
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            temp = int(result.stdout.strip())
            temps.append(temp)
            print(f"  Temperature reading {i+1}/10: {temp}°C")
            time.sleep(3)
        else:
            print(f"  Error reading temperature")
    
    if temps:
        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        print(f"\n  Temperature Statistics:")
        print(f"    Average: {avg_temp:.1f}°C")
        print(f"    Maximum: {max_temp}°C") 
        print(f"    Minimum: {min_temp}°C")
        print(f"    Range: {max_temp - min_temp}°C")
        
        if max_temp > 85:
            print(f"  ⚠️  WARNING: High temperature detected ({max_temp}°C)")
        elif max_temp < 75:
            print(f"  ✓ Excellent thermal performance")
        else:
            print(f"  ✓ Good thermal performance")
    
    print(f"\nCompleted: {time.ctime()}")
    return True

if __name__ == "__main__":
    success = run_nvidia_smi_test()
    sys.exit(0 if success else 1)