import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


# Read user config file for iPerf config
f1 = open('config.json')
data1 = json.load(f1)
f1.close()

# Run iPerf with user config, and Output iPerf data to file
exit_code = os.system(f"iperf3 -c {data1['servip']} -i {data1['interval']} -t {data1['time']} --json > {data1['clilog']}")
# --connect-timeout {data1['timeout']} seems can't be applied by my iPerf version

# Parse iPerf exit code and output file
f2 = open(data1['clilog'])
# data2 = json.load(f2)
data2 = json.loads("[{}]".format(f2.read().replace('}\n{', '},{')))
f2.close()

f3 = open('log.txt','w')

#Plot iPerf output data in a graph
for run in data2:
    for interval in run['intervals']:
        test_end = interval['streams'][0]['end']
        test_start = interval['streams'][0]['start']
        test_time = test_end - test_start
        test_bits = (interval['streams'][0]['bytes'])* 8 / 10**6
        os.system(f"echo {test_end},{test_bits} >> plot.txt")
        if exit_code == 0:
            print("\n Testing was successful!")
    
            def animate(i):
                graph_data = open('plot.txt','r').read()
                lines = graph_data.split('\n')
                tm = []
                bw = []
                for line in lines:
                    if len(line) > 1:
                        x, y = line.split(',')
                        tm.append(float(x))
                        bw.append(float(y))
                ax1.clear()
                ax1.plot(tm, bw)
            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()

        else: 
            error = data2[-1]['error']
            print("Testing was failed for the", error)



f3.close()
