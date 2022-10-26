import matplotlib.pyplot as plt


with open(f"task_3.dat") as f:
    l = f.readlines()
    
l = [a.split() for a in l]
x = [float(t[0]) for t in l]
y = [int(t[1]) for t in l]

plt.figure()
plt.plot(x,y,linewidth=1.5)
plt.xlabel('time (in s)')
plt.ylabel('Congestion window size' )
plt.title(f'Congestion window size vs time')
# plt.legend()
plt.savefig(f'task_3.png', dpi=300)



