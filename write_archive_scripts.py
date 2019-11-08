import sys

nc = int(sys.argv[1])


with open('archive_template.sh', 'r') as fp:
    jobtemp = fp.readlines()

    jobtemp = "".join(jobtemp)

for i in range(nc):

    temp = jobtemp.format(cnum=i, lcnum='{lcnum}')

    with open('jobs/job.tar{}.sh'.format(i), 'w') as fp:

        fp.write(temp)
