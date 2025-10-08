"""
Code writtern with help from Claude-Sonnet-4
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def show_3d_spatial_propagation_only():
    """Show only the 3D spatial propagation plot"""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create spatial grid
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # Distance from origin
    R = np.sqrt(X**2 + Y**2)
    
    # Time snapshot
    t = 3
    
    # Field exists only where information has arrived (R < ct)
    Z = np.zeros_like(R)
    mask = R <= t  # ct with c=1
    
    # Inside the light cone: oscillating field
    Z[mask] = np.sin(2*np.pi*(R[mask] - t)) * np.exp(-(R[mask] - t)**2/2)
    
    # Plot the field
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    
    # Show the wavefront (circle at R = ct)
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = t * np.cos(theta)
    circle_y = t * np.sin(theta)
    circle_z = np.zeros_like(theta)
    ax.plot(circle_x, circle_y, circle_z, 'r-', linewidth=4, label='Wavefront')
    
    # Source at origin
    ax.scatter([0], [0], [0], color='red', s=200, label='Source')
    
    ax.set_xlabel('X distance')
    ax.set_ylabel('Y distance')
    ax.set_zlabel('Field strength')
    ax.set_title(f'3D Spatial Propagation at t={t}\nField exists only inside light cone', fontweight='bold')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

def create_rotating_3d_static_animation(save_gif=True, filename='em_wave_3d_rotating_static.gif'):
    """Create rotating animation of the static 3D spatial propagation plot"""
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create spatial grid (same as static plot)
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    
    # Fixed time snapshot
    t = 3
    
    # Field exists only where information has arrived (R < ct)
    Z = np.zeros_like(R)
    mask = R <= t
    Z[mask] = np.sin(2*np.pi*(R[mask] - t)) * np.exp(-(R[mask] - t)**2/2)
    
    def animate_rotation(frame):
        ax.clear()
        
        # Plot the field surface
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, 
                              linewidth=0, antialiased=True)
        
        # Show the wavefront (circle at R = ct)
        theta = np.linspace(0, 2*np.pi, 100)
        circle_x = t * np.cos(theta)
        circle_y = t * np.sin(theta)
        circle_z = np.zeros_like(theta)
        ax.plot(circle_x, circle_y, circle_z, 'r-', linewidth=4, label='Wavefront')
        
        # Add some radial lines to show the circular nature
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            r_line = np.linspace(0, t, 20)
            x_line = r_line * np.cos(angle)
            y_line = r_line * np.sin(angle)
            z_line = np.zeros_like(r_line)
            ax.plot(x_line, y_line, z_line, 'k--', alpha=0.4, linewidth=1)
        
        # Source at origin
        ax.scatter([0], [0], [0], color='red', s=200, label='Source', zorder=5)
        
        # Set labels and title
        ax.set_xlabel('X distance', fontsize=12)
        ax.set_ylabel('Y distance', fontsize=12)
        ax.set_zlabel('Field strength', fontsize=12)
        ax.set_title(f'3D Spatial Propagation at t={t}\nField exists only inside light cone', 
                    fontsize=14, fontweight='bold')
        
        # Set consistent limits
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-1, 1])
        
        # Rotate the view - smoother rotation for 60fps
        elevation = 20 + 10 * np.sin(frame * 0.05)  # Slower elevation variation
        azimuth = frame * 1.5  # Slower rotation for smoother motion at 60fps
        ax.view_init(elev=elevation, azim=azimuth)
        
        ax.legend()
    
    # Create animation - more frames for 60fps
    frames = 240  # 4 seconds at 60fps for full rotation
    anim = FuncAnimation(fig, animate_rotation, frames=frames, interval=16.67, repeat=True, blit=False)
    
    # Save as GIF if requested
    if save_gif:
        print(f"Saving rotating 3D static animation as {filename}...")
        try:
            anim.save(filename, writer='pillow', fps=60, dpi=100,
                     savefig_kwargs={'bbox_inches': 'tight', 'pad_inches': 0.1})
            print(f"Rotating 3D static animation saved successfully as {filename}")
        except Exception as e:
            print(f"Error saving rotating 3D GIF: {e}")
    
    plt.show()
    return anim

def create_2d_propagation_animation_with_gif(save_gif=True, filename='em_wave_2d_propagation.gif'):
    """Create 2D propagation animation and optionally save as GIF"""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    def animate(frame):
        ax.clear()
        
        t = frame * 0.08  # Slower time progression for smoother 60fps animation
        
        # 2D spatial propagation
        x2d = np.linspace(-6, 6, 150)
        y2d = np.linspace(-6, 6, 150)
        X, Y = np.meshgrid(x2d, y2d)
        R = np.sqrt(X**2 + Y**2)
        
        # Field pattern - more complex wave
        Z = np.zeros_like(R)
        mask = R <= t
        
        if np.any(mask) and t > 0:
            # Create a more interesting wave pattern
            wave_component = np.sin(3*np.pi*(R[mask] - t)) * np.exp(-(R[mask] - t)**2/3)
            Z[mask] = wave_component
        
        # Create contour plot with more levels for smoother appearance
        levels = np.linspace(-0.8, 0.8, 21)
        contour = ax.contourf(X, Y, Z, levels=levels, cmap='RdBu_r', extend='both')
        
        # Add contour lines for better definition
        ax.contour(X, Y, Z, levels=levels[::2], colors='black', alpha=0.3, linewidths=0.5)
        
        # Wavefront circle (leading edge)
        if t > 0:
            circle_outer = plt.Circle((0, 0), t, fill=False, color='red', linewidth=3, linestyle='-')
            ax.add_patch(circle_outer)
            
            # Add inner circles to show wave structure
            for r in np.arange(0, t, 1.0):
                if r > 0:
                    circle_inner = plt.Circle((0, 0), r, fill=False, color='white', 
                                            linewidth=1, alpha=0.6, linestyle='--')
                    ax.add_patch(circle_inner)
        
        # Source at origin
        ax.scatter([0], [0], color='yellow', s=200, zorder=5, 
                  edgecolors='black', linewidth=2, label='Accelerating Charge')
        
        # Add field strength indicators
        if t > 0:
            ax.text(-5.5, 5, f'Time: t = {t:.2f}', fontsize=14, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
            ax.text(-5.5, 4.3, f'Wavefront radius: r = ct = {t:.2f}', fontsize=12,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        
        ax.set_xlim([-6, 6])
        ax.set_ylim([-6, 6])
        ax.set_aspect('equal')
        ax.set_xlabel('X distance', fontsize=12)
        ax.set_ylabel('Y distance', fontsize=12)
        ax.set_title('Electromagnetic Wave Propagation\n(Field changes propagate at speed of light)', 
                    fontsize=14, fontweight='bold')
        
        # Add colorbar on first frame
        if frame == 0:
            cbar = plt.colorbar(contour, ax=ax, shrink=0.8)
            cbar.set_label('Field Strength', fontsize=12)
        
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
    
    # Create animation - more frames for 60fps
    frames = 300  # 5 seconds at 60fps
    anim = FuncAnimation(fig, animate, frames=frames, interval=16.67, repeat=True, blit=False)
    
    plt.tight_layout()
    
    # Save as GIF if requested
    if save_gif:
        print(f"Saving animation as {filename}...")
        try:
            # Save with 60fps
            anim.save(filename, writer='pillow', fps=60, dpi=100, 
                     savefig_kwargs={'bbox_inches': 'tight', 'pad_inches': 0.1})
            print(f"Animation saved successfully as {filename}")
        except Exception as e:
            print(f"Error saving GIF: {e}")
            print("Make sure you have Pillow installed: pip install Pillow")
    
    plt.show()
    return anim

def create_enhanced_3d_animation_with_gif(save_gif=True, filename='em_wave_3d_propagation.gif'):
    """Create enhanced 3D animation and save as GIF"""
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    def animate_3d(frame):
        ax.clear()
        
        t = frame * 0.1  # Slower time progression for 60fps
        
        # Create spatial grid
        x = np.linspace(-5, 5, 40)
        y = np.linspace(-5, 5, 40)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        
        # Field exists only where information has arrived (R < ct)
        Z = np.zeros_like(R)
        mask = R <= t
        
        if np.any(mask) and t > 0:
            # More complex wave pattern
            Z[mask] = (np.sin(2*np.pi*(R[mask] - t)) * 
                      np.exp(-(R[mask] - t)**2/4) * 
                      np.cos(np.pi*R[mask]/2))
        
        # Plot the field surface
        surf = ax.plot_surface(X, Y, Z, cmap='RdYlBu_r', alpha=0.8, 
                              linewidth=0, antialiased=True)
        
        # Show the wavefront (circle at R = ct)
        if t > 0:
            theta = np.linspace(0, 2*np.pi, 100)
            circle_x = t * np.cos(theta)
            circle_y = t * np.sin(theta)
            circle_z = np.zeros_like(theta)
            ax.plot(circle_x, circle_y, circle_z, 'r-', linewidth=4, label='Wavefront')
            
            # Add some radial lines to show propagation
            for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
                r_line = np.linspace(0, t, 20)
                x_line = r_line * np.cos(angle)
                y_line = r_line * np.sin(angle)
                z_line = np.zeros_like(r_line)
                ax.plot(x_line, y_line, z_line, 'k--', alpha=0.3, linewidth=1)
        
        # Source at origin
        ax.scatter([0], [0], [0], color='red', s=300, label='Source', zorder=5)
        
        # Set labels and title
        ax.set_xlabel('X distance', fontsize=12)
        ax.set_ylabel('Y distance', fontsize=12)
        ax.set_zlabel('Field strength', fontsize=12)
        ax.set_title(f'3D EM Wave Propagation (t={t:.2f})\nField exists only inside light cone', 
                    fontsize=14, fontweight='bold')
        
        # Set consistent view limits
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-1, 1])
        
        # Set viewing angle - slower rotation for 60fps
        ax.view_init(elev=20, azim=frame*0.75)  # Slower rotation
        
        ax.legend()
    
    # Create animation - more frames for 60fps
    frames = 300  # 5 seconds at 60fps
    anim = FuncAnimation(fig, animate_3d, frames=frames, interval=16.67, repeat=True, blit=False)
    
    # Save as GIF if requested
    if save_gif:
        print(f"Saving 3D animation as {filename}...")
        try:
            anim.save(filename, writer='pillow', fps=60, dpi=80,
                     savefig_kwargs={'bbox_inches': 'tight', 'pad_inches': 0.1})
            print(f"3D Animation saved successfully as {filename}")
        except Exception as e:
            print(f"Error saving 3D GIF: {e}")
    
    plt.show()
    return anim

if __name__ == "__main__":
    print("1. Showing 3D spatial propagation plot...")
    show_3d_spatial_propagation_only()
    
    print("\n2. Creating rotating 3D static animation at 60fps...")
    anim_rotating = create_rotating_3d_static_animation(save_gif=True, 
                                                       filename='em_wave_3d_rotating_static.gif')
    
    print("\n3. Creating 2D propagation animation at 60fps...")
    anim_2d = create_2d_propagation_animation_with_gif(save_gif=True, 
                                                      filename='em_wave_2d_propagation.gif')
    
    print("\n4. Creating enhanced 3D animation at 60fps...")
    anim_3d = create_enhanced_3d_animation_with_gif(save_gif=True, 
                                                   filename='em_wave_3d_propagation.gif')
    
    print("\nAll visualizations complete!")
    print("Generated files (all at 60fps):")
    print("- em_wave_3d_rotating_static.gif (3D rotating view of static snapshot)")
    print("- em_wave_2d_propagation.gif (2D time evolution)")
    print("- em_wave_3d_propagation.gif (3D time evolution with rotation)")
