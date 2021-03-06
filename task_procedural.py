import csv

filepath = 'data.raw'

columns = [
    'data_center', 'host_name', 'disk_serial',
    # 'disk_age_in_s',
    'disk_age',
    'total_reads',
    'total_writes',
    # 'average_IO_latency_from_5_minutes_in_ms',
    'av_IO_in_ms',
    # 'total_uncorrected_read_errors',
    'tot_read_errs',
    # 'total_uncorrected_write_errors',
    'tot_write_errs',
]


def csv_to_dicts_list(file, names):
    with open(file, 'r') as csvfile:
        file_data = csv.reader(csvfile, delimiter=';')
        return [dict(zip(names, row)) for row in file_data]


def convert_to_int(dict_list, keys):
    for d in dict_list:
        for k in keys:
            d[k] = int(d[k])


def lists_grouped_per_dc(dict_list):
    grouped_dict = {}
    for d in dict_list:
        grouped_dict.setdefault(d['data_center'], []).append(d)
    return grouped_dict


def count_disks_info(data_list):
    disks_total = len(data_list)
    set_of_DC = set([x['data_center'] for x in data_list])
    count_DC_dict = {x['data_center']: 0 for x in data_list}

    for s in set_of_DC:
        for d in data_list:
            if s == d['data_center']:
                count_DC_dict[s] += 1

    sum_all = sum(item for item in count_DC_dict.values())

    return {
        'disks_total': disks_total,
        'set_of_DC': set_of_DC,
        'count_DC_dict': count_DC_dict,
        'sum_all': sum_all,
    }


def youngest_oldest_disk(data_list):
    youngest = None
    oldest = None
    for x in data_list:
        if not youngest or x['disk_age'] < youngest['disk_age']:
            youngest = x
        if not oldest or x['disk_age'] > oldest['disk_age']:
            oldest = x
    return {'youngest': youngest, 'oldest': oldest}


def avg_disk_age_in_days(data_list):
    sum_age = 0
    for x in data_list:
        sum_age += x['disk_age']
    return avg_age_in_days(sum_age, len(data_list))
    # return round(sum_age / len(data_list) / (3600 * 24), 2)


def avg_age_in_days(sum_age_in_sec, hdd_qty):
    return round(sum_age_in_sec / hdd_qty / (3600 * 24), 2)


# smd = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7}


def avg_disk_age_in_days_per_dc(grouped_data):
    sum_age_total = 0
    hdd_qty_total = 0
    ret = {'total_avg_age': 0}

    for dc in grouped_data:
        sum_age_per_dc = 0
        for hdd in grouped_data[dc]:
            sum_age_total += int(hdd['disk_age'])
            sum_age_per_dc += int(hdd['disk_age'])

        hdd_qty_dc = len(grouped_data[dc])
        hdd_qty_total += hdd_qty_dc
        ret[f'{dc}_avg_age_days'] = avg_age_in_days(sum_age_per_dc, hdd_qty_dc)

    ret['total_avg_age'] = avg_age_in_days(sum_age_total, hdd_qty_total)
    return ret


def calc_avg_iops(data_list):
    """
    Nie jestem do konca pewny czy o takie obliczenia chodzi??o.
    Nie do konca rozumiem pytanie.

    http://b1s.eu/pl/storage-array/1156-how-to-convert-mbps-to-iops-or-calculate-iops-from-mb-s.html
    """
    sum_io = 0
    for x in data_list:
        sum_io += x['total_reads'] / x['total_writes']
    return sum_io / len(data_list)


def find_top_5_disks(data_list):
    sorted_list = sorted(data_list, key=lambda k: (k['av_IO_in_ms']))
    return sorted_list[:5] + sorted_list[-5:]


def find_broken_disks(data_list):
    return [x for x in data_list if x['tot_read_errs'] > 0 or x['tot_write_errs'] > 0]


def answer_1(cnt_disks):
    print(1, '. How many disks are in total and in each DC?')
    for x in cnt_disks['count_DC_dict']:
        print('%10s %10s' % (x, cnt_disks["count_DC_dict"][x]))
    print('-' * 22)
    print('%10s %10s' % ('Total:', cnt_disks['disks_total']))
    print('\n')


def answer_2(yo):
    print(2, '. Which disk is the youngest/oldest one and what is its age (in days)')
    print('youngest_serial:', yo['youngest']['disk_serial'], '\tdays',
          round(yo['youngest']['disk_age'] / (3600 * 24), 2))
    print('oldest_serial:\t', yo['oldest']['disk_serial'], '\tdays', round(yo['oldest']['disk_age'] / (3600 * 24), 2),
          '\n')

    print('youngest:\t', yo['youngest'], '\n')
    print('oldest:\t', yo['oldest'], '\n')

    print('\n')


def answer_3(data):
    print(3, 'What\'s the average disk age per DC (in days)')
    print(f'answer_3: {data}', )
    print('\n')


def answer_4(ret):
    print(4, 'How many read/write IO/s disks processes on average')
    print('answer_4:', 'average IO/s ~ {} '.format(round(ret, 3)), '\n')


def answer_5(list):
    print(5, 'Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)')
    print('answer_5:')
    for x in list:
        print(x, '\n', '-' * 30)
    print('\n')


def answer_6(list):
    print(6,
          'Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter)')
    print('answer_6:', 'Found {} probably broken disks'.format(len(list)))
    for x in list:
        print(x, '\n', '-' * 30)
    print('\n')


list_of_dicts = csv_to_dicts_list(filepath, columns)
convert_to_int(list_of_dicts,
               ['disk_age', 'total_reads', 'total_writes', 'av_IO_in_ms', 'tot_read_errs', 'tot_write_errs'])
print(0, 'Imported {} records.{}'.format(len(list_of_dicts), '\n'))
lists_grouped = lists_grouped_per_dc(list_of_dicts)

answer_1(count_disks_info(list_of_dicts))
answer_2(youngest_oldest_disk(list_of_dicts))
answer_3(avg_disk_age_in_days(list_of_dicts))
answer_3(avg_disk_age_in_days_per_dc(lists_grouped))
# answer_4(calc_avg_iops(list_of_dicts))
# answer_5(find_top_5_disks(list_of_dicts))
# answer_6(find_broken_disks(list_of_dicts))

# print(1 / (0.003 + 0.0045))
