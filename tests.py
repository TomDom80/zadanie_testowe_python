# from my_task import avg_disk_age_in_days, find_broken_disks
from task_procedural import *

'''
        python -m pytest tests.py -v
'''
dni_1 = {'disk_age': (24 * 3600)}
dni_2 = {'disk_age': (2 * 24 * 3600)}
dni_5 = {'disk_age': (5 * 24 * 3600)}
dni_10 = {'disk_age': (10 * 24 * 3600)}
dni_15 = {'disk_age': (15 * 24 * 3600)}
dni_20 = {'disk_age': (20 * 24 * 3600)}
dni_40 = {'disk_age': (40 * 24 * 3600)}


def test_youngest_oldest_disk():
    l1 = [dni_40, dni_2, dni_5, dni_20]
    l2 = [dni_1, dni_2, dni_10, dni_2]
    l3 = [dni_40, dni_2, dni_20, dni_5]
    l4 = [dni_1, dni_5, dni_5, dni_2]
    l5 = [dni_20, dni_10, dni_40, dni_1]
    l6 = [dni_40, dni_2, dni_20, dni_10]

    assert youngest_oldest_disk(l1) == {'youngest': dni_2, 'oldest': dni_40}
    assert youngest_oldest_disk(l2) == {'youngest': dni_1, 'oldest': dni_10}
    assert youngest_oldest_disk(l3) == {'youngest': dni_2, 'oldest': dni_40}
    assert youngest_oldest_disk(l4) == {'youngest': dni_1, 'oldest': dni_5}
    assert youngest_oldest_disk(l5) == {'youngest': dni_1, 'oldest': dni_40}
    assert youngest_oldest_disk(l6) == {'youngest': dni_2, 'oldest': dni_40}


def test_avg_disk_age_in_days():
    list_1_5 = [dni_1, dni_2]
    list_10 = [dni_15, dni_10, dni_5]
    list_5 = [dni_5, dni_5]

    assert avg_disk_age_in_days(list_1_5) == 1.5
    assert avg_disk_age_in_days(list_10) == 10
    assert avg_disk_age_in_days(list_5) == 5


def test_find_broken_disks():
    e_0 = {'tot_read_errs': 0, 'tot_write_errs': 0}
    e_1 = {'tot_read_errs': 0, 'tot_write_errs': 1}
    e_2 = {'tot_read_errs': 1, 'tot_write_errs': 1}
    e_2a = {'tot_read_errs': 0, 'tot_write_errs': 2}
    e_3 = {'tot_read_errs': 2, 'tot_write_errs': 1}

    le_0 = [e_0, e_0]
    le_1 = [e_0, e_1, e_0]
    le_2 = [e_0, e_1]
    le_3 = [e_0, e_1, e_0, e_0, e_2, e_2]

    assert find_broken_disks(le_0) == []
    assert find_broken_disks(le_1) == [e_1]
    assert find_broken_disks(le_2) == [e_1]
    assert find_broken_disks(le_3) == [e_1, e_2, e_2]
    assert find_broken_disks(le_3) != [e_2, e_2, e_1]


def test_calc_avg_io_ps():
    io_0 = {'total_reads': 9, 'total_writes': 3}
    io_1 = {'total_reads': 25000, 'total_writes': 5000}
    io_2 = {'total_reads': 80, 'total_writes': 20}

    lio_0 = [io_0]
    lio_1 = [io_1]
    lio_2 = [io_0, io_1]
    lio_3 = [io_0, io_1, io_2]

    assert calc_avg_iops(lio_0) == 3
    assert calc_avg_iops(lio_0) == 3
    assert calc_avg_iops(lio_1) == 5
    assert calc_avg_iops(lio_2) == 4
    assert calc_avg_iops(lio_3) == 4

