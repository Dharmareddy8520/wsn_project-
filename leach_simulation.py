import numpy as np
import random

# Network Parameters
xm, ym = 100, 100  # Field dimensions
n = 100  # Number of nodes
sinkx, sinky = 50, 50  # Sink coordinates
Eo = 0.5  # Initial energy of nodes
Eelec = 50 * 10**-9  # Energy for running circuitry
Eamp = 100 * 10**-12  # Energy for amplification
k = 2000  # Data packet size
p = 0.05  # Percentage of cluster heads

# LEACH Protocol Simulation
def run_leach():
    nodes = np.array([
        (i, random.randint(0, xm), random.randint(0, ym), Eo, 0, 0, 1, 0, 
         np.sqrt((random.randint(0, xm)-sinkx)**2 + (random.randint(0, ym)-sinky)**2), 0)
        for i in range(1, n + 1)
    ], dtype=[
        ('id', int), ('x', int), ('y', int), ('E', float),
        ('role', int), ('cluster', int), ('cond', int),
        ('rop', int), ('dts', float), ('tel', int)
    ])
    
    results = []
    rounds = 0
    while np.sum(nodes['cond']) > 0:
        cluster_heads = []
        # Select cluster heads
        for node in nodes:
            if node['cond'] == 1 and random.uniform(0, 1) <= p:
                node['role'] = 1
                cluster_heads.append(node)

        # Assign nodes to nearest cluster head
        for node in nodes:
            if node['cond'] == 1 and node['role'] == 0:
                distances = [np.sqrt((node['x'] - ch['x'])**2 + (node['y'] - ch['y'])**2) for ch in cluster_heads]
                if distances:
                    min_distance = np.argmin(distances)
                    energy_spent = Eelec * k + Eamp * k * distances[min_distance]**2
                    node['E'] -= energy_spent
                    if node['E'] <= 0:
                        node['cond'] = 0

        # Cluster head energy dissipation
        for ch in cluster_heads:
            if ch['cond'] == 1:
                ch['E'] -= Eelec * k
                if ch['E'] <= 0:
                    ch['cond'] = 0

        results.append((rounds, np.sum(nodes['cond'])))
        rounds += 1
        
        # Reset roles for next round
        nodes['role'] = 0
        
    return results

if __name__ == "__main__":
    print("Running LEACH simulation...")
    results = run_leach()
    print(f"Simulation completed with {len(results)} rounds.")