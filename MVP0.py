import os
import json
import matplotlib.pyplot as plt


# Read user config file for iPerf config
f1 = open('config.json')
data1 = json.load(f1)
f1.close()

# Run iPerf with user config, and Output iPerf data to file
exit_code = os.system(f"iperf3 -c {data1['servip']} -i {data1['interval']} -t {data1['time']} --json >> {data1['clilog']}")
# --connect-timeout {data1['timeout']} seems can't be applied by my iPerf version

# Parse iPerf exit code and output file
f2 = open(data1['clilog'])
# data2 = json.load(f2)
data2 = json.loads("[{}]".format(f2.read().replace('}\n{', '},{')))
f2.close()



#Plot iPerf output data in a graph
data_time = []
data_bits = []
for run in data2:
    for interval in run['intervals']:
        test_end = interval['streams'][0]['end']
        test_start = interval['streams'][0]['start']
        test_time = test_end - test_start
        test_bits = (interval['streams'][0]['bytes'])* 8 / 10**6
        print("Time:    ", test_time)
        print("Bandwidth:   ", test_bits)
        data_time.append(test_end)
        data_bits.append(test_bits / test_time)

#present result and graph
print(f"\niPerf3 exited with code {exit_code}")
if exit_code == 0:
    print("\n Testing was successful!")
    
    plt.title("iPerf Bandwidth test")
    plt.plot(data_time, data_bits)
    plt.xlabel('Time(sec)')
    plt.ylabel('Bandwidth(Mbits/sec)')
    plt.grid()
    plt.show()
else: 
    error = data2[-1]['error']
    print("Testing was failed for the", error)
