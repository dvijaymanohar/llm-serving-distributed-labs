import subprocess, sys

for workers in [1,2,4,8]:
    for q in [8,32,128]:
        print(f"\nworkers={workers} queue={q}")
        subprocess.run([sys.executable,"examples/queue_simulator.py","--requests","500","--workers",str(workers),"--queue",str(q),"--service-ms","10"],check=True)
