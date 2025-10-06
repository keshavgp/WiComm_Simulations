"""
Entire Code Created Using Claude-Sonnet-4
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Create 3D grid (avoiding the origin)
x, y, z = np.meshgrid(np.linspace(-2, 2, 8), 
                      np.linspace(-2, 2, 8), 
                      np.linspace(-2, 2, 8))

# Remove points too close to origin
mask = np.sqrt(x**2 + y**2 + z**2) > 0.3
x, y, z = x[mask], y[mask], z[mask]

# Calculate field components
r = np.sqrt(x**2 + y**2 + z**2)
Ex, Ey, Ez = -x/r**3, -y/r**3, -z/r**3

# Create figure
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Function to create field lines
def create_field_lines():
    field_lines = []
    
    # Create field lines from different starting points
    angles_theta = np.linspace(0, np.pi, 6)  # 6 lines in theta direction
    angles_phi = np.linspace(0, 2*np.pi, 8)  # 8 lines in phi direction
    
    for theta in angles_theta:
        for phi in angles_phi:
            # Starting point on a sphere around the charge
            start_r = 2.0
            start_x = start_r * np.sin(theta) * np.cos(phi)
            start_y = start_r * np.sin(theta) * np.sin(phi)
            start_z = start_r * np.cos(theta)
            
            # Create field line by following the field direction
            line_x, line_y, line_z = [start_x], [start_y], [start_z]
            
            # Trace the field line inward
            current_x, current_y, current_z = start_x, start_y, start_z
            
            for step in range(50):  # Number of steps along the field line
                # Calculate current position distance from origin
                current_r = np.sqrt(current_x**2 + current_y**2 + current_z**2)
                
                # Stop if too close to the charge
                if current_r < 0.2:
                    break
                
                # Calculate field direction (pointing inward)
                field_x = -current_x / current_r**3
                field_y = -current_y / current_r**3
                field_z = -current_z / current_r**3
                
                # Normalize field direction
                field_magnitude = np.sqrt(field_x**2 + field_y**2 + field_z**2)
                field_x /= field_magnitude
                field_y /= field_magnitude
                field_z /= field_magnitude
                
                # Step size (smaller steps for smoother lines)
                step_size = 0.05
                
                # Move along the field line
                current_x += field_x * step_size
                current_y += field_y * step_size
                current_z += field_z * step_size
                
                line_x.append(current_x)
                line_y.append(current_y)
                line_z.append(current_z)
            
            field_lines.append((np.array(line_x), np.array(line_y), np.array(line_z)))
    
    return field_lines

# Generate field lines once
field_lines = create_field_lines()

# Animation function with varying elevation and azimuth + selective axes removal
def animate(frame):
    ax.clear()
    
    # Plot faint continuous field lines FIRST (so arrows appear on top)
    for line_x, line_y, line_z in field_lines:
        ax.plot(line_x, line_y, line_z, color='lightblue', alpha=0.3, linewidth=0.8)
    
    # Plot field vectors with shorter length (0.1) ON TOP
    ax.quiver(x, y, z, Ex, Ey, Ez, length=0.1, color='blue', alpha=0.7)
    
    # Plot charge
    ax.scatter([0], [0], [0], color='red', s=200)
    
    # METHOD 2 ROTATION: Varying elevation and azimuth
    elev = 20 + 10 * np.sin(frame * 0.1)  # Varying elevation
    azim = frame * 2  # Rotating azimuth
    ax.view_init(elev=elev, azim=azim)
    
    # METHOD 2 AXES REMOVAL: Selective removal with more control
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_zticks([])  # Remove z-axis ticks
    
    # Remove axis labels
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')
    
    # Remove axis lines and panes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Make pane edges invisible
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    
    # Remove grid
    ax.grid(False)
    
    # Keep consistent axis limits (invisible)
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 360, 1),
                            interval=100, repeat=True)

# Save animation as professional quality GIF with 60 fps
ani.save('electric_field_rotation_pro.gif', writer='pillow', fps=60, dpi=150,
         savefig_kwargs={'bbox_inches': 'tight', 'pad_inches': 0.1})

plt.show()
