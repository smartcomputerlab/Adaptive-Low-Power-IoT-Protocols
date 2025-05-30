if temp>thigh or temp<tlow :              # testing thresholds - urgent packet
            print("send urgent packet");  led.on()
            ncycle=1; npos=0; nneg=0; rtc_store_param(ncycle,npos,nneg)  # back to shoirtes cycle
            sdelta = dmin; rtc_store(sdelta)
            send_lora_data(ts_chan,ts_wkey,lumi, temp, humi)
            lora.receive()
            time.sleep(ACK_wait_time)
            print("data packet sent, no ack received") 
            send_data(ts_chan,ts_wkey,lumi, temp, humi)
..
        elif abs(ssens-temp)>sdelta or (thigh-temp)<sdelta or (temp-tlow)<sdelta:  
            print("send normal packet")
            rtc_store_sensor(temp) ; led.on()
            if npos :
                if ncycle > 2:
                    ncycle= int(ncycle/2)
                else:
                    if sdelta< dmax:
                        sdelta = sdelta+0.1*sdelta         # new delta
                        rtc_store_delta(sdelta)      
            npos=npos+1; nneg=0  # positive and negative counters
            rtc_store_param(ncycle,npos,nneg)
            send_lora_data(ts_chan,ts_wkey,lumi, temp, humi)
            lora.receive()
            time.sleep(ACK_wait_time)
            print("data packet sent, no ack received") 
            send_data(ts_chan,ts_wkey,lumi, temp, humi)
    
        else:
            print("data packet NOT sent")
            if nneg :
                if ncycle < cmax:
                    ncycle = int(ncycle*2)           # maximum factor 64 (64*15sec)
                else :
                    if sdelta> dmin:
                        sdelta = sdelta-0.1*sdelta
                        rtc_store_delta(sdelta)
                    
            npos=0; nneg=nneg+1
            rtc_store_param(ncycle,npos,nneg)  
            # waiting for ACK frame
        lora.sleep()                      # only for deepsleep
        time.sleep(0.1)
        print(ncycle*cdef)
        print(sdelta)
        deepsleep(ncycle*cdef*1000)                # 10*1000 miliseconds
        