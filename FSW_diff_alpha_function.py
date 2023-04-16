def FSW_diff_alpha_algorithm(error_threshold,timeseries_data,alpha_in_buf,alg):   
    '''
    Input:
        error_threshold: The global error bound
        timeseries_data: The time series data
        alpha_in_buf: The scarling factor alpha
        alg: AEPLA or the original PLA methods
    Output:
        segment_total: A list of segments
    '''
    import math
    import numpy as np
    from FSW import FSW_algorithm
    
    max_min_in_timeseries_total = timeseries_data.max()-timeseries_data.min()
    
    et = error_threshold
    buf = int(len(timeseries_data)*alpha_in_buf*et) if alg == 'p' else len(timeseries_data)-1
    segment_total = []
    
    interval_start = 0
    end_flag = 0
    
    while interval_start < len(timeseries_data)-1:
        interval_end = interval_start + buf
        if interval_end >= len(timeseries_data)-1:
            interval_end = len(timeseries_data)-1  
            end_flag = 1
        
        interval = timeseries_data[interval_start:interval_end+1]
        
        # if plus or original
        if alg == 'p':
            max_min_in_interval = interval.max()-interval.min()
            et_interval = et*math.exp(0.5-max_min_in_interval/max_min_in_timeseries_total)#parameter2
        elif alg == 'o':
            et_interval = et        
        
        # do FSW
        segment_interval = FSW_algorithm(et_interval,interval,max_min_in_timeseries_total)
       
        # re-adjust the index
        segment_interval = np.array(segment_interval)
        segment_interval[:,0:3] = segment_interval[:,0:3] + interval_start #s_start, s_end, intersection_x0 + interval_start 
        segment_interval = segment_interval.tolist()
        
        # append segment_interval to segment_total
        if len(segment_interval) > 1: # for the intervals contain more than one segment
            if end_flag == 0: # not the last interval, record the segments except for the last one  
                segment_total = segment_total + segment_interval[0:(len(segment_interval)-1)]
            else: # deal with the last interval, record all segments
                segment_total = segment_total + segment_interval
        else: # for the intervals contain only one segment, record it
            segment_total = segment_total + segment_interval       
            
        interval_start = int(segment_total[-1][1]) #s_end of the last segment

    return segment_total