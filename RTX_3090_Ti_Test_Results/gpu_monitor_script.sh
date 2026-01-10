#!/bin/bash
# GPU Stress Test Monitor Script
# Monitors the RTX 3090 Ti during burn-in test

LOG_FILE=~/gpu_test_monitor_$(date +%Y%m%d_%H%M%S).log

echo "=== RTX 3090 Ti Stress Test Monitor ===" | tee $LOG_FILE
echo "Started monitoring at: $(date)" | tee -a $LOG_FILE
echo "Expected completion: ~$(date -d '+27 minutes')" | tee -a $LOG_FILE

# Monitor for 30 minutes (every 2 minutes = 15 checks)
for i in {1..15}; do
    echo -e "\n=== Check $i/15 at $(date) ===" | tee -a $LOG_FILE
    
    # Get burn test progress
    PROGRESS=$(tail -1 ~/gpu_burn_full_test.log 2>/dev/null | grep -o '[0-9]*\.*[0-9]*%' | head -1)
    ERRORS=$(tail -1 ~/gpu_burn_full_test.log 2>/dev/null | grep -o 'errors: [0-9]*' | cut -d' ' -f2)
    GFLOPS=$(tail -1 ~/gpu_burn_full_test.log 2>/dev/null | grep -o '[0-9]* Gflop/s' | cut -d' ' -f1)
    
    echo "Progress: $PROGRESS | Errors: $ERRORS | Performance: $GFLOPS Gflop/s" | tee -a $LOG_FILE
    
    # Get GPU metrics
    nvidia-smi --query-gpu=timestamp,temperature.gpu,power.draw,utilization.gpu,clocks.gr,fan.speed --format=csv,noheader | tee -a $LOG_FILE
    
    # Check for thermal throttling
    TEMP=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits)
    if [ "$TEMP" -gt 90 ]; then
        echo "⚠️  WARNING: High temperature detected: ${TEMP}°C" | tee -a $LOG_FILE
    elif [ "$TEMP" -gt 85 ]; then
        echo "ℹ️  Temperature elevated but safe: ${TEMP}°C" | tee -a $LOG_FILE
    else
        echo "✅ Temperature normal: ${TEMP}°C" | tee -a $LOG_FILE
    fi
    
    # Sleep for 2 minutes between checks
    sleep 120
done

echo -e "\n=== Final Status Check ===" | tee -a $LOG_FILE
tail -5 ~/gpu_burn_full_test.log | tee -a $LOG_FILE
echo "Monitor completed at: $(date)" | tee -a $LOG_FILE