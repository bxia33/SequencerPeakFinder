import sys, operator, os


def peak_range(data, peaktab): # return the range of each peak
    peak_r = []                          # peak range
    for pos, value, left_range, right_range in peaktab:
        left_pos = left_range
        tmp_pos = pos
        while tmp_pos >= left_range:         # delimit left side
            if data[tmp_pos] <= data[tmp_pos-1]:
                left_pos = tmp_pos
                break
            tmp_pos -= 1
        right_pos = right_range
        tmp_pos = pos
        while tmp_pos <= right_range:  # delimit right side
            if data[tmp_pos] >= data[tmp_pos+1]:
                right_pos = tmp_pos
                break
            tmp_pos += 1
        peak_r.append((left_pos, right_pos))
        #print(left_pos, right_pos)
        
    return peak_r

def peak_area(data, peak_r):    # return the area of each peak
    peak_a = []                 
    for left_pos, right_pos in peak_r:
        pos = left_pos
        sum = 0
        while pos <= right_pos:
            sum += data[pos]
            pos +=1
        peak_a.append(sum*(right_pos-left_pos)/2.)
    return peak_a

def percentage_sub(peaktab,peak_a):
    product = 0
    substrate = 0
    for i in range(len(peaktab)):
        if peaktab[i][0]<1550:
            product += peak_a[i]
        else:
            substrate += peak_a[i]
    percentage = int(product/ (product+substrate)*10000)/100
    return str(percentage)+"%"


    
def peak_find(data, delta):     # find peak
    mn = float("inf")
    mx = -mn-1
    mxpos = mnpos = 0
    maxtab = []
    mintab = []

    lookformax = True
    mintab.append([0,0])
    for i in range(len(data)):
        
        if data[i] > mx:

            mx = data[i]
            mxpos = i
        if data[i] < mn:
            mn = data[i]
            mnpos = i

        if lookformax:
            if data[i] < mx-delta:
                maxtab.append([mxpos, mx])
                mn = data[i]
                mnpos = i
                lookformax = False
        else:
            if data[i] > mn+delta:
                mintab.append([mnpos, mn])
               # print(mintab[-1])
                mx = data[i]
                mxpos = i
                lookformax = True

    mintab.append([len(data),0])
    maxtab.sort(key=operator.itemgetter(0))

 
    

  #  product_pos = input("Please specify product peak: ")
  #  substrate_pos = input("Please sepcify substrate peak: ")

    peaktab = []
    for i in range(len(maxtab)):
        peaktab.append(maxtab[i]+[mintab[i][0],mintab[i+1][0]])
          

    
    #peaktab = [maxtab[0]+[0, mintab[0][0]], maxtab[-1]+[mintab[0][0], len(data)]] # Two peaks are found. Values in each peak: (pos, value, left_range, right_range)
    peak_r = peak_range(data, peaktab)
    peak_a = peak_area(data, peak_r)

    out_put = str(os.path.basename(f)+"\n#\tSize\tHeight\tL_range\tR_range\tArea")
    for j in range(len(peak_a)):
        out_put = out_put+"\n"+str(j+1)+"\t"+str(maxtab[j][0])+"\t"+str(maxtab[j][1])+"\t"+str(peak_r[j][0])+"\t"+str(peak_r[j][1])+"\t"+str(peak_a[j])
    out_put = out_put+"\n\t\t\t\t\t\tPercentage\t"+percentage_sub(peaktab,peak_a)+"\n----------------------------------\n"
    
    #print(out_put)
   
  
    f_result = open("result.xls", "a")
    f_result.write(out_put)
    f_result.close()
    
    #if sum(peak_a)==0:
    #   return peak_a[0], peak_a[1]
    #else:
     #  return peak_a[0], peak_a[1], str(min(peak_a)/sum(peak_a)*100)+"%"

def process_file(file_path, hold):
    with open(file_path) as f:
        string= f.read()

    data = string[string.find("DATA\t1"):string.find("DATA\t2")].split("\t")[-1].split()
    data = [int(x) for x in data]
    median = lambda x: sorted(x)[len(x)/2]
    print ("Processing file", file_path, ":")
    peak_find(data,hold)
    #print("percentage:",percentage(data)) 
   # print ("Results (area of peak1, area of peak2, smaller peak percentage):", peak_find(data, hold))
        



if __name__ == "__main__":
    hold = 100
    hold = input("Please input height cut off (default=100):")
    if hold=="":
        hold =100
    else:
        hold = int(hold)
    
  
    for parent, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.endswith("txt"):
                process_file(os.path.join(parent, f),hold)
        print ("Processing done.")
