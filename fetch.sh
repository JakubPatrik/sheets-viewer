#!/bin/bash
# ==================== SECRETS [edit]=============================
# This script exports the <doc_id> which is not exposed due to 
# privacy concerns
source sheets_id.sh
# ================================================================

# First argument expected to be the year
yr=$1
if [[ $# -ne 1 ]]; then
    echo -e -n "\033[38;5;9mInvalid or missing year: ($1)";
    echo -e " [2020/2021/2022/...]\033[0m"
    while [[ ! yr -gt 1900 ]] 
    do 
        echo -e -n "\033[38;5;6mEnter the year: \033[0m" 
        read -p "" yr
    done 
fi

g_id=${YEAR_MAP[$yr]}
url="https://docs.google.com/spreadsheets/d/$SHEETS_ID/export?format=csv&gid=$g_id&usp=sharing"

echo -e -n "\n--$(date +%F\ %T)[INFO]--: " >> debug.log
echo "(1/2) Downloading the invoices for year $yr" | tee -a debug.log

# Download the latest data from the Google Sheets
wget --no-check-certificate --output-document=csv/${yr}.csv $url -a debug.log

if [[ $? == 0 ]]; then
    echo -e -n "--$(date +%F\ %T)[INFO]--: " >> debug.log
    echo "(2/2) Downloaded the invoices for year $yr" | tee -a debug.log
    
    python3 build.py "csv/${yr}.csv"
else
    echo -e -n "--$(date +%F\ %T)[ERROR]--: " >> debug.log
    echo -e -n "\033[38;5;9m"
    echo "(2/2)Download FAILED for the year $yr" | tee -a debug.log
    echo -e "\033[0m"
fi
 