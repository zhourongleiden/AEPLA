import math
import numpy as np

def error_measure_function(segments, data_timeseries):
    '''
    Input:
        segments: A list of segments
        data_timeseries: The original time series
    Output:
        errot_total: The total representation error
    '''
    error_total = 0
    for i in range(0,len(segments)):
        point_start = segments[i][0]
        point_end = segments[i][1]
        intersect_point_x0 = segments[i][2]
        intersect_point_y0 = segments[i][3]
        slope = segments[i][4]        
        for j in range(int(point_start), int(point_end+1)):
            # RMSE & MSE
            error_point = ((slope*(j-intersect_point_x0)+intersect_point_y0)-data_timeseries[j])**2            
            error_total = error_total + error_point
    #RMSE
    error_total =  math.sqrt(error_total / len(data_timeseries))
    
    return error_total

def error_measure_function_SemiOpt(semi_points, data_timeseries):
    error_total = 0
    for i in range(0,len(semi_points)-1):
        x_start, y_start = semi_points[i]
        x_end, y_end = semi_points[i+1]
        time_stamp_interval = np.arange(int(np.ceil(x_start)), int(np.floor(x_end)+1))
        slope = (y_end-y_start)/(x_end-x_start)
        error_interval = np.sum(((slope*(time_stamp_interval-x_start)+y_start)
                                -data_timeseries[time_stamp_interval])**2)
        error_total += error_interval
    #RMSE
    error_total =  math.sqrt(error_total / len(data_timeseries))
    
    return error_total