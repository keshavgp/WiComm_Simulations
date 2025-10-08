"""
Code written with help from Claude-Sonnet-4
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as patches

# Physical constants
mu_0 = 4*np.pi*1e-7  # Permeability of free space (H/m)

def magnetic_field_from_dc_current_3d(x, y, z, current, conductor_x=0, conductor_y=0):
    """
    Calculate magnetic field at point (x,y,z) due to DC current in straight conductor along z-axis
    Using Ampère's law: B = μ₀I/(2πr) in circular direction around conductor
    """
    # Distance from conductor center (in x-y plane)
    dx = x - conductor_x
    dy = y - conductor_y
    r = np.sqrt(dx**2 + dy**2)
    
    if r < 1e-10:  # Avoid division by zero
        return 0, 0, 0, 0
    
    # Magnetic field magnitude
    B_magnitude = (mu_0 * current) / (2 * np.pi * r)
    
    # Direction: circular around conductor (right-hand rule)
    # For current going in +z direction, B-field circles counterclockwise when viewed from +z
    Bx = -B_magnitude * dy / r  # Tangential component
    By = B_magnitude * dx / r   # Tangential component
    Bz = 0  # No z-component for infinite straight conductor
    
    return Bx, By, Bz, B_magnitude

def create_3d_magnetic_field_visualization():
    """
    Create 3D visualization of magnetic field around DC conductor
    """
    # Conductor parameters
    conductor_length = 4.0  # meters
    conductor_radius = 0.02  # 2cm radius for visibility
    dc_current = 10.0  # Amperes
    
    # Create figure
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set up the plot
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_zlabel('Z (m)', fontsize=12)
    ax.set_title('3D Magnetic Field from DC Current in Straight Conductor', fontsize=14, weight='bold')
    
    # Make grid lines much fainter
    ax.grid(True, alpha=0.1, linewidth=0.5)  # Changed from default to very faint
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('gray')
    ax.yaxis.pane.set_edgecolor('gray')
    ax.zaxis.pane.set_edgecolor('gray')
    ax.xaxis.pane.set_alpha(0.1)  # Make panes very transparent
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)
    
    # Draw conductor as a cylinder along z-axis
    z_conductor = np.linspace(-conductor_length/2, conductor_length/2, 50)
    theta_conductor = np.linspace(0, 2*np.pi, 20)
    Z_cyl, Theta_cyl = np.meshgrid(z_conductor, theta_conductor)
    X_cyl = conductor_radius * np.cos(Theta_cyl)
    Y_cyl = conductor_radius * np.sin(Theta_cyl)
    
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, color='orange', alpha=0.8, linewidth=0)
    
    # Add current direction arrows along the conductor
    arrow_z_positions = np.linspace(-1.5, 1.5, 8)
    for z_pos in arrow_z_positions:
        ax.quiver(0, 0, z_pos, 0, 0, 0.2, color='red', arrow_length_ratio=0.3, linewidth=3)
    
    # Add current label
    ax.text(0.3, 0, 0, f'I = {dc_current} A\n↑ +Z direction', fontsize=12, color='red', weight='bold')
    
    # Create circular field lines at different z-levels
    z_levels = [-1.5, -0.75, 0, 0.75, 1.5]
    radii = [0.5, 1.0, 1.5]
    
    for z_level in z_levels:
        for radius in radii:
            theta = np.linspace(0, 2*np.pi, 100)
            x_circle = radius * np.cos(theta)
            y_circle = radius * np.sin(theta)
            z_circle = np.full_like(theta, z_level)
            ax.plot(x_circle, y_circle, z_circle, 'purple', alpha=0.4, linewidth=1)
    
    # Create 3D grid for field vectors
    x_grid = np.linspace(-1.8, 1.8, 6)
    y_grid = np.linspace(-1.8, 1.8, 6)
    z_grid = np.linspace(-1.5, 1.5, 5)
    
    # Calculate and plot magnetic field vectors
    max_field = 0
    field_data = []
    
    for x in x_grid:
        for y in y_grid:
            for z in z_grid:
                distance_from_conductor = np.sqrt(x**2 + y**2)
                if distance_from_conductor > conductor_radius * 3:  # Outside conductor
                    Bx, By, Bz, B_mag = magnetic_field_from_dc_current_3d(x, y, z, dc_current)
                    field_data.append((x, y, z, Bx, By, Bz, B_mag))
                    max_field = max(max_field, B_mag)
    
    # Plot field vectors
    arrow_scale = 0.4 / max_field if max_field > 0 else 1
    
    for x, y, z, Bx, By, Bz, B_mag in field_data:
        if B_mag > 0:
            # Color based on field strength
            color_intensity = min(B_mag / max_field, 1.0)
            if color_intensity > 0.7:
                color = 'magenta'
            elif color_intensity > 0.4:
                color = 'purple'
            else:
                color = 'indigo'
            
            ax.quiver(x, y, z, 
                     Bx * arrow_scale, By * arrow_scale, Bz * arrow_scale,
                     color=color, alpha=0.8, arrow_length_ratio=0.3, linewidth=2)
    
    # Add coordinate system arrows
    ax.quiver(1.5, 1.5, -1.8, 0.3, 0, 0, color='black', arrow_length_ratio=0.3, linewidth=2)
    ax.quiver(1.5, 1.5, -1.8, 0, 0.3, 0, color='black', arrow_length_ratio=0.3, linewidth=2)
    ax.quiver(1.5, 1.5, -1.8, 0, 0, 0.3, color='black', arrow_length_ratio=0.3, linewidth=2)
    ax.text(1.8, 1.5, -1.8, 'X', fontsize=12, weight='bold')
    ax.text(1.5, 1.8, -1.8, 'Y', fontsize=12, weight='bold')
    ax.text(1.5, 1.5, -1.5, 'Z', fontsize=12, weight='bold')
    
    # Add right-hand rule visualization
    ax.text(-1.8, -1.8, 1.5, 'Right-Hand Rule:\n👍 Thumb = Current (+Z)\n🤚 Fingers = B-field\n(Circular in X-Y plane)', 
           fontsize=10, color='blue', weight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    # Add physics info
    ax.text(-1.8, -1.8, -1.8, f'Magnetic Field (B):\n• B = μ₀I/(2πr)\n• I = {dc_current} A\n• Circular around conductor\n• Decreases as 1/r', 
           fontsize=10, color='darkgreen', weight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8))
    
    # Set viewing angle for best perspective
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Creating 3D visualization of magnetic field from DC current...")
    print("This shows the true 3D nature of the circular magnetic field!")
    print()
    
    # Create 3D visualization
    create_3d_magnetic_field_visualization()
    
    print("\nVisualization complete!")
    print("You can see the circular magnetic field pattern around the conductor.")
    print("The field vectors show the direction and relative strength of the B-field.")
    
    input("Press Enter to exit...")
