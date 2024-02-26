import matplotlib.pyplot as plt
from fisher_py import RawFile
import numpy as np
from fisher_py.data.business import TraceType
from scipy.interpolate import interp1d
from processData import find_peaks_and_valleys,clean_data,find_valley_before_peak_rt


raw_file = RawFile("./data/1115-200PPT-female-1-pos-2.RAW")

target_mass = 760.58
mass_tolerance_ppm = 5

rt, i = raw_file.get_chromatogram(target_mass, mass_tolerance_ppm, TraceType.MassRange)
print('rt:',rt)
plt.figure()
plt.plot(rt, i)

max_i = np.max(i)
normalized_i = np.copy(i) / max_i
plt.figure()
plt.plot(rt, normalized_i)

cleand_i = clean_data(i)
plt.figure()
plt.plot(rt, cleand_i)
print('max_cleand_i:',np.max(cleand_i))

max_i = np.max(cleand_i)
normalized_ri = np.copy(cleand_i) / max_i
plt.figure()
plt.plot(rt, normalized_ri)

print(len(rt) , rt)

print('max_rt clean:',max_i)




peak_indexes,valley_indexes = find_peaks_and_valleys(rt, normalized_ri, threshold=0.2, order=1)
print('Peaks:', peak_indexes)
print('Valleys:', valley_indexes)

valleyPeakRtTuple = find_valley_before_peak_rt(peak_indexes,valley_indexes,rt)
print('valleyPeakTuple:',valleyPeakRtTuple)

for i in range(0,len(valleyPeakRtTuple)):
    valleyPeakRtItem = valleyPeakRtTuple[i]
    print('valleyPeakRtItem:',valleyPeakRtItem)
    
    mz_peak, i2_peak, charges_peak, real_rt_peak = raw_file.get_scan_ms1(valleyPeakRtItem[1])
   
    mz_valley, i2_valley, charges_valley, real_rt_valley = raw_file.get_scan_ms1(valleyPeakRtItem[3])
    
    print('len mz_peak mz_valley',len(mz_peak),len(mz_valley))
    
    plt.figure()
    
    x1 = np.array([])
    y1 = np.array([])
    x2 = np.array([])
    y2 = np.array([])
    
    y_diff = np.array([])
    if len(mz_valley) < len(mz_peak):
        print('len mz_valley < len mz_peak')
        x1 = mz_peak
        y1 = i2_peak
        x2 = mz_valley # 点少，需要插值
        y2 = i2_valley # 点少，需要插值
        f = interp1d(x2, y2, kind='slinear')
        x1_clipped = np.clip(x1, np.min(x2), np.max(x2))
        y2_interp = f(x1_clipped)
        plt.plot(x1_clipped, y2_interp, label='y2_interp')
        y_diff =  y1 - y2_interp
    else:
        print('len mz_valley > len mz_peak')
        x1 = mz_valley
        y1 = i2_valley
        x2 = mz_peak # 点少，需要插值
        y2 = i2_peak # 点少，需要插值
        
        f = interp1d(x2, y2, kind='slinear')                                                                    
        x1_clipped = np.clip(x1, np.min(x2), np.max(x2))
        y2_interp = f(x1_clipped)
        plt.plot(x1_clipped, y2_interp, label='y2_interp')
        y_diff = y2_interp - y1

    
    plt.plot(x1, y1, label='y1')
    plt.plot(x2, y2, label='y2')
    
   

   
    #if flag == 1:
    #    y_diff =  y1 - y2_interp
    #elif flag == 2:
    #    y_diff = y2_interp - y1
    #y_diff =  y1 - y2_interp
    
    plt.plot(x1, y_diff, label='diff')
    plt.legend()
    




print("=======")


#for i in range(0, 1200):
#    mz, i2, charges, real_rt = raw_file.get_scan_ms1(i/100)
#    plt.figure()
#    plt.plot(mz, i2)
#    print('this is ',i,' :',mz, i2, charges, real_rt)

plt.show()