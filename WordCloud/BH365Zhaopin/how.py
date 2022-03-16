import csv

job_list = []

with open('2022-03-15-job_title.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    for item in reader:
        for i in item:
            job_list.append(i)

with open('2022-03-15-365job.csv', 'w', encoding='utf-8') as f:
    for item in job_list:
        f.write(str(item) + '\n')

    f.close()





