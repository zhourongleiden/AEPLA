def FSW_algorithm(error_threshold,timeseries_data,max_min_in_timeseries_total):
    '''
    Input:
        error_threshold: The global error bound epsilon0
        timeseries_data: The time series data
        max_min_in_timeseries_total: The global range gr in AEPLA
    Output:
        segment: A list of segments
    '''

    et=error_threshold
    max_error_threshold = et*max_min_in_timeseries_total
    timeseries_up = timeseries_data + max_error_threshold
    timeseries_low = timeseries_data - max_error_threshold
    
    i = 0
    seg_no = 0
    csp_id = 0
    segment_point = [[0,0]]
    upl = float('inf')
    lowl = float('-inf')  
    
    while i < len(timeseries_data)-1:
        i = i + 1
        upl = min(upl,((timeseries_up[i]-timeseries_data[segment_point[seg_no][1]])/(i-segment_point[seg_no][1])))
        lowl = max(lowl,((timeseries_low[i]-timeseries_data[segment_point[seg_no][1]])/(i-segment_point[seg_no][1])))
        if upl < lowl:
            seg_no = seg_no + 1
            segment_point.append([seg_no,csp_id])
            i = csp_id
            upl = float('inf')
            lowl = float('-inf')
        elif lowl <= ((timeseries_data[i]-timeseries_data[segment_point[seg_no][1]])/(i-segment_point[seg_no][1])) <= upl:
            csp_id = i
            
    # deal with the last segment
    if segment_point[seg_no][1] < len(timeseries_data)-1:
        seg_no = seg_no + 1
        segment_point.append([seg_no, len(timeseries_data)-1])
        
    # create segment
    segment = []
    for i in range(1,seg_no+1):
        segment.append([segment_point[i-1][1], 
                        segment_point[i][1], 
                        segment_point[i-1][1], 
                        timeseries_data[segment_point[i-1][1]], 
                        ((timeseries_data[segment_point[i-1][1]]-timeseries_data[segment_point[i][1]])/(segment_point[i-1][1]-segment_point[i][1]))])

    return segment
