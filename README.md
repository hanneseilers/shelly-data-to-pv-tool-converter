# Shelly Data to PV Tool Converter

A Python tool for converting Shelly energy monitoring data into formats suitable for PV (photovoltaic) analysis tools.

## Overview

This project provides two main scripts for processing energy consumption data:

1. **main.py** - Processes Shelly 3EM CSV export data and generates statistical analysis
2. **calculate-daily-consumption.py** - Creates reference consumption profiles for a full year

## Scripts

### main.py

Processes CSV data from Shelly 3EM devices and generates hourly consumption statistics.

**Features:**
- Automatically finds CSV files in the current directory
- Combines data from three-phase energy measurements (a, b, c)
- Compresses data to one-day format
- Calculates min, max, and median values for each hour
- Outputs statistical data to CSV files

**Expected Input:**
- CSV file with columns: `timestamp`, `a_total_act_energy`, `b_total_act_energy`, `c_total_act_energy`

**Output:**
- `output/min.csv` - Minimum power consumption per hour
- `output/max.csv` - Maximum power consumption per hour  
- `output/median.csv` - Median power consumption per hour

**Usage:**
```bash
python main.py
```
(Place your Shelly CSV export in the same directory)

### calculate-daily-consumption.py

Generates a full year consumption profile based on daily and monthly reference patterns.

**Features:**
- Creates hourly consumption data for an entire year
- Uses percentage-based distribution from daily consumption patterns
- Applies monthly consumption variations
- Outputs timestamp-based CSV for PV tools

**Usage:**
```bash
python calculate-daily-consumption.py -dcf <daily_consumption_file.csv> -mcf <monthly_consumption_file.csv>
```

**Arguments:**
- `-dcf, --daily_consumption_file` - CSV with hourly consumption pattern
- `-mcf, --monthly_consumption_file` - CSV with monthly consumption distribution

**Output:**
- `output/reference.csv` - Full year consumption data with timestamps

## Requirements

- Python 3.x
- pandas

## Installation

```bash
pip install pandas
```

## Output Directory

The `output/` directory contains all generated CSV files. This directory should exist before running the scripts.

## License

No license specified.
