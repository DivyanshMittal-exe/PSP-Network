import matplotlib.pyplot as plt

for prot in ["NewReno","Vegas","Veno","Westwood"]:
    with open(f"task_1_{prot}.dat") as f:
        l = f.readlines()
        
    l = [a.split() for a in l]
    x = [float(t[0]) for t in l]
    y = [int(t[1]) for t in l]

    plt.figure()
    plt.plot(x,y,label=f"TCP {prot}",linewidth=1.5)
    plt.xlabel('time (in s)')
    plt.ylabel('Congestion window size')
    plt.title('Congestion window size vs time ')
    plt.legend()
    plt.savefig(f'{prot}.png', dpi=300)

