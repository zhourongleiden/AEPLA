def SemiOpt_diff_alpha_algorithm(error_threshold,timeseries_data,alpha_in_buf,alg):   
    
    import numpy as np
    import math
    from SemiOptConnAlg_algorithm import SemiOptConnAlg_algorithm
    
    max_min_in_timeseries_total = timeseries_data.max()-timeseries_data.min()
    
    et = error_threshold
    buf = int(len(timeseries_data)*alpha_in_buf*et) if alg == 'p' else len(timeseries_data)-1
    if (buf == 0 or buf == 1):
        buf = 2 
    segment_total = []
    
    interval_start = 0
    
    
    while interval_start < len(timeseries_data)-1:
        interval_end = interval_start + buf
        if interval_end >= len(timeseries_data)-1:
            interval_end = len(timeseries_data)-1  
        
        interval = timeseries_data[interval_start:interval_end+1]
        
        # if plus or original
        if alg == 'p':
            max_min_in_interval = interval.max()-interval.min()
            et_interval = et*math.exp(0.5-max_min_in_interval/max_min_in_timeseries_total)#parameter2
        else:
            et_interval = et        
        
        # do FSW
        segment_interval = SemiOptConnAlg_algorithm(et_interval, interval, max_min_in_timeseries_total)
       
        # re-adjust the index
        segment_interval = np.array(segment_interval)
        segment_interval[:,0] = segment_interval[:,0] + interval_start
        segment_interval = segment_interval.tolist()
        
        # append to segment_total
        segment_total = segment_total + segment_interval       
        
        # update interval_start
        interval_start = int(segment_total[-1][0]+1) 

    return segment_total
    