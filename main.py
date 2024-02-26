import matplotlib.pyplot as plt
from fisher_py import RawFile
import numpy as np
from fisher_py.data.business import TraceType
from scipy.interpolate import interp1d
from processData import find_peaks_and_valleys,clean_data,find_valley_before_peak_rt

# 读文件
raw_file = RawFile("./data/1115-200PPT-female-1-pos-2.RAW")

target_mass = 760.58
mass_tolerance_ppm = 5

# 读原始数据
rt, i = raw_file.get_chromatogram(target_mass, mass_tolerance_ppm, TraceType.MassRange)
print('rt:',rt)
plt.figure()
plt.plot(rt, i)

# 找到原始数据的最大值，把原始数据做归一化处理
max_i = np.max(i)
normalized_i = np.copy(i) / max_i
plt.figure()
plt.plot(rt, normalized_i)

# 对原始数据做清洗
cleand_i = clean_data(i)
plt.figure()
plt.plot(rt, cleand_i)
print('max_cleand_i:',np.max(cleand_i))

# 找到清洗后的数据的最大值，把清洗后的数据做归一化处理
max_i = np.max(cleand_i)
normalized_ri = np.copy(cleand_i) / max_i
plt.figure()
plt.plot(rt, normalized_ri)
print(len(rt) , rt)
print('max_rt clean:',max_i)

# 找到清洗后的归一化的数据的所有的峰值和谷值
peak_indexes,valley_indexes = find_peaks_and_valleys(rt, normalized_ri, threshold=0.2, order=1)
print('Peaks:', peak_indexes)
print('Valleys:', valley_indexes)

# 找到所有的峰值，和它对应的前置谷值
valleyPeakRtTuple = find_valley_before_peak_rt(peak_indexes,valley_indexes,rt)
print('valleyPeakTuple:',valleyPeakRtTuple)

# 遍历所有的峰值
for i in range(0,len(valleyPeakRtTuple)):
    valleyPeakRtItem = valleyPeakRtTuple[i]
    print('valleyPeakRtItem:',valleyPeakRtItem)
    
    # 获取当前峰值的质谱图数据
    mz_peak, i2_peak, charges_peak, real_rt_peak = raw_file.get_scan_ms1(valleyPeakRtItem[1])
    
    # 获取当前谷值的质谱图数据
    mz_valley, i2_valley, charges_valley, real_rt_valley = raw_file.get_scan_ms1(valleyPeakRtItem[3])
    
    print('len mz_peak mz_valley',len(mz_peak),len(mz_valley))
    plt.figure()
    
    # 因为峰值的质谱图和谷值的质谱图的点数不一样，所以需要做插值处理
    x1 = np.array([])
    y1 = np.array([])
    x2 = np.array([])
    y2 = np.array([])
    y_diff = np.array([])
    
    # 插值处理，点数少的做插值
    if len(mz_valley) < len(mz_peak):
        print('len mz_valley < len mz_peak')
        x1 = mz_peak
        y1 = i2_peak
        x2 = mz_valley # 点少，需要插值
        y2 = i2_valley # 点少，需要插值
        
        # 插值用的是slinear，一阶样条插值
        f = interp1d(x2, y2, kind='slinear')
        x1_clipped = np.clip(x1, np.min(x2), np.max(x2))
        y2_interp = f(x1_clipped)
        plt.plot(x1_clipped, y2_interp, label='y2_interp')
        
        # 计算两个折线图的差值
        y_diff =  y1 - y2_interp
    else:
        print('len mz_valley > len mz_peak')
        x1 = mz_valley
        y1 = i2_valley
        x2 = mz_peak # 点少，需要插值
        y2 = i2_peak # 点少，需要插值
        
        # 插值用的是slinear，一阶样条插值
        f = interp1d(x2, y2, kind='slinear')                                                                    
        x1_clipped = np.clip(x1, np.min(x2), np.max(x2))
        y2_interp = f(x1_clipped)
        plt.plot(x1_clipped, y2_interp, label='y2_interp')
        
        # 计算两个折线图的差值
        y_diff = y2_interp - y1

    
    plt.plot(x1, y1, label='y1')
    plt.plot(x2, y2, label='y2')    
    plt.plot(x1, y_diff, label='diff')
    plt.legend()
    




print("=======")

plt.show()