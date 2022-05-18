import csv

filepath = 'data.raw'


class Disk:
    list_of_disks = []
    dict_grouped_disks = {}

    def __init__(self, *args):
        self.__data_center = args[0]
        self.__host_name = args[1]
        self.__disk_serial = args[2]
        self.__disk_age = int(args[3])
        self.__total_reads = int(args[4])
        self.__total_writes = int(args[5])
        self.__av_io_in_ms = int(args[6])
        self.__tot_read_errs = int(args[7])
        self.__tot_write_errs = int(args[8])

        Disk.list_of_disks.append(self)
        Disk.dict_grouped_disks.setdefault(self.__data_center, []).append(self)

    @property
    def data_center(self):
        return self.__data_center

    @property
    def host_name(self):
        return self.__host_name

    @property
    def disk_serial(self):
        return self.__disk_serial

    @property
    def disk_age(self):
        return self.__disk_age

    @property
    def total_reads(self):
        return self.__total_reads

    @property
    def total_writes(self):
        return self.__total_writes

    @property
    def av_io_in_ms(self):
        return self.__av_io_in_ms

    @property
    def tot_read_errs(self):
        return self.__tot_read_errs

    @property
    def tot_write_errs(self):
        return self.__tot_write_errs

    @classmethod
    def import_csv_to_list_of_obj(cls, csv_file):
        with open(csv_file, 'r') as csvfile:
            file_data = csv.reader(csvfile, delimiter=';')
            return [cls(*row) for row in file_data]

    @classmethod
    def total_qty_of_disks(cls):
        return len(cls.list_of_disks)

    @classmethod
    def qty_disks_info(cls):
        # ('\n', 1, '. How many disks are in total and in each DC?')
        ret = {'disks_total': 0}
        for key in cls.dict_grouped_disks.keys():
            ret[key] = len(cls.dict_grouped_disks[key])
            ret['disks_total'] += ret[key]
        return ret

    @classmethod
    def youngest_oldest_disk(cls):
        # ('\n', 2, '. Which disk is the youngest/oldest one and what is its age (in days)?')
        youngest = None
        oldest = None
        for x in cls.list_of_disks:
            if not youngest or x.__disk_age < youngest.__disk_age:
                youngest = x
            if not oldest or x.__disk_age > oldest.__disk_age:
                oldest = x

        youngest.age_in_days = round(youngest.disk_age / (3600 * 24), 1)
        oldest.age_in_days = round(oldest.disk_age / (3600 * 24), 1)

        ret = {
            'youngest_disk_serial': youngest.__disk_serial,
            'youngest_age_in_days': youngest.age_in_days,
            'oldest_disk_serial': oldest.__disk_serial,
            'oldest_age_in_days': oldest.age_in_days,
            'youngest': youngest,
            'oldest': oldest,
        }
        return ret

    @classmethod
    def avg_disk_age_in_days_per_dc(cls):
        # (3, 'What\'s the average disk age per DC (in days)')
        data = cls.dict_grouped_disks
        ret = {}
        for k in data.keys():
            sum_seconds = 0
            for obj in data[k]:
                sum_seconds += obj.disk_age
            ret[f'{k}__avg_age_in_days'] = round(sum_seconds / len(data[k]) / (3600 * 24), 1)

        return ret

    @classmethod
    def avg_iops(cls):
        # (4, 'How many read/write IO/s disks processes on average')
        # data = cls.dict_grouped_disks
        ret = {}
        ret = 'NOT READY. I need a formula to calculate a value.'
        # for k in data.keys():
        #     sum_seconds = 0
        #     for obj in data[k]:
        #         sum_seconds += obj.disk_age
        #     ret[f'{k}__avg_age_in_days'] = round(sum_seconds / len(data[k]) / (3600 * 24), 1)
        return ret

    @classmethod
    def find_top_5_disks(cls):
        # (5, 'Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)')
        sorted_list = sorted(cls.list_of_disks, key=lambda k: k.av_io_in_ms)
        return {'lowest': sorted_list[:5], 'highest': sorted_list[-5:]}

    @classmethod
    def find_broken_disks(cls):
        # (6, 'Find disks which are most probably broken, i.e. have non-zero uncorrected errors '
        #          '(print disks and error counter)')
        return [x for x in cls.list_of_disks if x.tot_read_errs > 0 or x.tot_write_errs > 0]

    @staticmethod
    def print_total_qty_of_disks(info_int):
        print('\nTotal quantity of disks is: {}'.format(info_int))
        print('-' * 40, '\n')

    @staticmethod
    def print_answer_1(info_dict):
        print('\n', 1, '. How many disks are in total and in each DC?')
        print('\n [answer 1] - {}'.format(info_dict))
        print('-' * 40, '\n')

    @staticmethod
    def print_answer_2(info_dict):
        print('\n', 2, '. Which disk is the youngest/oldest one and what is its age (in days)?')
        print('\n [answer 2] - {}\n\nyoungest - {}\n\noldest - {}'
              .format(info_dict, vars(info_dict['youngest']), vars(info_dict['oldest'])))
        print('-' * 40, '\n')

    @staticmethod
    def print_answer_3(info_dict):
        print(3, 'What\'s the average disk age per DC (in days)')
        print('\n [answer 3] - {}'.format(info_dict))
        print('-' * 40, '\n')

    @staticmethod
    def print_answer_4(info_dict):
        print(4, 'How many read/write IO/s disks processes on average')
        print('\n [answer 4] - {}'.format(info_dict))
        print('-' * 40, '\n')

    @staticmethod
    def print_answer_5(info_list):
        print(5, 'Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)')
        print('\n [answer 5] - {}\n'.format(info_list))
        for x in info_list['lowest'] + info_list['highest']:
            print('top_low_hi-', vars(x), '\n')
        print('-' * 40, '\n')

    @staticmethod
    def print_answer_6(info_list):
        print(6, 'Find disks which are most probably broken, i.e. have non-zero uncorrected errors '
                 '(print disks and error counter)')
        print('\n [answer 6] - ', 'Found {} probably broken disks\n'.format(len(info_list)))
        for x in info_list:
            print(vars(x), '\n', '-' * 20)
        print('\n')


Disk.import_csv_to_list_of_obj(filepath)
Disk.print_total_qty_of_disks(Disk.total_qty_of_disks())

Disk.print_answer_1(Disk.qty_disks_info())
Disk.print_answer_2(Disk.youngest_oldest_disk())
Disk.print_answer_3(Disk.avg_disk_age_in_days_per_dc())
Disk.print_answer_4(Disk.avg_iops())
Disk.print_answer_5(Disk.find_top_5_disks())
Disk.print_answer_6(Disk.find_broken_disks())
