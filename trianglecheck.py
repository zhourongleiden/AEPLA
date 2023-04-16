def tc_algorithm (original_cvx, flag, timeseries_data):
    '''
    The triangle check function for DJ algorithm.
    Input:
        original_cvx: THe convex hall to be checked
        flag: Dealing with cvx_up or cvx_low
        timeseries_data: The original time series data
    Output:
    '''
    if len(original_cvx) < 3:
        checked_cvx = list(original_cvx)
    
    else:
        processing_cvx = list(original_cvx)
        last_1 = processing_cvx[len(processing_cvx)-1] 
        last_2 = processing_cvx[len(processing_cvx)-2]
        last_3 = processing_cvx[len(processing_cvx)-3]
       
        while len(processing_cvx) >= 3:           
           
            if flag == 1: #deal with cvx_up
                if timeseries_data[last_2] >= ((timeseries_data[last_1]-timeseries_data[last_3])/(last_1-last_3))*(last_2-last_3)+timeseries_data[last_3]:
                    processing_cvx.remove(last_2)
                    if len(processing_cvx) < 3: #only 2 records remain
                        checked_cvx = list(processing_cvx)
                        break
                    #initialize
                    last_1 = processing_cvx[len(processing_cvx)-1] 
                    last_2 = processing_cvx[len(processing_cvx)-2]
                    last_3 = processing_cvx[len(processing_cvx)-3]
                else:
                    checked_cvx = list(processing_cvx)
                    break
           
            if flag == 0: #deal with cvx_low
                if timeseries_data[last_2] <= ((timeseries_data[last_1]-timeseries_data[last_3])/(last_1-last_3))*(last_2-last_3)+timeseries_data[last_3]:
                    processing_cvx.remove(last_2)
                    if len(processing_cvx) < 3: #only 2 records remain
                        checked_cvx = list(processing_cvx)
                        break
                    #initialize
                    last_1 = processing_cvx[len(processing_cvx)-1] 
                    last_2 = processing_cvx[len(processing_cvx)-2]
                    last_3 = processing_cvx[len(processing_cvx)-3]
                else:
                    checked_cvx = list(processing_cvx)
                    break
    
    return checked_cvx
