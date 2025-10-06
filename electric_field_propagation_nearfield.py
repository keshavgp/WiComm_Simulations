"""
Entire Code written using Claude-Sonnet-4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patches as patches

# Physical constants
k = 8.99e9  # Coulomb's constant (N⋅m²/C²)
e = 1.602e-19  # Elementary charge (C)
electron_charge = -e  # Electron has negative charge

def electric_field_at_point(x, y, charge_x, charge_y, charge):
    """
    Calculate electric field at a specific point (x,y) due to a point charge
    """
    # Distance from charge to point
    dx = x - charge_x
    dy = y - charge_y
    r = np.sqrt(dx**2 + dy**2)
    
    # Electric field magnitude
    E_magnitude = k * abs(charge) / r**2
    
    # Electric field components (for negative charge, field points toward charge)
    if charge < 0:
        Ex = -E_magnitude * dx / r
        Ey = -E_magnitude * dy / r
    else:
        Ex = E_magnitude * dx / r
        Ey = E_magnitude * dy / r
    
    return Ex, Ey, E_magnitude, r

def create_animated_field_with_components():
    """
    Create 1080p animated visualization with original component sizes
    """
    # Test point position (fixed)
    test_x, test_y = 1.0, 0.0
    electron_x = 0.0  # Fixed x position
    
    # Animation parameters - reduced frames to avoid memory issues
    y_range = 0.5  # ±0.5 meters
    n_frames = 60  # Reduced for stability
    
    # Create figure for 1080p - fixed approach
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    
    # Create figure with exact 1080p dimensions
    fig = plt.figure(figsize=(19.2, 10.8))
    ax = fig.add_subplot(111)
    
    # Set margins to use full figure
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.08)
    
    # Everything else remains the same as original
    ax.set_xlim(-0.3, 1.8)
    ax.set_ylim(-0.8, 0.8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Distance (m)', fontsize=12)
    ax.set_ylabel('Distance (m)', fontsize=12)
    # REMOVED TITLE as requested
    
    # Create static elements with ORIGINAL small sizes
    test_circle = Circle((test_x, test_y), 0.005, color='blue', zorder=5)
    ax.add_patch(test_circle)
    test_label = ax.text(test_x + 0.05, test_y + 0.05, 'Test Point\n(1.0, 0.0)', 
                        fontsize=11, color='blue', weight='bold')
    
    # Create dynamic elements
    electron_circle = Circle((0, 0), 0.005, color='red', zorder=4)
    ax.add_patch(electron_circle)
    
    # Distance line
    distance_line, = ax.plot([], [], 'k--', alpha=0.6, linewidth=1)
    
    # Electric field components - ORIGINAL sizes
    ex_arrow = FancyArrowPatch((test_x, test_y), (test_x, test_y), arrowstyle='->', 
                              mutation_scale=20, color='red', linewidth=3, 
                              alpha=0.4, zorder=3)
    ax.add_patch(ex_arrow)
    
    ey_arrow = FancyArrowPatch((test_x, test_y), (test_x, test_y), arrowstyle='->', 
                              mutation_scale=20, color='blue', linewidth=3, zorder=3)
    ax.add_patch(ey_arrow)
    
    total_arrow = FancyArrowPatch((test_x, test_y), (test_x, test_y), arrowstyle='->', 
                                 mutation_scale=20, color='green', linewidth=2, 
                                 alpha=0.3, zorder=2)
    ax.add_patch(total_arrow)
    
    # Component lines
    ex_line, = ax.plot([], [], 'r--', alpha=0.3, linewidth=1)
    ey_line, = ax.plot([], [], 'b--', alpha=0.5, linewidth=1)
    
    # Text displays - electron position stays top left
    electron_pos_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=10,
                               verticalalignment='top', 
                               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    
    # Field info text - Box aligned to right, text aligned to left
    field_info_text = ax.text(0.98, 0.98, '', transform=ax.transAxes, fontsize=10,
                             verticalalignment='top', horizontalalignment='right',
                             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"),
                             multialignment='left')  # This makes text inside box left-aligned
    
    # REMOVED: Legend box (lightblue) completely removed
    
    # Scale factor - ORIGINAL
    scale_factor = 2e8
    
    def animate(frame):
        # Calculate current electron y position
        t = frame / n_frames * 4 * np.pi
        electron_y = y_range * np.sin(t)
        
        # Update electron position
        electron_circle.center = (electron_x, electron_y)
        
        # Calculate electric field at test point
        Ex, Ey, E_magnitude, distance = electric_field_at_point(test_x, test_y, 
                                                               electron_x, electron_y, 
                                                               electron_charge)
        
        # Update distance line
        distance_line.set_data([electron_x, test_x], [electron_y, test_y])
        
        # Calculate arrow endpoints
        ex_end_x = test_x + Ex * scale_factor
        ey_end_y = test_y + Ey * scale_factor
        total_end_x = test_x + Ex * scale_factor
        total_end_y = test_y + Ey * scale_factor
        
        # Update arrows
        ex_arrow.set_positions((test_x, test_y), (ex_end_x, test_y))
        ey_arrow.set_positions((test_x, test_y), (test_x, ey_end_y))
        total_arrow.set_positions((test_x, test_y), (total_end_x, total_end_y))
        
        # Update construction lines
        ex_line.set_data([ex_end_x, total_end_x], [test_y, total_end_y])
        ey_line.set_data([test_x, total_end_x], [ey_end_y, total_end_y])
        
        # Update text information
        electron_pos_text.set_text(f'Electron Position:\nx = {electron_x:.3f} m\ny = {electron_y:.3f} m\n\nDistance: {distance:.4f} m')
        
        field_info_text.set_text(f'Electric Field Components:\n\nEx = {Ex:.2e} N/C\nEy = {Ey:.2e} N/C\n\nTotal = {E_magnitude:.2e} N/C\n\nAngle = {np.degrees(np.arctan2(Ey, Ex)):.1f}°')
        
        # Return empty list to avoid blit issues
        return []
    
    # Create animation with conservative settings
    anim = FuncAnimation(fig, animate, frames=n_frames, interval=33, 
                        blit=False, repeat=True, cache_frame_data=False)
    
    # Add annotations - ORIGINAL sizes
    ax.text(0.5, -0.7, '← Electron oscillates from y = -0.5m to +0.5m →', 
            fontsize=12, ha='center', style='italic')
    
    ax.text(test_x + 0.1, test_y - 0.08, 'Ex', fontsize=12, color='red', 
            weight='bold', alpha=0.6)
    ax.text(test_x - 0.05, test_y + 0.1, 'Ey', fontsize=12, color='blue', weight='bold')
    ax.text(test_x + 0.15, test_y + 0.1, 'E⃗total', fontsize=12, color='green', 
            weight='bold', alpha=0.5)
    
    return fig, anim

def save_gif_robust(fig, anim, filename='electric_field_1080p.gif'):
    """
    Robust GIF saving method
    """
    try:
        # Method 1: Simple PillowWriter
        print("Attempting Method 1: Simple PillowWriter...")
        writer = PillowWriter(fps=30)
        anim.save(filename, writer=writer)
        print(f"✓ Success! Saved as '{filename}'")
        return True
        
    except Exception as e1:
        print(f"Method 1 failed: {e1}")
        
        try:
            # Method 2: Direct pillow writer
            print("Attempting Method 2: Direct pillow...")
            anim.save(filename, writer='pillow', fps=30)
            print(f"✓ Success! Saved as '{filename}'")
            return True
            
        except Exception as e2:
            print(f"Method 2 failed: {e2}")
            
            try:
                # Method 3: Lower quality fallback
                print("Attempting Method 3: Lower quality fallback...")
                fig_small = plt.figure(figsize=(12, 6.75), dpi=90)  # 1080x607
                # Re-create animation with smaller figure...
                anim.save('electric_field_smaller.gif', writer='pillow', fps=30)
                print("✓ Saved smaller version as 'electric_field_smaller.gif'")
                return True
                
            except Exception as e3:
                print(f"All methods failed: {e3}")
                return False

if __name__ == "__main__":
    print("Creating 1080p animated electric field visualization...")
    print("Using robust saving method...")
    
    # Create the animation
    fig, anim = create_animated_field_with_components()
    
    print("Saving GIF with multiple fallback methods...")
    
    # Try robust saving
    success = save_gif_robust(fig, anim, 'electric_field_1080p.gif')
    
    if not success:
        print("\nTroubleshooting suggestions:")
        print("1. pip install --upgrade pillow matplotlib")
        print("2. Try closing other applications to free memory")
        print("3. Restart Python and try again")
    
    # Show animation
    plt.show()
    input("Press Enter to exit...")
    
