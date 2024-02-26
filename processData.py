from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def clean_data(data):
    clean_data = clean_data_with_zero(data)
    return clean_data

def clean_data_with_zero(data):
    copyData = np.copy(data)
    copyData[copyData < 0] = 0
    return copyData


def clean_data_with_threee_sigma(data):
    copyData = np.copy(data)
    mean = np.mean(copyData)
    std = np.std(copyData)
    upper = mean + 3 * std
    lower = mean - 3 * std
    outliers = copyData[(copyData > upper) | (copyData < lower)]
    data_cleaned = np.copy(copyData)
    data_cleaned[(data_cleaned > upper) | (data_cleaned < lower)] = 0
    return data_cleaned

def find_peaks_and_valleys(data_x,data_y, threshold=0.2, order=4):
    # Find peaks
    # order:两侧使用多少点进行比较
    def greater(a, b):
        return np.logical_and(a > threshold,  a > b)
    #greater = np.greater
    peak_indexes = signal.argrelextrema(data_y, greater, order=order)
    peak_indexes = peak_indexes[0]

    # Find valleys
    # order:两侧使用多少点进行比较
    def less(a, b):
        return np.logical_and(a < threshold, np.logical_and(a > 0, a < b))
    #less = np.less
    valley_indexes = signal.argrelextrema(data_y, less, order=order)
    valley_indexes = valley_indexes[0]

    (fig, ax) = plt.subplots()

    # Plot all data
    ax.plot(data_x, data_y)

    # Plot peaks
    peak_x = peak_indexes
    peak_y = data_y[peak_indexes]
    ax.scatter(peak_x, peak_y, marker='o', color='red', label="Peaks_Pointers")

    # Plot valleys
    valley_x = valley_indexes
    valley_y = data_y[valley_indexes]
    ax.scatter(valley_x, valley_y, marker='o', color='green', label="Valleys_Pointers")
    ax.plot(peak_x, peak_y, marker='*', linestyle='dashed', color='orange', label="peaks_connetted_line")
    ax.plot(valley_x, valley_y, marker='*', linestyle='dashed', color='blue', label="valleys_connetted_line")


    # 添加标题
    plt.title('Find peaks and valleys using argrelextrema()')
    # 添加图例
    plt.legend(loc='best')

    # 保存图像
    # plt.savefig('peaks-valleys.png')
    # 显示图像
    #plt.show()

    #print('Peaks:', peak_indexes)
    #print('Valleys:', valley_indexes)
    return peak_indexes, valley_indexes


def find_valley_before_peak_rt(peaks, valleys,rt):
    valleyPeakTuple = []
    for peak in peaks:
        idx = np.searchsorted(valleys, peak)
        if idx == 0:
            closest_valley = valleys[idx]
        elif idx == len(valleys):
            closest_valley = valleys[-1]
        else:
            closest_valley = valleys[idx-1]
        #print(idx,valleys[idx],f"Peak {peak} is closest to valley {closest_valley}")
        valleyPeakTuple.append((peak,rt[peak],closest_valley, rt[closest_valley]))
    return valleyPeakTuple

