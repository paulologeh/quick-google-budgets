#!/bin/bash

interpreter=`which python3`

echo "Welcome to Quick Google Budgets!"
echo "Have you converted your bank statements to csv ?"
read response1

if [ "$response1" != 'YES' ]; then
    echo "Please convert your bank statements to CSV."
    exit 0
fi

echo "Have you filled out the config.json ?"
read response2

if [ "$response2" != 'YES' ]; then
    echo "Please fill out the config.json file."
    exit 0
fi

echo "Have you filled out the rules.json ?"
read response3

if [ "$response3" != 'YES' ]; then
    echo "Please fill out the rules.json file."
    exit 0
fi

$interpreter app.py