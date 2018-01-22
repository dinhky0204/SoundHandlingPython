def extend_space(list_f0, max_points, samplerate): #tinh khoang cach giua 2 cuc dai sau khi xep chong
    new_f0 = []
    extend_f0 = []
    for i in xrange(0, len(max_points)):
        tmp = int(len(list_f0)*(i+1)/len(max_points)) - 1
        new_f0.append(list_f0[tmp])
        print i

    for i in xrange(0, len(new_f0)-1):
        extend_f0.append(samplerate*2/(new_f0[i]+new_f0[i+1]))
    print extend_f0
    return extend_f0
def ghep_frame_thanh_huyen(extend_space, prev_signals, new_signal, number_sample_prev_frame):
    stack_up_space = int(number_sample_prev_frame/2 + len(new_signal)/2 - extend_space)
    # print "stack up space: ", stack_up
    # extend_space = int(extend_space/2)
    # extend_space = extend_space - len(new_signal)/2
    
    for i in xrange(0, stack_up_space):
        prev_signals[len(prev_signals) - i - 1] += new_signal[stack_up_space - i - 1]
    for i in xrange(stack_up_space, len(new_signal)):
        # prev_signals.extend(new_signal[i:i])
        prev_signals.append(new_signal[i])
    return prev_signals