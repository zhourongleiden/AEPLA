def DJ_algorithm(error_threshold, timeseries_data, max_min_in_timeseries_total):
    '''
    Input:
        error_threshold: The global error bound epsilon0
        timeseries_data: The time series data
        max_min_in_timeseries_total: The global range gr in AEPLA
    Output:
        segment: A list of segments
    '''
    import numpy as np
    import intersect
    from trianglecheck import tc_algorithm

    et=error_threshold
    max_error_threshold = et*max_min_in_timeseries_total
    timeseries_up = timeseries_data + max_error_threshold
    timeseries_low = timeseries_data - max_error_threshold
    
    s_start = 0
    s_new = 1
    sa, sd = 0, 1
    sb, sc = 0, 1
    upl = (timeseries_low[sb]-timeseries_up[sd])/(sb-sd)
    lowl = (timeseries_up[sa]-timeseries_low[sc])/(sa-sc)
    cvx_up = [sa,sd]
    cvx_low = [sb,sc]
    
    seg_no = 0
    segment = [] 
    
    
    last_segment_contain_one_point = 0
    
    while s_new < len(timeseries_data)-1:
        s_new = s_new + 1
        if (timeseries_up[s_new] <= upl*(s_new-sb)+timeseries_low[sb]+2*max_error_threshold and timeseries_low[s_new] >= lowl*(s_new-sa)+timeseries_up[sa]-2*max_error_threshold):
            sd_changed = 0 
            cvx_flag = -1
            if timeseries_up[s_new] < upl*(s_new-sb)+timeseries_low[sb]:
                # updata upl, sb(optional), sd and cvx_up                
                upl_candidate = [] 
                for i in cvx_low:
                    upl_candidate.append([i,(timeseries_low[i]-timeseries_up[s_new])/(i-s_new)])
                sb = upl_candidate[np.argmin(upl_candidate,axis=0)[1]][0]
                sd = s_new
                sd_changed = 1
                cvx_low = [i for i in cvx_low if i >= sb] # sb has been updated, we only need to consider points after sb in cvx_low
                upl = (timeseries_low[sb]-timeseries_up[sd])/(sb-sd)
                cvx_up.append(sd)
                cvx_flag = 1
                cvx_up = tc_algorithm(cvx_up, cvx_flag, timeseries_up) # update cvx_up by triangle check    
            if timeseries_low[s_new] > lowl*(s_new-sa)+timeseries_up[sa]:
                # updata lowl, sa(optional), sc and cvx_up
                lowl_candidate = [] 
                if sd_changed == 0:
                    for i in cvx_up:
                        lowl_candidate.append([i,(timeseries_up[i]-timeseries_low[s_new])/(i-s_new)])
                else:
                    for i in cvx_up:
                        if i < sd: # if i=sd then pho=-inf                       
                            lowl_candidate.append([i,(timeseries_up[i]-timeseries_low[s_new])/(i-s_new)])
                sa = lowl_candidate[np.argmax(lowl_candidate,axis=0)[1]][0]
                sc = s_new
                cvx_up = [i for i in cvx_up if i >= sa] # sa has been updated, we only need to consider points after sb in cvx_up             
                lowl = (timeseries_up[sa]-timeseries_low[sc])/(sa-sc)
                cvx_low.append(sc)  
                cvx_flag = 0
                cvx_low = tc_algorithm(cvx_low, cvx_flag, timeseries_low) # update cvx_low by triangle check    
        else:
            x0,y0 = intersect.GetIntersectPointofLines(sa,timeseries_up[sa], sc,timeseries_low[sc], sb,timeseries_low[sb], sd, timeseries_up[sd])
            l = 0.5*(upl+lowl)
            seg_no = seg_no + 1
            segment.append([s_start, s_new-1, x0, y0, l])
            
            # initialize
            s_start = s_new
            if s_start < len(timeseries_data)-1:
                sa, sd = s_start, s_start+1
                sb, sc = s_start, s_start+1
                upl = (timeseries_low[sb]-timeseries_up[sd])/(sb-sd)
                lowl = (timeseries_up[sa]-timeseries_low[sc])/(sa-sc)
                s_new = s_start + 1
                cvx_up = [sa,sd]
                cvx_low = [sb,sc]

            else:
                last_segment_contain_one_point = 1
    
    # deal with the last segment
    if last_segment_contain_one_point == 0:
        x0,y0 = intersect.GetIntersectPointofLines(sa,timeseries_up[sa], sc,timeseries_low[sc], sb,timeseries_low[sb], sd, timeseries_up[sd])
        l = 0.5*(upl+lowl)
        seg_no = seg_no + 1
        segment.append([s_start, len(timeseries_data)-1, x0, y0, l])
    else:
        seg_no = seg_no + 1
        segment.append([len(timeseries_data)-1, len(timeseries_data)-1, len(timeseries_data)-1, timeseries_data[len(timeseries_data)-1], 0])
                 
    return segment
    
