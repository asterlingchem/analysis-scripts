import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
import numpy as np

# Plot 1 for dobpdc
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
# plt.show()

# Plot 2 for dobpdc
print('Plotting fine summary (plot 2)')

#                   --------shuffle------     ------peroxy------   ---------alkoxy--------
# array structure:   z   convex  concave  |  z   convex  concave  |  z   convex  concave  |
#           e-2   |                       |                       |                       |
#           en    |                       |                       |                       |
#           mm-2  |                       |                       |                       |

matrix2 = np.array([[0.00, 0.00, 0.00, 0.59, 0.81, 0.25, 0.44, 0.69, 0.06],
                    [0.00, 0.00, 0.00, 0.50, 0.75, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.66, 0.88, 0.13, 0.34, 0.75, 0.00]])

# Creating the 9x3 heat map
fig2, ax2 = plt.subplots(figsize=(8, 4))
cax2 = ax2.matshow(matrix2, cmap=cm)

# Label each cell with its value
for i in range(matrix2.shape[0]):
    for j in range(matrix2.shape[1]):
        ax2.text(j, i, f"{matrix2[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Replacing axis numbers with text labels
ax2.set_xticks(range(len(matrix2[0])))
ax2.set_yticks(range(len(matrix2)))
ax2.set_xticklabels(['a', 'concave', 'convex', 'a', 'concave', 'convex', 'a', 'concave', 'convex'], fontstyle='italic')
ax2.set_yticklabels(['e-2', 'en', 'mm-2'], fontweight='bold')

plt.tight_layout()
plt.savefig("heatmap_fine.pdf")
# plt.show()

# Plot 3 for dobpdc
print('Plotting fine summary with new TS (plot 3)')

# Creating the 2x3x6 heat map

#                   --------shuffle------    -------peroxy------
# array structure:   z   concave   convex |  z   concave  convex  |
#           e-2   |                       |                       |
#           en    |                       |                       |
#           mm-2  |                       |                       |

matrix3_top = np.array([[0.42, 0.67, 0.06, 0.56, 0.75, 0.11],
                        [0.19, 0.38, 0.00, 0.63, 0.47, 0.00],
                        [0.38, 0.68, 0.00, 0.49, 0.72, 0.08]])

#                   ----peroxy decomp----    ------alkoxy------
# array structure:   z   concave  convex  |  z   concave  convex  |
#           e-2   |                       |                       |
#           en    |                       |                       |
#           mm-2  |                       |                       |

matrix3_bottom = np.array([[0.68, 0.83, 0.28, 0.33, 0.53, 0.03],
                           [0.63, 0.67, 0.00, 0.19, 0.31, 0.00],
                           [0.73, 0.76, 0.16, 0.24, 0.64, 0.00]])


# Function to add dashed lines
def add_dashed_lines(ax, shape):
    # Vertical lines
    for x in range(1, shape[1]):
        if x % 3 == 0:  # Only after each 3 columns
            ax.axvline(x-0.5, color='black', linestyle='--', linewidth=0.5)


# Function to add thin dashed lines and remove lower tick marks
def customize_plot(ax, shape):
    add_dashed_lines(ax, shape)
    # Remove lower tick marks
    ax.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False)


fig3 = plt.figure(figsize=(6, 10))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.75)

# First 3x6 matrix
ax3_top = plt.subplot(gs[0])
cax3_top = ax3_top.matshow(matrix3_top, cmap=cm)
customize_plot(ax3_top, matrix3_top.shape)
for i in range(matrix3_top.shape[0]):
    for j in range(matrix3_top.shape[1]):
        ax3_top.text(j, i, f"{matrix3_top[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Second 6x3 matrix
ax3_bottom = plt.subplot(gs[1])
cax3_bottom = ax3_bottom.matshow(matrix3_bottom, cmap=cm)
customize_plot(ax3_bottom, matrix3_bottom.shape)
for i in range(matrix3_bottom.shape[0]):
    for j in range(matrix3_bottom.shape[1]):
        ax3_bottom.text(j, i, f"{matrix3_bottom[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Adjusting axis labels for demonstration (placeholders, adjust as needed)
ax3_top.set_xticks(range(6))
ax3_top.set_xticklabels(['a', 'concave', 'convex', 'a', 'concave', 'convex'], fontstyle='italic')
ax3_top.set_yticks(range(3))
ax3_top.set_yticklabels(['e-2', 'en', 'mm-2'], fontweight='bold')

ax3_bottom.set_xticks(range(6))
ax3_bottom.set_xticklabels(['a', 'concave', 'convex', 'a', 'concave', 'convex'], fontstyle='italic')
ax3_bottom.set_yticks(range(3))
ax3_bottom.set_yticklabels(['e-2', 'en', 'mm-2'], fontweight='bold')

plt.tight_layout()
plt.savefig("heatmap_fine_2x2.pdf")
plt.show()

# Plot 4 for olz
print('Plotting fine summary (plot 4) for olz')

# Creating the 2x3x6 heat map

#                  -shuffle- -peroxy--
# array structure:   z   c  |  z   c  |
#           e-2   |         |         |
#           mm-2  |         |         |

matrix4_top = np.array([[0.42, 0.06, 0.56, 0.08],
                        [0.38, 0.20, 0.49, 0.32]])

#                  -peroxy decomp- -alkoxy--
# array structure:      z   c    |  z   c  |
#           e-2   |              |         |
#           mm-2  |              |         |

matrix4_bottom = np.array([[0.68, 0.25, 0.33, 0.03],
                           [0.73, 0.52, 0.24, 0.08]])


# Function to add dashed lines
def add_dashed_lines_olz(ax, shape):
    # Vertical lines
    for x in range(1, shape[1]):
        if x % 2 == 0:  # Only after each 3 columns
            ax.axvline(x-0.5, color='black', linestyle='--', linewidth=0.5)


# Function to add thin dashed lines and remove lower tick marks
def customize_plot_olz(ax, shape):
    add_dashed_lines_olz(ax, shape)
    # Remove lower tick marks
    ax.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False)


fig4 = plt.figure(figsize=(6, 10))
gs4 = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.75)

# First 3x6 matrix
ax4_top = plt.subplot(gs4[0])
cax4_top = ax4_top.matshow(matrix4_top, cmap=cm)
customize_plot_olz(ax4_top, matrix4_top.shape)
for i in range(matrix4_top.shape[0]):
    for j in range(matrix4_top.shape[1]):
        ax4_top.text(j, i, f"{matrix4_top[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Second 6x3 matrix
ax4_bottom = plt.subplot(gs4[1])
cax4_bottom = ax4_bottom.matshow(matrix4_bottom, cmap=cm)
customize_plot_olz(ax4_bottom, matrix4_bottom.shape)
for i in range(matrix4_bottom.shape[0]):
    for j in range(matrix4_bottom.shape[1]):
        ax4_bottom.text(j, i, f"{matrix4_bottom[i, j]:.2f}", va='center', ha='center', color='black', fontweight='bold')

# Adjusting axis labels for demonstration (placeholders, adjust as needed)
ax4_top.set_xticks(range(4))
ax4_top.set_xticklabels(['a', 'c', 'a', 'c'], fontstyle='italic')
ax4_top.set_yticks(range(2))
ax4_top.set_yticklabels(['e-2', 'mm-2'], fontweight='bold')

ax4_bottom.set_xticks(range(4))
ax4_bottom.set_xticklabels(['a', 'c', 'a', 'c'], fontstyle='italic')
ax4_bottom.set_yticks(range(2))
ax4_bottom.set_yticklabels(['e-2', 'mm-2'], fontweight='bold')

plt.tight_layout()
plt.savefig("heatmap_fine_2x2_olz.pdf")
plt.show()
