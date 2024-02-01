import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Plot 1
print('Plotting coarse summary (plot 1)')

matrix = np.array([[0.00, 0.55, 0.40],
                   [0.00, 0.42, 0.00],
                   [0.00, 0.55, 0.36]])

# Green for 0, Red for 1
colors = [(0, 0.5, 0, 0.7), (1, 1, 0, 0.7), (1, 0, 0, 0.7)]  # RGB for Dark Forest Green, Yellow, Red
cmap_name = 'green_yellow_red'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Creating the heat map
fig, ax = plt.subplots(figsize=(6, 4))
cax = ax.matshow(matrix, cmap=cm)

# Adding the color bar
# plt.colorbar(cax)

# Label each cell with its value
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        ax.text(j, i, f"{matrix[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Replacing axis numbers with text labels
ax.set_xticks(range(len(matrix)))
ax.set_yticks(range(len(matrix)))
ax.set_xticklabels(['shuffle HAT', 'peroxy HAT', 'oxy HAT'])
ax.set_yticklabels(['e-2', 'en', 'mm-2'], fontweight='bold')

plt.tight_layout()
plt.savefig("heatmap_combined.pdf")
plt.show()

# Plot 2
print('Plotting fine summary (plot 2)')

matrix2 = np.array([[0.00, 0.00, 0.00, 0.59, 0.81, 0.25, 0.44, 0.69, 0.06],
                    [0.00, 0.00, 0.00, 0.50, 0.75, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.66, 0.88, 0.13, 0.34, 0.75, 0.00]])

# Creating the heat map
fig2, ax2 = plt.subplots(figsize=(8, 4))
cax2 = ax2.matshow(matrix2, cmap=cm)

# Label each cell with its value
for i in range(matrix2.shape[0]):
    for j in range(matrix2.shape[1]):
        ax2.text(j, i, f"{matrix2[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Replacing axis numbers with text labels
ax2.set_xticks(range(len(matrix2[0])))
ax2.set_yticks(range(len(matrix2)))
ax2.set_xticklabels(['z', 'concave', 'convex', 'z', 'concave', 'convex', 'z', 'concave', 'convex'])
ax2.set_yticklabels(['e-2', 'en', 'mm-2'], fontweight='bold')

plt.tight_layout()
plt.savefig("heatmap_fine.pdf")
plt.show()
