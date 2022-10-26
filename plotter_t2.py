import matplotlib.pyplot as plt

for crt in [3,5,10,15,30]:
    with open(f"task_2_{crt}Mbps{5}Mbps.dat") as f:
        l = f.readlines()
        
    l = [a.split() for a in l]
    x = [float(t[0]) for t in l]
    y = [int(t[1]) for t in l]

    plt.figure()
    plt.plot(x,y,linewidth=1.5)
    plt.xlabel('time (in s)')
    plt.ylabel('Congestion window size' )
    plt.title(f'Congestion window size vs time \n Channel Rate: {crt}Mbps and application rate: 5Mbps')
    # plt.legend()
    plt.savefig(f'{crt}_5.png', dpi=300)

for crt in [1,2,4,8,12]:
    with open(f"task_2_{crt}Mbps{4}Mbps.dat") as f:
        l = f.readlines()
        
    l = [a.split() for a in l]
    x = [float(t[0]) for t in l]
    y = [int(t[1]) for t in l]

    plt.figure()
    plt.plot(x,y,linewidth=1.5)
    plt.xlabel('time (in s)')
    plt.ylabel('Congestion window size')
    plt.title(f'Congestion window size vs time  \n Channel Rate: {crt}Mbps and application rate: 4Mbps')
    # plt.legend()
    plt.savefig(f'{crt}_4.png', dpi=300)

