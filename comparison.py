import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import timeit

path = Path(r'C:\Users\User\PycharmProjects\Lab3 data\household_power_consumption.txt')


def read_file_p():
    df = pd.read_csv(path, sep=';')
    df.columns = ['Date', 'Time', 'Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity',
                  'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
    df = df.loc[(df['Global_active_power'] != '?') & (df['Global_reactive_power'] != '?') & (df['Voltage'] != '?') &
                (df['Global_intensity'] != '?') & (df['Sub_metering_1'] != '?') & (df['Sub_metering_2'] != '?') &
                (df['Sub_metering_3'] != '?')]
    cols = df.columns.drop(['Date', 'Time'])
    df[cols] = df[cols].apply(pd.to_numeric)
    return df


def read_file_n():
    df = pd.read_csv(path, sep=';')
    df.columns = ['Date', 'Time', 'Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity',
                  'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
    df = df.loc[(df['Global_active_power'] != '?') & (df['Global_reactive_power'] != '?') & (df['Voltage'] != '?') &
                (df['Global_intensity'] != '?') & (df['Sub_metering_1'] != '?') & (df['Sub_metering_2'] != '?') &
                (df['Sub_metering_3'] != '?')]
    cols = df.columns.drop(['Date', 'Time'])
    df[cols] = df[cols].apply(pd.to_numeric)
    v = df.to_numpy()
    np.set_printoptions(precision=3, edgeitems=5,
                        floatmode='fixed')  # 5 с начала и 5 с конца выводит (и столбиков и строчек)
    return v

df = read_file_p()
array = read_file_n()


def task1_p(dff):
    dfff = dff.loc[(dff['Global_active_power'] > 5)]
    return dfff


def task1_n(arr):
    arrr = arr[arr[:, 2] > 5]
    return arrr


def task_1():
    x = []
    pand = []
    nump = []
    for i in range(1, 7):
        i = 10 ** i
        x.append(i)
        pand.append(timeit.timeit(f'task1_p(df[:{i}])', number=10, globals=globals()))
        nump.append(timeit.timeit(f'task1_n(array[:{i}])', number=10, globals=globals()))
    plt.plot(x, pand, label='pandas')
    plt.plot(x, nump, label='numpy')
    plt.ylabel('time')
    plt.xlabel('size')
    plt.title('Task 1')
    plt.xscale("log")
    plt.legend()
    plt.show()


#task_1()


def task2_p(dff):
    dff = dff.loc[(dff['Voltage'] > 235)]
    return dff


def task2_n(arr):
    arr = arr[arr[:, 4] > 235]
    return arr


def task_2():
    x = []
    pand = []
    nump = []
    for i in range(1, 7):
        i = 10 ** i
        x.append(i)
        pand.append(timeit.timeit(f'task2_p(df[:{i}])', number=10, globals=globals()))
        nump.append(timeit.timeit(f'task2_n(array[:{i}])', number=10, globals=globals()))
    plt.plot(x, pand, label='pandas')
    plt.plot(x, nump, label='numpy')
    plt.ylabel('time')
    plt.xlabel('size')
    plt.title('Task 2')
    plt.legend()
    plt.xscale("log")
    plt.show()


#task_2()

def task3_p(dff):
    dff = dff.loc[(dff['Global_intensity'] > 19) & (dff['Global_intensity'] < 20) & (
                dff['Sub_metering_2'] > dff['Sub_metering_3'])]
    return dff


def task3_n(arr):
    arr = arr[(arr[:, 5] > 19) & (arr[:, 5] < 20) & (arr[:, 7] > arr[:, 8])]
    return arr


def task_3():
    x = []
    pand = []
    nump = []
    for i in range(1, 7):
        i = 10 ** i
        x.append(i)
        pand.append(timeit.timeit(f'task3_p(df[:{i}])', number=10, globals=globals()))
        nump.append(timeit.timeit(f'task3_n(array[:{i}])', number=10, globals=globals()))
    plt.plot(x, pand, label='pandas')
    plt.plot(x, nump, label='numpy')
    plt.ylabel('time')
    plt.xlabel('size')
    plt.title('Task 3')
    plt.legend()
    plt.xscale("log")
    plt.show()


#task_3()


df_t4 = df.sample(500000)



number_of_rows = array.shape[0]
random_indices = np.random.choice(number_of_rows, size=500000, replace=False)
array_t4 = array[random_indices]


def task4_p(dff):
    sm1_mean = dff['Sub_metering_1'].mean()
    sm2_mean = dff['Sub_metering_2'].mean()
    sm3_mean = dff['Sub_metering_3'].mean()
    return sm1_mean, sm2_mean, sm3_mean


def task4_n(arr):
    average = np.mean(arr[:, 6:9], axis=1)
    average = average.reshape(arr.shape[0], 1)
    arr = np.concatenate((arr, average), axis=1)  # counted average for task 4
    return arr

def task_4():
    x = []
    pand = []
    nump = []
    for i in range(1, 7):
        i = 10 ** i
        x.append(i)
        pand.append(timeit.timeit(f'task4_p(df_t4[:{i}])', number=10, globals=globals()))
        nump.append(timeit.timeit(f'task4_n(array_t4[:{i}])', number=10, globals=globals()))
    plt.plot(x, pand, label='pandas')
    plt.plot(x, nump, label='numpy')
    plt.ylabel('time')
    plt.xlabel('size')
    plt.title('Task 4')
    plt.legend()
    plt.xscale("log")
    plt.show()


task_4()



def task5_p(dff):
    dff = dff.loc[(dff['Time'] >= '18:00:00') & (dff['Global_active_power'] >= 6) & (
            dff['Sub_metering_2'] > dff['Sub_metering_3']) & (dff['Sub_metering_2'] > dff['Sub_metering_1'])]
    l = (len(dff))
    dff1 = dff.iloc[2: l // 2:3]  # every third
    dff2 = dff.iloc[l // 2 + 1::4]  # every fourth
    return dff1, dff2


def task5_n(arr):
    arr = arr[(arr[:, 1] >= '18:00:00') & (arr[:, 2] >= 6) & (arr[:, 7] > arr[:, 6]) &
              (arr[:, 7] > arr[:, 8])]
    l = len(arr)  # length
    arr1 = arr[2: l // 2:3]  # every third
    arr2 = arr[l // 2 + 1::4]  # every fourth
    return arr1, arr2


def task_5():
    x = []
    pand = []
    nump = []
    for i in range(1, 7):
        i = 10 ** i
        x.append(i)
        pand.append(timeit.timeit(f'task5_p(df[:{i}])', number=10, globals=globals()))
        nump.append(timeit.timeit(f'task5_n(array[:{i}])', number=10, globals=globals()))
    plt.plot(x, pand, label='pandas')
    plt.plot(x, nump, label='numpy')
    plt.ylabel('time')
    plt.xlabel('size')
    plt.title('Task 5')
    plt.legend()
    plt.xscale("log")
    plt.show()


#task_5()
