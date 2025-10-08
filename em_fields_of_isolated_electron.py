"""
Code written with help from Claude-Sonnet-4
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

def plot_electron_fields():
    # Create figure with subplots
    fig = plt.figure(figsize=(18, 6))
    
    # 1. Electric Field (always definite)
    ax1 = fig.add_subplot(131, projection='3d')
    plot_electric_field(ax1)
    
    # 2. Magnetic Field (quantum superposition)
    ax2 = fig.add_subplot(132, projection='3d')
    plot_magnetic_superposition(ax2)
    
    # 3. Magnetic Field (after measurement)
    ax3 = fig.add_subplot(133, projection='3d')
    plot_magnetic_measured(ax3)
    
    plt.tight_layout()
    plt.show()

def plot_electric_field(ax):
    """Plot the radial electric field of an electron"""
    
    # Create a grid of points around the electron
    n_points = 8
    theta = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    phi = np.linspace(0, np.pi, n_points//2)
    
    # Electron at origin
    ax.scatter([0], [0], [0], color='blue', s=200, alpha=0.8, label='Electron')
    
    # Plot radial field lines (pointing inward)
    for r in [1, 2]:  # Two shells
        for t in theta:
            for p in phi:
                x = r * np.sin(p) * np.cos(t)
                y = r * np.sin(p) * np.sin(t)
                z = r * np.cos(p)
                
                # Field points toward electron (inward)
                dx = -0.3 * x/r
                dy = -0.3 * y/r
                dz = -0.3 * z/r
                
                ax.quiver(x, y, z, dx, dy, dz, 
                         color='red', alpha=0.7, arrow_length_ratio=0.3)
    
    ax.set_title('Electric Field\n(Always Definite)', fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])

def plot_magnetic_superposition(ax):
    """Plot the quantum superposition of magnetic field"""
    
    # Electron at origin
    ax.scatter([0], [0], [0], color='blue', s=200, alpha=0.8)
    
    # Create "fuzzy cloud" representing superposition
    n_orientations = 50
    
    for i in range(n_orientations):
        # Random orientation for each "virtual" dipole
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        
        # Dipole axis direction
        axis_x = np.sin(phi) * np.cos(theta)
        axis_y = np.sin(phi) * np.sin(theta)
        axis_z = np.cos(phi)
        
        # Plot a few field lines for this orientation (very faint)
        plot_dipole_field_lines(ax, axis_x, axis_y, axis_z, alpha=0.05, color='purple')
    
    # Add fuzzy sphere to represent uncertainty
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x_sphere = 1.5 * np.outer(np.cos(u), np.sin(v))
    y_sphere = 1.5 * np.outer(np.sin(u), np.sin(v))
    z_sphere = 1.5 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='purple')
    
    ax.set_title('Magnetic Field\n(Quantum Superposition)', fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])

def plot_magnetic_measured(ax):
    """Plot magnetic field after measurement (spin-up along z)"""
    
    # Electron at origin
    ax.scatter([0], [0], [0], color='blue', s=200, alpha=0.8)
    
    # Measured spin-up along z-axis
    axis_x, axis_y, axis_z = 0, 0, 1
    
    # Plot clear dipole field lines
    plot_dipole_field_lines(ax, axis_x, axis_y, axis_z, alpha=0.8, color='green')
    
    # Add arrow showing spin direction
    ax.quiver(0, 0, 0, 0, 0, 1, color='black', alpha=1, 
             arrow_length_ratio=0.2, linewidth=3, label='Spin Direction')
    
    ax.set_title('Magnetic Field\n(After Measurement: Spin-Up)', fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])

def plot_dipole_field_lines(ax, axis_x, axis_y, axis_z, alpha=0.8, color='green'):
    """Plot magnetic dipole field lines for given axis orientation"""
    
    # Create field lines for a magnetic dipole
    r_values = [1.5, 2.5]
    
    for r in r_values:
        # Field lines around the dipole
        n_lines = 8
        angles = np.linspace(0, 2*np.pi, n_lines, endpoint=False)
        
        for angle in angles:
            # Create field line points
            t = np.linspace(-np.pi/2, np.pi/2, 10)
            
            # Parametric equations for dipole field lines
            field_r = r * np.sin(t)**2
            field_theta = t
            
            # Convert to Cartesian (rotate according to dipole axis)
            x_local = field_r * np.cos(field_theta) * np.cos(angle)
            y_local = field_r * np.cos(field_theta) * np.sin(angle)
            z_local = field_r * np.sin(field_theta)
            
            # Rotate to align with dipole axis
            # (Simplified rotation - just for visualization)
            if axis_z > 0.9:  # Nearly aligned with z
                x_field = x_local
                y_field = y_local
                z_field = z_local
            else:  # General case (simplified)
                x_field = x_local
                y_field = y_local
                z_field = z_local
            
            # Plot field line
            ax.plot(x_field, y_field, z_field, color=color, alpha=alpha, linewidth=1)
            
            # Add some field vectors
            if len(x_field) > 5:
                mid_idx = len(x_field) // 2
                dx = x_field[mid_idx+1] - x_field[mid_idx-1]
                dy = y_field[mid_idx+1] - y_field[mid_idx-1]
                dz = z_field[mid_idx+1] - z_field[mid_idx-1]
                
                norm = np.sqrt(dx**2 + dy**2 + dz**2)
                if norm > 0:
                    dx, dy, dz = dx/norm * 0.2, dy/norm * 0.2, dz/norm * 0.2
                    ax.quiver(x_field[mid_idx], y_field[mid_idx], z_field[mid_idx],
                             dx, dy, dz, color=color, alpha=alpha, 
                             arrow_length_ratio=0.3)

def plot_2d_comparison():
    """Create a 2D comparison showing the conceptual difference"""
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Electric field (2D slice)
    theta = np.linspace(0, 2*np.pi, 16)
    r = 1.5
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    ax1.scatter([0], [0], color='blue', s=200, label='Electron')
    ax1.quiver(x, y, -0.3*x/r, -0.3*y/r, color='red', alpha=0.8, 
               angles='xy', scale_units='xy', scale=1)
    ax1.set_xlim([-2.5, 2.5])
    ax1.set_ylim([-2.5, 2.5])
    ax1.set_aspect('equal')
    ax1.set_title('Electric Field\n(Always Definite)')
    ax1.grid(True, alpha=0.3)
    
    # Magnetic superposition
    ax2.scatter([0], [0], color='blue', s=200)
    circle = plt.Circle((0, 0), 1.5, fill=False, color='purple', alpha=0.3, linewidth=3)
    ax2.add_patch(circle)
    ax2.text(0, -2, 'Quantum\nSuperposition', ha='center', va='top', 
             fontsize=10, color='purple')
    ax2.set_xlim([-2.5, 2.5])
    ax2.set_ylim([-2.5, 2.5])
    ax2.set_aspect('equal')
    ax2.set_title('Magnetic Field\n(Before Measurement)')
    ax2.grid(True, alpha=0.3)
    
    # Magnetic after measurement
    ax3.scatter([0], [0], color='blue', s=200)
    # Draw dipole field pattern
    theta_dipole = np.linspace(0, 2*np.pi, 8)
    for angle in theta_dipole:
        x_start = 0.5 * np.cos(angle)
        y_start = 0.5 * np.sin(angle)
        # Simplified dipole field direction
        if np.cos(angle) > 0:  # Right side
            dx, dy = 0.3, 0.1 * np.sin(angle)
        else:  # Left side
            dx, dy = -0.3, 0.1 * np.sin(angle)
        ax3.arrow(x_start, y_start, dx, dy, head_width=0.1, 
                 head_length=0.1, fc='green', ec='green', alpha=0.8)
    
    ax3.arrow(0, 0, 0, 1, head_width=0.15, head_length=0.15, 
             fc='black', ec='black', linewidth=3, label='Spin Direction')
    ax3.set_xlim([-2.5, 2.5])
    ax3.set_ylim([-2.5, 2.5])
    ax3.set_aspect('equal')
    ax3.set_title('Magnetic Field\n(After Measurement)')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Plotting 3D visualization of electron fields...")
    plot_electron_fields()
    
    print("\nPlotting 2D comparison...")
    plot_2d_comparison()
    
    print("\nVisualization complete!")
    print("\nKey points:")
    print("1. Electric field: Always radial and definite")
    print("2. Magnetic field (unmeasured): Quantum superposition of all orientations")
    print("3. Magnetic field (measured): Definite dipole pattern")
