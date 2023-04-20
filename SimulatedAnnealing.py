import random
import math
import time
import csv
R = []
T = []
C = []
D = []
tmp_schedule = []
real_schedule = []
tmp = []
numbers=[]
def mappingTeacher():
    handle = open(linkgv+'.txt', 'r')
    teacher = []
    dictTeacher = []
    while True:
        line = handle.readline()
        if line == '':
            break
        teacher.append(line.strip())
    for i in teacher:
        a = i.split(',')
        a[0] = int(a[0])
        dictTeacher.append(tuple(a))
    dictTeacher = dict(dictTeacher)
    return dictTeacher
def outputCSV():
    title = ['Lop']
    tmp = []
    tmp1 = []
    tmp2 = [[]]
    dictTeacher=mappingTeacher()
    for i in real_schedule:
        tmp1 = []
        for j in i:
            tmp1.append(dictTeacher[j])
        tmp2.append(tmp1)
    tmp2.pop(0)
    list_tkb = tmp2
    for i in range(numbers[2]):
        title.append("Tiet " + str(i + 1))
    for i in range(numbers[1]):
        tmp.append(list_tkb[i])
    # use
    for i in tmp:
        for j in i:
            j = str(j)
            j = j.strip()

    temp = []
    index = 1
    with open('D:/tkb.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(title)
        for i in tmp:
            temp.append('Lop ' + str(index))
            for j in i:
                temp.append(str(j))
            writer.writerow(temp)
            temp = []
            index += 1
    with open('D:/tkb.csv') as f:
        print(f.read())
def toInt(param, tmp):
    for i in range(len(tmp)):
        tmp[i] = int(tmp[i])

    param.append(tmp)


def readFile():
    tmp = []
    signal = ''
    handle = open(linkdata+'.txt', 'r')
    toInt(numbers,handle.readline().split())
    for line in handle:
        if len(line) == 2:
            signal = line.split()[0]
            continue
        else:
            tmp = line.split()
            if signal == 'R':
                toInt(R, tmp)
            elif signal == 'T':
                toInt(T, tmp)
            elif signal == 'C':
                toInt(C, tmp)
            elif signal == 'D':
                toInt(D, tmp)


def check_table():
    class_max = []
    lesson_max = []

    for c in C:
        class_max.append(sum(c))
        lesson_max.append(0)

    for r in R:
        for i in range(len(r)):
            lesson_max[i] += r[i]

    for i in range(len(class_max)):
        if (class_max[i] - lesson_max[i] < 0):
            print(
                'Cannot study because lesson_max > class ability! Check table R (sum by each column) and table C (sum by each row)')
            return False

    for i in range(len(C)):
        for j in range(len(C[i])):
            if C[i][j] == 0 and D[i][j] == 1:
                print('Conflict at [', i, j, '] in table C and D')
                return False

    return True


def init_state():
    global tmp_schedule
    tmp_schedule = [list(x) for x in C]  # Create a copy of C
    t_number = 1

    # Clean Schedule
    for line in tmp_schedule:
        for e in range(len(line)):
            if (line[e] != 0):
                line[e] = 0

    # Create Init State Base On R Table
    for teacher in R:
        for i in range(len(teacher)):
            if teacher[i] == 0:
                continue
            else:
                for j in range(teacher[i]):
                    tmp_schedule[i][tmp_schedule[i].index(0)] = t_number
        t_number += 1

    # Shaking
    for i in range(len(tmp_schedule)):
        for t in range(69):
            l1 = random.randint(0, len(tmp_schedule[i]) - 1)
            l2 = l1

            while (l1 == l2):
                l2 = random.randint(0, len(tmp_schedule[i]) - 1)

            handle = tmp_schedule[i][l1]
            tmp_schedule[i][l1] = tmp_schedule[i][l2]
            tmp_schedule[i][l2] = handle


def is_valid():
    for i in range(len(real_schedule)):
        for j in range(len(real_schedule[i])):
            for k in range(len(real_schedule)):
                if k != i and real_schedule[i][j] != 0:
                    if (real_schedule[i][j] == real_schedule[j][k]):
                        return False

    return True


def cost(schedule):
    cost = 0
    t_number = 1

    for teacher in T:
        for t in range(len(teacher)):
            if (teacher[t] == 1):
                continue
            else:
                for i in range(len(schedule)):
                    for j in range(len(schedule[i])):
                        if schedule[i][j] == t_number and j == t:
                            cost += 1

        t_number += 1

    for i in range(len(schedule)):
        for j in range(len(schedule[i])):
            if schedule[i][j] != 0 and C[i][j] == 0:
                cost += 1
            if schedule[i][j] == 0 and D[i][j] == 1:
                cost += 1

    return cost


def cost_one_line(line):
    cost = 0
    t_number = 1

    for teacher in T:
        for t in range(len(teacher)):
            if (teacher[t] == 1):
                continue
            else:
                for i in range(len(line)):
                    if line[i] == t_number and i == t:
                        cost += 1

        t_number += 1

    for l in range(len(line)):
        if line[l] != 0 and C[0][l] == 0:
            cost += 1
        if line[l] == 0 and D[0][l] == 1:
            cost += 1

    return cost


def detailCost(schedule):
    cost = 0
    t_number = 1

    print("Teacher:")

    for teacher in T:
        for t in range(len(teacher)):
            if (teacher[t] == 1):
                continue
            else:
                for i in range(len(schedule)):
                    for j in range(len(schedule[i])):
                        if schedule[i][j] == t_number and j == t:
                            print(i, j, schedule[i][j])
                            cost += 1

        t_number += 1

    print("Class:")

    for i in range(len(tmp_schedule)):
        for j in range(len(tmp_schedule[i])):
            if tmp_schedule[i][j] != 0 and C[i][j] == 0:
                print('C', i, j, tmp_schedule[i][j])
                cost += 1
            if tmp_schedule[i][j] == 0 and D[i][j] == 1:
                print('D', i, j, tmp_schedule[i][j])
                cost += 1


def randomState():
    schedule = [list(x) for x in tmp_schedule]

    c = random.randint(0, len(schedule) - 1)

    l1 = random.randint(0, len(schedule[0]) - 1)
    l2 = l1

    while (l1 == l2):
        l2 = random.randint(0, len(schedule[0]) - 1)

    tmp = schedule[c][l1]
    schedule[c][l1] = schedule[c][l2]
    schedule[c][l2] = tmp

    return schedule


def randomState_one_line():
    line = []

    for x in tmp:
        line.append(x)

    l1 = random.randint(0, len(line) - 1)
    l2 = l1

    while (l1 == l2):
        l2 = random.randint(0, len(line) - 1)

    handle = line[l1]
    line[l1] = line[l2]
    line[l2] = handle

    return line


def annealing():
    global tmp_schedule

    temparature = 10000
    cooling_sense = 3.5
    prob = 0
    times = 1

    newState = []

    c0 = cost(tmp_schedule)
    c1 = 0

    while (True):
        newState = randomState()
        c1 = cost(newState)

        prob = pow(math.e, (c1 - c0) / temparature)
        choose = random.random() - prob

        temparature -= cooling_sense
        print('t: ', temparature, 'oldVal: ', c0, 'newVal: ', c1, 'prob: ', prob, 'choose: ', choose)

        if (c1 == 0):
            tmp_schedule = newState
            print(times)
            return tmp_schedule
        elif (c1 < c0):
            tmp_schedule = newState
            c0 = c1
        elif choose > 0:
            tmp_schedule = newState
            c0 = c1

        if (temparature < 1):
            if c0 != 0:
                temparature = 10000
                times += 1

                if times == 10:
                    print(T)
                    return tmp_schedule


def annealing_one_line():
    global tmp
    
    temparature = 100
    cooling_sense = 0.99
    prob = 0
    times = 1
    
    newState = []
    
    c0 = cost_one_line(tmp)
    c1 = 0

    while(True):
        newState = randomState_one_line()
        c1 = cost_one_line(newState)
    
        temparature -= cooling_sense

        prob = pow(math.e, -(c1-c0)/temparature)

        choose = prob - random.random() - 0.15*(times-1)

        print('t: ', temparature, 'oldVal: ', c0, 'newVal: ', c1, 'prob: ', prob, 'choose: ', choose)

        if (c1 == 0):
            tmp = newState
            print(times)
            return tmp
        elif (c1 < c0):
            tmp = newState
            c0 = c1
        elif (choose > 0):
            tmp = newState
            c0 = c1

        if (temparature <= 0.002):
            if c0 != 0:
                temparature = 1
                cooling_sense = 0.001
                times += 1

                if times == 5:
                    return tmp


def do_it():
    global T
    global real_schedule
    global tmp

    while (True):
        tmp = tmp_schedule.pop(0)

        annealing_one_line()

        #print(tmp)
        time.sleep(1)

        real_schedule.append(tmp)

        C.pop(0)
        D.pop(0)

        for i in range(len(tmp)):
            if (tmp[i] != 0 and T[tmp[i] - 1][i] != 0):
                T[tmp[i] - 1][i] = 0

        if (len(tmp_schedule) == 0):
            break

linkgv='giaovien'
linkdata='data'
print('Hay chon du lieu demo....')
print('Co 2 du lieu demo co san, hay nhap 1 hoac 2:',end='')
choose=input()
while choose != '1' and choose != '2':
    print('Lua chon khong hop le, vui long nhap lai:',end='')
    choose=input()
linkgv=linkgv+str(choose)
linkdata=linkdata+str(choose)
print('Dang chay..........')
readFile()
if check_table() == True:

    init_state()
    do_it()
    numbers=numbers[0]
    outputCSV()
    print('Done!!!!!!')
    print('Du lieu duoc ghi tai D:/tkb.csv !')
else:
    print('Check all of the table again!')


