from .models import Schema, List

from celery import shared_task

import csv


@shared_task
def create_csv(numbers_of_lines, user):
    print('create_csv is begining')
    obj_list = Schema.objects.filter(author=user)
    for schema in obj_list:
        schema.status = 'processing'
        schema.save()

        file_fields = List.objects.filter(schema_id=schema.id).order_by('order')
        files_directory = 'files/'
        file_name = schema.title + str(schema.id) + '.csv'
        full_name = files_directory + file_name
        with open(file_name, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            list1 = []
            list2 = []
            list3 = []
            for i in file_fields:
                list1.append(i.column_name)
                list2.append(i.column_type)
                list3.append(i.parameters)

            file_writer.writerow(list1)
            file_writer.writerow(list2)
            file_writer.writerow(list3)
            for i in range(int(numbers_of_lines)-3):
                file_writer.writerow('')

        print('file ' + full_name + ' is done') 

        schema.link = full_name
        schema.status = 'ready_to_download'
        schema.save()

