import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from numpy.lib.stride_tricks import as_strided

def create_initial_array(size_y, size_x):
    """Initialize a random RGB array with velocities."""
    # Initialize RGB values (0.0-1.0)
    rgb = np.random.rand(size_y, size_x, 3)
    # Initialize velocities
    vel = (np.random.rand(size_y, size_x, 3) - 0.5) * 0.01
    return rgb, vel

def get_neighborhoods(array, window_size):
    """Get all neighborhoods at once using as_strided."""
    half = window_size // 2
    # Pad the array
    padded = np.pad(array, ((half, half), (half, half), (0, 0)), mode='empty')
    # Create a view of all neighborhoods
    shape = (array.shape[0], array.shape[1], window_size, window_size, array.shape[2])
    strides = (padded.strides[0], padded.strides[1], padded.strides[0], padded.strides[1], padded.strides[2])
    return as_strided(padded, shape=shape, strides=strides)

def update_frame(frame, rgb_array, vel_array, img, window_size, weights):
    """Update the frame using classic Boids flocking rules."""
    # Boids parameters
    max_speed = 0.02
    max_force = 0.002
    
    # Get weights from slider values
    separation_weight = weights['separation'].val
    alignment_weight = weights['alignment'].val
    cohesion_weight = weights['cohesion'].val
    
    # Get all neighborhoods at once
    rgb_neighborhoods = get_neighborhoods(rgb_array, window_size)
    vel_neighborhoods = get_neighborhoods(vel_array, window_size)
    
    # Reshape arrays for broadcasting
    current_rgb = rgb_array[:, :, np.newaxis, np.newaxis, :]
    current_vel = vel_array[:, :, np.newaxis, np.newaxis, :]
    
    # 1. Separation: Avoid crowding neighbors
    diff = current_rgb - rgb_neighborhoods
    distances = np.linalg.norm(diff, axis=4, keepdims=True)
    distances = np.where(distances > 0, distances, 1)
    diff = diff / distances
    separation = np.mean(diff, axis=(2, 3))
    norm = np.linalg.norm(separation, axis=2, keepdims=True)
    separation = np.where(norm > 0, separation / norm * max_speed, separation)
    separation = separation - current_vel[:, :, 0, 0, :]
    separation = np.clip(separation, -max_force, max_force)
    
    # 2. Alignment: Steer towards average heading of neighbors
    alignment = np.mean(vel_neighborhoods, axis=(2, 3))
    norm = np.linalg.norm(alignment, axis=2, keepdims=True)
    alignment = np.where(norm > 0, alignment / norm * max_speed, alignment)
    alignment = alignment - current_vel[:, :, 0, 0, :]
    alignment = np.clip(alignment, -max_force, max_force)
    
    # 3. Cohesion: Steer towards center of mass of neighbors
    cohesion = np.mean(rgb_neighborhoods, axis=(2, 3))
    desired = cohesion - current_rgb[:, :, 0, 0, :]
    norm = np.linalg.norm(desired, axis=2, keepdims=True)
    desired = np.where(norm > 0, desired / norm * max_speed, desired)
    cohesion = desired - current_vel[:, :, 0, 0, :]
    cohesion = np.clip(cohesion, -max_force, max_force)
    
    # Apply all forces
    acceleration = (separation_weight * separation + 
                   alignment_weight * alignment + 
                   cohesion_weight * cohesion)
    
    # Update velocity
    new_vel = vel_array + acceleration
    new_vel = np.clip(new_vel, -max_speed, max_speed)
    
    # Update position (RGB values)
    new_rgb = rgb_array + new_vel
    new_rgb = np.clip(new_rgb, 0.0, 1.0)
    
    # Update arrays
    rgb_array[:] = new_rgb
    vel_array[:] = new_vel
    
    # Only crop for display
    half = window_size // 2
    display_rgb = rgb_array[half:-half, half:-half]
    
    # Update the image
    img.set_array(display_rgb)
    return [img]

def create_animation(size_y=50, size_x=100, interval=50, window_size=10):
    """Create and return the animation."""
    # Set up the figure and axis
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes([0.1, 0.3, 0.8, 0.6])  # Main plot
    plt.axis('off')

    # Initialize the arrays
    rgb_array, vel_array = create_initial_array(size_y, size_x)

    # Create the initial plot (cropped for display only)
    half = window_size // 2
    display_rgb = rgb_array[half:-half, half:-half]
    img = ax.imshow(display_rgb, aspect='auto')

    # Create sliders
    ax_sep = plt.axes([0.1, 0.2, 0.8, 0.03])
    ax_ali = plt.axes([0.1, 0.15, 0.8, 0.03])
    ax_coh = plt.axes([0.1, 0.1, 0.8, 0.03])

    # Initialize weights dictionary
    weights = {
        'separation': Slider(ax_sep, 'Separation', 0.0, 5.0, valinit=1.5),
        'alignment': Slider(ax_ali, 'Alignment', 0.0, 5.0, valinit=2.3),
        'cohesion': Slider(ax_coh, 'Cohesion', 0.0, 5.0, valinit=4.0)
    }

    # Create the animation
    ani = FuncAnimation(
        fig, 
        lambda frame: update_frame(frame, rgb_array, vel_array, img, window_size, weights),
        interval=interval,
        blit=True,
        cache_frame_data=False
    )
    
    return ani

def main():
    """Main function to run the animation."""
    ani = create_animation(window_size=3, interval=15)
    plt.show()

if __name__ == '__main__':
    main() 