import numpy as np
import intersect
from trianglecheck import tc_algorithm

def test_semi(timeseries_data, 
              max_error, previous_seg, 
              current_seg_info, 
              call_from_backward_DJ, 
              call_from_SemiOptConnAlg_function,
              within_flag):
    '''
 
    Parameters
    ----------
    timeseries_data : array. Complete time series.
    max_error : float
    previous_seg : array, e.g. [upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, extrm, trivial_label]
                           #     0    1    2   3      4       5    6   7   8   9    10         11  
    current_seg_info : array, same as the aboved.
    call_from_backward_DJ: bool.
    call_from_SemiOptConnAlg_function: bool.
    
    Returns
    -------
    semi_label

    '''
    
    timeseries_up = timeseries_data + max_error
    timeseries_low = timeseries_data - max_error 
    sa_pre, sd_pre = int(previous_seg[6]), int(previous_seg[8])
    sb_pre, sc_pre = int(previous_seg[7]), int(previous_seg[9]) 
        
    # only if call from stepDJ (forward process), we have to adjust the index of current_seg_info
    if (call_from_SemiOptConnAlg_function == False and call_from_backward_DJ == False):
        sa_cur, sd_cur = int(current_seg_info[6]+previous_seg[5]+1), int(current_seg_info[8]+previous_seg[5]+1)
        sb_cur, sc_cur = int(current_seg_info[7]+previous_seg[5]+1), int(current_seg_info[9]+previous_seg[5]+1)  
        current_seg_info[4] += previous_seg[5]+1
        current_seg_info[5] += previous_seg[5]+1        
    else:
        sa_cur, sd_cur = int(current_seg_info[6]), int(current_seg_info[8])
        sb_cur, sc_cur = int(current_seg_info[7]), int(current_seg_info[9])        

    # call from stepDJ (forward pass): if the current_seg[4] is below previous_seg[5], find the intersection of lk and lk+1, if not semi, then case3
    # call from SemiOptConnAlg_function: if the current_seg[4] is below previous_seg[5], find the intersection of lk and uk+1, if not semi, then case2, if semi, then case1
    # call from stepDJ (backward pass): if the current_seg[4] is below previous_seg[5], find the intersection of lk and uk+1, if not semi, continue loop in backward DJ
    if previous_seg[10] == 0: 
        # if call from stepDJ, calculate (x_ll, y_ll)
        if (call_from_SemiOptConnAlg_function == False and call_from_backward_DJ == False):
            x_extrm, _ = intersect.GetIntersectPointofLines(sa_pre, timeseries_up[sa_pre], sc_pre, timeseries_low[sc_pre], 
                                                            sa_cur, timeseries_up[sa_cur], sc_cur, timeseries_low[sc_cur])
            max_x_extrm = sc_cur 
        # else calculate(x_lu, y_lu)
        else:
            x_extrm, _ = intersect.GetIntersectPointofLines(sa_pre, timeseries_up[sa_pre], sc_pre, timeseries_low[sc_pre], 
                                                            sb_cur, timeseries_low[sb_cur], sd_cur, timeseries_up[sd_cur])
            max_x_extrm = sd_cur 
        # if two lines are parallel
        if x_extrm is None:
            semi_flag = False
        else:      
            # test if semi
            if x_extrm < sc_pre: 
                semi_flag = False
            elif (x_extrm >= previous_seg[5] and x_extrm < current_seg_info[4]):
                semi_flag = True # caution: the case that previous_seg contains only 2 points is included here
                                 # caution: the case that sc_pre == previous_seg[5] is included here
            elif (x_extrm >= current_seg_info[4] and within_flag == 0):# in case of slope(lk+1) >= slope(lk) or slope(uk+1) >= slope(lk)
                semi_flag = False               
            ####    
            elif(x_extrm >= current_seg_info[4] and x_extrm <= max_x_extrm and within_flag == 1): 
                semi_flag = True
            elif(x_extrm > current_seg_info[5] and within_flag == 1):
                semi_flag = False     
            ####
            else: # sc_pre <= x_extrm < previous_seg[5]
                timestamp_check = np.arange(int(np.ceil(x_extrm)), int(previous_seg[5]+1), 1) # caution previous_seg[5]+1
                # caution: use lk+1 or uk+1
                if (call_from_SemiOptConnAlg_function == False and call_from_backward_DJ == False):
                    intersection_value = ((timeseries_low[sc_cur] - timeseries_up[sa_cur]) / (sc_cur - sa_cur)) * (timestamp_check - sa_cur) + timeseries_up[sa_cur] # y = ((yc-ya)/(xc-xa))*(x-xa)+ya
                else:
                    intersection_value = ((timeseries_up[sd_cur] - timeseries_low[sb_cur]) / (sd_cur - sb_cur)) * (timestamp_check - sb_cur) + timeseries_up[sb_cur] # y = ((yd-yb)/(xd-xb))*(x-xd)+yb
                if (np.all(intersection_value >= timeseries_low[timestamp_check])): # caution '>='
                    semi_flag = True
                else:
                    semi_flag = False   
    # call from stepDJ (forward pass): if the current_seg[4] is upon previous_seg[5], find the intersection of uk and uk+1, if not semi, then case3
    # call from SemiOptConnAlg_function: if the current_seg[4] is upon previous_seg[5], find the intersection of uk and lk+1, if not semi, then case2, if semi, then case1
    # call from stepDJ (backward pass): if the current_seg[4] is upon previous_seg[5], find the intersection of uk and lk+1, if not semi, continue loop in backward DJ
    if previous_seg[10] == 1: 
        # if call from stepDJ, calculate (x_uu, y_uu)
        if (call_from_SemiOptConnAlg_function == False and call_from_backward_DJ == False):        
            x_extrm, _ = intersect.GetIntersectPointofLines(sb_pre, timeseries_low[sb_pre], sd_pre, timeseries_up[sd_pre], 
                                                            sb_cur, timeseries_low[sb_cur], sd_cur, timeseries_up[sd_cur])
            max_x_extrm = sd_cur 
        # else calculate(x_ul, y_ul)
        else:
            x_extrm, _ = intersect.GetIntersectPointofLines(sb_pre, timeseries_low[sb_pre], sd_pre, timeseries_up[sd_pre], 
                                                            sa_cur, timeseries_up[sa_cur], sc_cur, timeseries_low[sc_cur])  
            max_x_extrm = sc_cur 
        # if two lines are parallel
        if x_extrm is None:
            semi_flag = False
        else:   
            # test if semi
            if x_extrm < sd_pre:
                semi_flag = False            
            elif (x_extrm >= previous_seg[5] and x_extrm < current_seg_info[4]):
                semi_flag = True # caution: the case that previous_seg contains only 2 points is included here not in 'else'
                                 # caution: the case that sd_pre == previous_seg[5] is included here         
            elif (x_extrm >= current_seg_info[4] and within_flag == 0): # in case of slope(uk+1) <= slope(uk) or slope(lk+1) <= slope(uk)
                semi_flag = False  
            ####    
            elif(x_extrm >= current_seg_info[4] and x_extrm <= max_x_extrm and within_flag == 1): 
                semi_flag = True
            elif(x_extrm > current_seg_info[5] and within_flag == 1):
                semi_flag = False     
            ####
            else: # sd_pre <= x_extrm < previous_seg[5]
                timestamp_check = np.arange(int(np.ceil(x_extrm)), int(previous_seg[5]+1), 1) # caution previous_seg[5]+1
                # caution: use uk+1 or lk+1
                if (call_from_SemiOptConnAlg_function == False and call_from_backward_DJ == False): 
                    intersection_value = ((timeseries_up[sd_cur] - timeseries_low[sb_cur]) / (sd_cur - sb_cur)) * (timestamp_check - sb_cur) + timeseries_low[sb_cur] # y = ((yd-yb)/(xd-xb))*(x-xb)+yb
                else:
                    intersection_value = ((timeseries_low[sc_cur] - timeseries_up[sa_cur]) / (sc_cur - sa_cur)) * (timestamp_check - sa_cur) + timeseries_up[sa_cur] # y = ((yc-ya)/(xc-xa))*(x-xa)+ya
                if (np.all(intersection_value <= timeseries_up[timestamp_check])): # caution '<='
                    semi_flag = True
                else:
                    semi_flag = False       
                            
    return semi_flag                           
                           
                
def stepDJ(previous_seg, 
           max_error, 
           timeseries_data, 
           pending_seg,
           within_flag):   
    '''
    ''''''create one segment by DJ''''''
      
    Parameters
    ----------
    previous_seg : array (optional), e.g. [upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, extrm, trivial_label], 
                    extrm = -1 by default.
    max_error : float. 
    timeseries_data : array.
    max_min_in_timeseries_total : float.
    pending_seg : array (optional)
    
    Returns
    ----------
    seg : list, e.g. [upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, extrm, trivial_label]. The current segment. 
                   #   0    1    2   3      4       5    6   7   8   9    10         11      
    '''
    # initialization
    if pending_seg is not None: # DJ (backward process)
        timeseries_data_use = timeseries_data[int(previous_seg[4]):int(pending_seg[5]+1)][::-1]
    elif previous_seg is not None: # DJ (forward process), not the first segment
        timeseries_data_use = timeseries_data[int(previous_seg[5]+1):] # delete data in previous_seg from timeseries_data
    else: # DJ (forward process), the first segment
        timeseries_data_use = timeseries_data        
        
    timeseries_up = timeseries_data_use + max_error
    timeseries_low = timeseries_data_use - max_error 
    s_start = 0
    s_end = 1
    sa, sd = 0, 1
    sb, sc = 0, 1
    upl = (timeseries_low[sb]-timeseries_up[sd])/(sb-sd)
    lowl = (timeseries_up[sa]-timeseries_low[sc])/(sa-sc)
    cvx_up = [sa,sd]
    cvx_low = [sb,sc] 
    trivial_label = 0
    
    # if DJ (forward process)
    if pending_seg is None: 
        # 1. test if the current segment constructed by the first two data of timeseries_data_use can be semi-connected to previous_seg
        if previous_seg is not None:
            x0,y0 = intersect.GetIntersectPointofLines(sa, timeseries_up[sa], sc, timeseries_low[sc], 
                                                       sb, timeseries_low[sb], sd, timeseries_up[sd])            
            seg = np.array([upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, -1, trivial_label])
            semi_label  = test_semi(timeseries_data = timeseries_data, 
                                          max_error = max_error, 
                                          previous_seg = previous_seg,
                                          current_seg_info = seg,
                                          call_from_backward_DJ = False,
                                          call_from_SemiOptConnAlg_function = False,
                                          within_flag = within_flag)  
            # update the trivial statue of the current segment constructed by the first two points
            if semi_label == False:
                trivial_label = 1
 
            seg[11] = trivial_label           
            
        # 2. if timeseries_data_use contains more than 2 points, start DJ algorithm
        while s_end < len(timeseries_data_use)-1:
            if previous_seg is not None: # not precessing the first_seg
                # save the result of last interation before the new one, 
                # in case of not semi in the new iteration, but upl or lowl has been updated
                x0,y0 = intersect.GetIntersectPointofLines(sa, timeseries_up[sa], sc, timeseries_low[sc], 
                                                           sb, timeseries_low[sb], sd, timeseries_up[sd])
                seg = np.array([upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, -1, trivial_label])
            # new iteration
            s_end = s_end + 1
            if (timeseries_up[s_end] <= upl*(s_end-sb)+timeseries_low[sb]+2*max_error 
                    and timeseries_low[s_end] >= lowl*(s_end-sa)+timeseries_up[sa]-2*max_error):
                sd_changed = 0 
                cvx_flag = -1            
                if timeseries_up[s_end] < upl*(s_end-sb)+timeseries_low[sb]:
                    # updata upl, sb(optional), sd and cvx_up                
                    upl_candidate = [] 
                    for i in cvx_low:
                        upl_candidate.append([i,(timeseries_low[i]-timeseries_up[s_end])/(i-s_end)])
                    sb = upl_candidate[np.argmin(upl_candidate,axis=0)[1]][0]
                    sd = s_end
                    sd_changed = 1
                    cvx_low = [i for i in cvx_low if i >= sb] # sb has been updated, we only need to consider points after sb in cvx_low
                    upl = (timeseries_low[sb]-timeseries_up[sd])/(sb-sd)
                    cvx_up.append(sd)
                    cvx_flag = 1
                    cvx_up = tc_algorithm(cvx_up, cvx_flag, timeseries_up) # update cvx_up by triangle check    
                if timeseries_low[s_end] > lowl*(s_end-sa)+timeseries_up[sa]:
                    # updata lowl, sa(optional), sc and cvx_up
                    lowl_candidate = [] 
                    if sd_changed == 0:
                        for i in cvx_up:
                            lowl_candidate.append([i,(timeseries_up[i]-timeseries_low[s_end])/(i-s_end)])
                    else:
                        for i in cvx_up:
                            if i < sd: # if i=sd then pho=-inf                       
                                lowl_candidate.append([i,(timeseries_up[i]-timeseries_low[s_end])/(i-s_end)])
                    sa = lowl_candidate[np.argmax(lowl_candidate,axis=0)[1]][0]
                    sc = s_end
                    cvx_up = [i for i in cvx_up if i >= sa] # sa has been updated, we only need to consider points after sb in cvx_up             
                    lowl = (timeseries_up[sa]-timeseries_low[sc])/(sa-sc)
                    cvx_low.append(sc)  
                    cvx_flag = 0
                    cvx_low = tc_algorithm(cvx_low, cvx_flag, timeseries_low) # update cvx_low by triangle check                 
                # check semi_connection after updating upl or lowl
                if (previous_seg is not None and trivial_label != 1) : # not precessing the first_seg /  if label 1, as far as can
                    x0,y0 = intersect.GetIntersectPointofLines(sa, timeseries_up[sa], sc, timeseries_low[sc], 
                                                               sb, timeseries_low[sb], sd, timeseries_up[sd])
                    seg_check = np.array([upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, -1, trivial_label])
                    semi_label = test_semi(timeseries_data = timeseries_data, 
                                                          max_error = max_error, 
                                                          previous_seg = previous_seg, 
                                                          current_seg_info = seg_check, 
                                                          call_from_backward_DJ = False,
                                                          call_from_SemiOptConnAlg_function = False,
                                                          within_flag = within_flag) 
                    if semi_label == True: # in case of case1 or case2
                        seg = seg_check
                        continue
                    else: # in case of not semi (further depend on trivial_label)
                        #if trivial_label == 1:
                        #    continue # if extrmline_(k+1) becomes greater than or equal to extrmline_k
                        #else: # this is real case3
                        s_end = s_end - 1 # Caution s_end-1, avoid wrongly update seg in the "if" before return if s_end reach len(timeseries_data_use)-1
                        break
            else: # a new point is not located between the current upl and lowl
                s_end = s_end - 1 # Caution s_end-1, avoid re-calculate in the "if" before return if the s_end reach len(timeseries_data_use)-1
                if previous_seg is None: # precessing the first_seg
                    x0,y0 = intersect.GetIntersectPointofLines(sa, timeseries_up[sa], sc, timeseries_low[sc], 
                                                               sb, timeseries_low[sb], sd, timeseries_up[sd])
                    seg = np.array([upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, -1, trivial_label])                       
                break    
        
        # if all of timeseries_data_use can be included in the current segment, so s_end can reach len(timeseries_data_use)-1
        # or if len(timeseries_data_use) == 2
        if s_end == len(timeseries_data_use)-1: 
            x0,y0 = intersect.GetIntersectPointofLines(sa, timeseries_up[sa], sc, timeseries_low[sc], 
                                                       sb, timeseries_low[sb], sd, timeseries_up[sd])
            seg = np.array([upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, -1, trivial_label])        
        
    # else DJ (backward process)
    else:
        # determining the max value of s_end
        if previous_seg[10] == 0:
            s_end_max = pending_seg[5]-previous_seg[9]-1 
        elif previous_seg[10] == 1:
            s_end_max = pending_seg[5]-previous_seg[8]-1
        while s_end < s_end_max: 
            # new iteration
            s_end = s_end + 1
            if (timeseries_up[s_end] <= upl*(s_end-sb)+timeseries_low[sb]+2*max_error 
                    and timeseries_low[s_end] >= lowl*(s_end-sa)+timeseries_up[sa]-2*max_error):
                sd_changed = 0 
                cvx_flag = -1            
                if timeseries_up[s_end] < upl*(s_end-sb)+timeseries_low[sb]:
                    # updata upl, sb(optional), sd and cvx_up                
                    upl_candidate = [] 
                    for i in cvx_low:
                        upl_candidate.append([i,(timeseries_low[i]-timeseries_up[s_end])/(i-s_end)])
                    sb = upl_candidate[np.argmin(upl_candidate,axis=0)[1]][0]
                    sd = s_end
                    sd_changed = 1
                    cvx_low = [i for i in cvx_low if i >= sb] # sb has been updated, we only need to consider points after sb in cvx_low
                    upl = (timeseries_low[sb]-timeseries_up[sd])/(sb-sd)
                    cvx_up.append(sd)
                    cvx_flag = 1
                    cvx_up = tc_algorithm(cvx_up, cvx_flag, timeseries_up) # update cvx_up by triangle check    
                if timeseries_low[s_end] > lowl*(s_end-sa)+timeseries_up[sa]:
                    # updata lowl, sa(optional), sc and cvx_up
                    lowl_candidate = [] 
                    if sd_changed == 0:
                        for i in cvx_up:
                            lowl_candidate.append([i,(timeseries_up[i]-timeseries_low[s_end])/(i-s_end)])
                    else:
                        for i in cvx_up:
                            if i < sd: # if i=sd then pho=-inf                       
                                lowl_candidate.append([i,(timeseries_up[i]-timeseries_low[s_end])/(i-s_end)])
                    sa = lowl_candidate[np.argmax(lowl_candidate,axis=0)[1]][0]
                    sc = s_end
                    cvx_up = [i for i in cvx_up if i >= sa] # sa has been updated, we only need to consider points after sb in cvx_up             
                    lowl = (timeseries_up[sa]-timeseries_low[sc])/(sa-sc)
                    cvx_low.append(sc)  
                    cvx_flag = 0
                    cvx_low = tc_algorithm(cvx_low, cvx_flag, timeseries_low) # update cvx_low by triangle check      
                # do semi check only after the length of seg (construct from backward) > the length of pending_seg 
                if (s_end >= pending_seg[5] - pending_seg[4]):
                    x0,y0 = intersect.GetIntersectPointofLines(sa, timeseries_up[sa], sc, timeseries_low[sc], 
                                                               sb, timeseries_low[sb], sd, timeseries_up[sd])
                    # adjust the index of seg                        
                    seg = np.array([-lowl,                   # exchange upl and lowl
                                    -upl,                    # exchange upl and lowl
                                    pending_seg[5]-x0,      # s_end of pending_seg - x0
                                    y0,                     # y0 is the same
                                    pending_seg[5]-s_end,   # s_end of pending_seg - s_end, i.e. change s_start with s_end
                                    pending_seg[5]-s_start, # s_end of pending_seg - s_start(0), i.e. change s_end with s_start
                                    pending_seg[5]-sd,      # s_end of pending_seg - sd. i.e. change sa with sd
                                    pending_seg[5]-sc,      # s_end of pending_seg - sc. i.e. change sb with sc
                                    pending_seg[5]-sa,      # s_end of pending_seg - sa. i.e. change sd with sa
                                    pending_seg[5]-sb,      # s_end of pending_seg - sb. i.e. change sc with sb
                                    pending_seg[10],        # use the extrm of pending_seg
                                    pending_seg[11]])       # use the trivial_label of pending_seg

                    #only update previous_seg[5]
                    previous_seg[5] = pending_seg[5]-s_end-1
                    
                    # test semi stepwisely
                    semi_label = test_semi(timeseries_data = timeseries_data, 
                                              max_error = max_error, 
                                              previous_seg = previous_seg, 
                                              current_seg_info = seg, 
                                              call_from_backward_DJ = True,
                                              call_from_SemiOptConnAlg_function = False,
                                              within_flag = within_flag)                         
                    # if semi
                    if semi_label == True:
                        s_end = s_end - 1  
                        break                        
            # a new point is not located between the current upl and lowl before semi_label becomes True
            else: 
                seg = pending_seg    
                break

        if s_end == s_end_max:
            seg = pending_seg    
                    
    return seg                



def SemiOptConnAlg_function(previous_seg, 
                            new_seg, 
                            timeseries_data, 
                            max_error,
                            within_flag):
    '''
    Parameters
    ----------
    previous_seg : array, e.g. [upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, extrm, trivial_label] 
                            #   0     1    2   3      4       5    6   7   8   9    10         11 
    new_seg : array,      e.g. [upl, lowl, x0, y0, s_start, s_end, sa, sb, sd, sc, extrm, trivial_label]
    timeseries_data : array
    max_error : float
    sabdc_previous_seg: array, additional information - stepwise sa, sb, sd and sc result of previous_seg

    Returns
    -------
    new_seg : array
    '''
    
    inter_update = []
    case2 = 0
    
    # read data of previous_seg and new_seg  
    timeseries_up = timeseries_data + max_error
    timeseries_low = timeseries_data - max_error 
    sa_pre, sd_pre = int(previous_seg[6]), int(previous_seg[8])
    sb_pre, sc_pre = int(previous_seg[7]), int(previous_seg[9])  
    sa_cur, sd_cur = int(new_seg[6]), int(new_seg[8]) # the index of new_seg has been adjusted
    sb_cur, sc_cur = int(new_seg[7]), int(new_seg[9]) # the index of new_seg has been adjusted
    
    
    if new_seg[11] == 1:
        new_seg_update = new_seg
        inter_update.append([previous_seg[5], timeseries_low[int(previous_seg[5])] if previous_seg[10] == 0 else timeseries_up[int(previous_seg[5])]])
        inter_update.append([new_seg[4], timeseries_low[int(new_seg[4])] if new_seg[10] == 0 else timeseries_up[int(new_seg[4])]])
    
    # else case2 or case1, 
    # here we make sure that new_seg and previous_seg are semi because trivial_label {determined by (uk+1,uk) or (lk+1,lk)} != 1, 
    # and we exclude case3 in stepDJ (forward pass)                 
    else:
        # if (down, down) or (up, up), calculate (x_ll, y_ll) or (x_uu, y_uu), 
        # we make sure these can be calculated in stepDJ (forward pass)
        if previous_seg[10] == new_seg[10]:
            new_seg_update = new_seg
            if previous_seg[10] == 0: 
                x_ll, y_ll = intersect.GetIntersectPointofLines(sa_pre, timeseries_up[sa_pre], sc_pre, timeseries_low[sc_pre], 
                                                                sa_cur, timeseries_up[sa_cur], sc_cur, timeseries_low[sc_cur])
                inter_update.append([x_ll, y_ll])
            if previous_seg[10] == 1: 
                x_uu, y_uu = intersect.GetIntersectPointofLines(sb_pre, timeseries_low[sb_pre], sd_pre, timeseries_up[sd_pre], 
                                                                sb_cur, timeseries_low[sb_cur], sd_cur, timeseries_up[sd_cur])
                inter_update.append([x_uu, y_uu])    
        # if (down, up) or (up, down)
        else: 
            # test if semi, {determined by (lk,uk+1) or (uk,lk+1)}
            semi_label = test_semi(timeseries_data = timeseries_data, 
                                      max_error = max_error, 
                                      previous_seg = previous_seg,
                                      current_seg_info = new_seg, 
                                      call_from_backward_DJ = False,
                                      call_from_SemiOptConnAlg_function = True,
                                      within_flag = within_flag)
            # case2
            if semi_label == False: 
                case2 = 1
                # do stepDJ from backward
                # caution: extrm of previous_seg and new_seg will not be updated during backward DJ
                new_seg_update = stepDJ(previous_seg = previous_seg, 
                                        max_error = max_error, 
                                        timeseries_data = timeseries_data, 
                                        pending_seg = new_seg,
                                        within_flag = within_flag)
                
                # still can not turn to case1
                # we set semi point as (x_uu, y_uu) or (x_ll, y_ll)
                if all(new_seg_update == new_seg):
                    new_seg_update[10] = previous_seg[10] # caution: (lk, uk+1) or (uk,lk+1) can not semi, we thus do this
                    if previous_seg[10] == 0:  # we compute (x_ll, y_ll) instead of (x_lu, y_lu)  
                        x_ll, y_ll = intersect.GetIntersectPointofLines(sa_pre, timeseries_up[sa_pre], sc_pre, timeseries_low[sc_pre], 
                                                                        sa_cur, timeseries_up[sa_cur], sc_cur, timeseries_low[sc_cur])
                        inter_update.append([x_ll, y_ll])                    
                    elif previous_seg[10] == 1:  # we compute (x_uu, y_uu) instead of (x_ul, y_ul)  
                        x_uu, y_uu = intersect.GetIntersectPointofLines(sb_pre, timeseries_low[sb_pre], sd_pre, timeseries_up[sd_pre], 
                                                                        sb_cur, timeseries_low[sb_cur], sd_cur, timeseries_up[sd_cur])
                        inter_update.append([x_uu, y_uu])                           
                else: # new_seg has been updated to semi to previous_seg
                    semi_label = True
                    # update sa, sb, sc, sd 
                    # case2 can be turn to case1
                    sa_cur, sd_cur = int(new_seg_update[6]), int(new_seg_update[8]) 
                    sb_cur, sc_cur = int(new_seg_update[7]), int(new_seg_update[9])                                                                  
        
            # case1, originally or turn from case2
            if semi_label == True:
                if case2 == 0:
                    new_seg_update = new_seg
                if previous_seg[10] == 0: # new_seg[10] should be 1 because of contraint aboved
                    x_lu, y_lu = intersect.GetIntersectPointofLines(sa_pre, timeseries_up[sa_pre], sc_pre, timeseries_low[sc_pre], 
                                                                    sb_cur, timeseries_low[sb_cur], sd_cur, timeseries_up[sd_cur])
                    inter_update.append([x_lu, y_lu])  
                
                elif previous_seg[10] == 1: # new_seg[10] should be 0 because of contraint aboved
                    x_ul, y_ul = intersect.GetIntersectPointofLines(sb_pre, timeseries_low[sb_pre], sd_pre, timeseries_up[sd_pre], 
                                                                    sa_cur, timeseries_up[sa_cur], sc_cur, timeseries_low[sc_cur])
                    inter_update.append([x_ul, y_ul])  
    return new_seg_update, inter_update


def SemiOptConnAlg_algorithm(error_threshold, 
                             timeseries_data, 
                             max_min_in_timeseries_total):  

    # calculate max_error
    max_error = error_threshold * max_min_in_timeseries_total
    
    # for the storage of semi-connected points, e.g. [t,y], where t is the semi-connected timestamp, y is the corresponding value
    inter = []
    
    # create first segment by stepDJ
    first_seg = stepDJ(previous_seg = None, 
                       max_error = max_error, 
                       timeseries_data = timeseries_data, 
                       pending_seg = None,
                       within_flag = 0) 

    # if the end timestamp of first_seg equal to len(timeseries_data)-1, return the only segment
    if first_seg[5] == len(timeseries_data)-1:
        inter.append([first_seg[4], 0.5 * (first_seg[0] + first_seg[1]) * (first_seg[4] - first_seg[2]) + first_seg[3]])
        inter.append([first_seg[5], 0.5 * (first_seg[0] + first_seg[1]) * (first_seg[5] - first_seg[2]) + first_seg[3]])
        
    # if the end timestamp of first_seg equal to len(timeseries_data)-2, return the first_seg and the last point
    elif first_seg[5] == len(timeseries_data)-2: # in this case, we need to add a trivial segment
        inter.append([first_seg[4], 0.5 * (first_seg[0] + first_seg[1]) * (first_seg[4] - first_seg[2]) + first_seg[3]])
        inter.append([first_seg[5], 0.5 * (first_seg[0] + first_seg[1]) * (first_seg[5] - first_seg[2]) + first_seg[3]])
        inter.append([len(timeseries_data)-1, timeseries_data[-1]])
        
    # after creating the first_seg, there are at least two points left 
    else:
        # set first_seg as previous_seg for the next iteration
        previous_seg = first_seg
        
        # set extrm, update inter
        if timeseries_data[int(previous_seg[5])+1] < previous_seg[1] * (previous_seg[5]+1 - previous_seg[2]) + previous_seg[3]: # timeseries_data[s_end+1] < lowl * (s_end+1 - x0) + y0
            previous_seg[10] = 0 # extrm = 0
            inter.append([previous_seg[4], previous_seg[1] * (previous_seg[4] - previous_seg[2]) + previous_seg[3]]) # [s_start, lowl * (s_start - x0) + y0]
        elif timeseries_data[int(previous_seg[5])+1] > previous_seg[0] * (previous_seg[5]+1 - previous_seg[2]) + previous_seg[3]: # timeseries_data[s_end+1] > upl * (s_end+1 - x0) + y0
            previous_seg[10] = 1 # extrm = 1
            inter.append([previous_seg[4], previous_seg[0] * (previous_seg[4] - previous_seg[2]) + previous_seg[3]]) # [s_start, upl * (s_start - x0) + y0]
        
        # if there are at least two points left 
        while previous_seg[5] < len(timeseries_data)-2 : 
            # update within_flag
            if (((previous_seg[10] == 0) 
                 and 
                 (timeseries_data[int(previous_seg[5])+1] + max_error >= previous_seg[1] * (previous_seg[5]+1 - previous_seg[2]) + previous_seg[3]) 
                 and 
                 (timeseries_data[int(previous_seg[5])+1] - max_error <= previous_seg[1] * (previous_seg[5]+1 - previous_seg[2]) + previous_seg[3])) 
                or 
                ((previous_seg[10] == 1) 
                 and 
                 (timeseries_data[int(previous_seg[5])+1] + max_error >= previous_seg[0] * (previous_seg[5]+1 - previous_seg[2]) + previous_seg[3]) 
                 and 
                 (timeseries_data[int(previous_seg[5])+1] - max_error <= previous_seg[0] * (previous_seg[5]+1 - previous_seg[2]) + previous_seg[3]))): 
                
                within_flag = 1   
            else:
                within_flag = 0
                
            # create next segment by stepDJ            
            new_seg = stepDJ(previous_seg = previous_seg, 
                             max_error = max_error, 
                             timeseries_data = timeseries_data, 
                             pending_seg = None,
                             within_flag = within_flag)       
            
            # adjust the index of new_seg, and sabdc_new_seg
            new_seg[2] +=  previous_seg[5]+1
            new_seg[4:10] += previous_seg[5]+1

            # update extrm of new_seg 
            if new_seg[5] == len(timeseries_data)-1: # There is no data left after creating new_seg, we set the extrm of new_seg as the extrm of previous_seg, i.e. new_seg[10] = previous_seg[10]  
                new_seg[10] = previous_seg[10]
            else:
                # if there is at least one point left, we set the extrm of new_seg w.r.t. the position between the upcoming point and the extreme lines of new_seg
                mid_point = 0.5 * (new_seg[0]+new_seg[1]) * (new_seg[5]+1 - new_seg[2]) + new_seg[3]
                if timeseries_data[int(new_seg[5])+1] < mid_point: # timeseries_data[s_end+1] < 0.5* (upl + lowl) * (s_end+1 - x0) + y0 
                    new_seg[10] = 0 # extrm = 0 
                elif timeseries_data[int(new_seg[5])+1] >= mid_point: # timeseries_data[s_end+1] > upl * (s_end+1 - x0) + y0
                    new_seg[10] = 1 # extrm = 1   
                    
            # do SemiOptConnAlg  
            new_seg, inter_update = SemiOptConnAlg_function(previous_seg, new_seg, timeseries_data, max_error, within_flag) 
            for item in inter_update:
                inter.append(item)                
                
            # set new_seg as previous_seg for the next iteration
            previous_seg = new_seg
        
        # if there is no point left after 'while'
        if previous_seg[5] == len(timeseries_data)-1:
            # [s_end, (upl or lowl)*(s_end-x0)+y0]
            inter.append([previous_seg[5], (previous_seg[0] if previous_seg[10] == 1 else previous_seg[1]) * (previous_seg[5] - previous_seg[2]) + previous_seg[3]]) 
        # if there is only one point left after 'while'
        if previous_seg[5] == len(timeseries_data)-2:
            # [s_end, (upl or lowl)*(s_end-x0)+y0] and [len(timeseries_data)-1, timeseries_data[-1]]
            inter.append([previous_seg[5], (previous_seg[0] if previous_seg[10] == 1 else previous_seg[1]) * (previous_seg[5] - previous_seg[2]) + previous_seg[3]])
            inter.append([len(timeseries_data)-1, timeseries_data[-1]])
    
    return inter