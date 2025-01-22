import os
import csv
from datetime import datetime


def find_csv_file():
    _files = os.listdir('.')
    _csv_files = [file for file in _files if file.lower().endswith('.csv')]
    return _csv_files[0] if _csv_files else None


def import_csv_file(csv_file, keys_to_use=None):
    if keys_to_use is None:
        keys_to_use = []
    data = []
    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            _reader = csv.DictReader(f)
            for row in _reader:
                data.append({key: row[key] for key in keys_to_use if key in row})
    except FileNotFoundError:
        print(f"Die Datei {csv_file} wurde nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Lesen der Datei {csv_file}: {e}")
    return data


def compress_data_to_one_day(data=None, keys_to_use=None):
    if keys_to_use is None:
        keys_to_use = []
    if data is None:
        data = []

    _data_compressed = []
    for row in data:
        time = datetime.fromtimestamp(int(row[keys_to_use[0]])).strftime("%H:%M")
        power = (float(row[keys_to_use[1]])
                 + float(row[keys_to_use[2]])
                 + float(row[keys_to_use[3]]))
        power = round(power, 3)
        _data_compressed.append({
            'time': time,
            'power': power
        })
    return _data_compressed


def combine_data(data, keys_to_use=None):
    if keys_to_use is None:
        keys_to_use = []
    if data is None:
        data = []

    time_data = {}
    for row in data:
        time = row[keys_to_use[0]]
        if time not in time_data:
            time_data[time] = []

        time_data[time].append(row[keys_to_use[1]])

    return time_data


def combine_to_hours(time_data):
    combined_data = {}
    for time in time_data:
        hour = time.split(':')[0]
        power = time_data[time]

        if hour not in combined_data:
            combined_data[hour] = 0

        combined_data[hour] = round(combined_data[hour] + power, 3)

    return combined_data


def calculate_stats(data=None):
    if data is None or not isinstance(data, dict):
        data = {}

    min_values = {}
    max_values = {}
    average_values = {}
    for key in data:
        if isinstance(data[key], list):
            min_values[key] = min(data[key])
            max_values[key] = max(data[key])
            average_values[key] = round(sum(data[key]) / len(data[key]), 3)

    return min_values, max_values, average_values


def write_stats(min_data=None, max_data=None, average_data=None):
    if min_data is None:
        min_data = {}
    if max_data is None:
        max_data = {}
    if average_data is None:
        average_data = {}

    min_file_name = 'output/min.csv'
    max_file_name = 'output/max.csv'
    average_file_name = 'output/average.csv'

    file_min = open(min_file_name, 'w', encoding='utf-8')
    file_max = open(max_file_name, 'w', encoding='utf-8')
    file_average = open(average_file_name, 'w', encoding='utf-8')

    writer_min = csv.writer(file_min)
    writer_min.writerow(['time', 'power'])
    writer_max = csv.writer(file_max)
    writer_max.writerow(['time', 'power'])
    writer_average = csv.writer(file_average)
    writer_average.writerow(['time', 'power'])

    for hour in range(24):
        time = f"{hour:02}"

        if time in min_data:
            writer_min.writerow([time, str(min_data[time]).replace('.', ',')])
        if time in max_data:
            writer_max.writerow([time, str(max_data[time]).replace('.', ',')])
        if time in average_data:
            writer_average.writerow([time, str(average_data[time]).replace('.', ',')])

    return min_file_name, max_file_name, average_file_name


# ---- MAIN ----
if __name__ == '__main__':
    # get csv file
    _csv_file = find_csv_file()
    _keys_to_use = [
        'timestamp',
        'a_total_act_energy',
        'b_total_act_energy',
        'c_total_act_energy'
    ]

    if _csv_file:
        # get data from csv file for total energy
        _data = import_csv_file(_csv_file, keys_to_use=_keys_to_use)

        # compress data
        _data = compress_data_to_one_day(_data, keys_to_use=_keys_to_use)

        # combine data
        _data = combine_data(_data, keys_to_use=['time', 'power'])

        # calculate stats
        _min, _max, _avg = calculate_stats(_data)

        # combine stats to hourly data
        hour_data_min = combine_to_hours(_min)
        hour_data_max = combine_to_hours(_max)
        hour_data_average = combine_to_hours(_avg)

        # write data to csv files
        _min_filename, _max_filename, _avg_filename = write_stats(min_data=hour_data_min,
                                                                  max_data=hour_data_max,
                                                                  average_data=hour_data_average)

        print(f"written data to {_min_filename}, {_max_filename}, {_avg_filename}")
