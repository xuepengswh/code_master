def genImeiLuhn(digits14): 
    digit15=0 
    for num in range(14): 
        if num%2==0: 
            digit15=digit15+int(digits14[num]) 
        else: 
            digit15=digit15+(int(digits14[num])*2)%10+(int(digits14[num])*2)/10 
    digit15=int(digit15)%10 
    if digit15==0: 
        digits14=digits14+str(digit15) 
    else: 
        digits14=digits14+str(10-digit15) 
    return digits14 
def genMassImei(stat14digits,amount,filepath): 
    fo=open(filepath,"w") 
    for num in range(amount): 
        imei=genImeiLuhn(stat14digits) 
        stat14digits=str(int(stat14digits)+1) 
        fo.write(imei+"\r\n") 
        print(imei) 
    fo.flush() 
    fo.close() 
genMassImei("12345678901234",1000,"imei2.txt")