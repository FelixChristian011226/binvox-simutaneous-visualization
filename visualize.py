import numpy as np
import binvox_rw
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import widgets

class LinkedRotation:
    def __init__(self, axes_list):
        self.axes_list = axes_list
        self.cids = [ax.figure.canvas.mpl_connect('button_press_event', self.on_press) for ax in axes_list]
        self.motion_cid = None

    def on_press(self, event):
        for ax in self.axes_list:
            if ax.in_axes(event):
                active_ax = ax
                break

        for ax in self.axes_list:
            if ax is not active_ax:
                ax.view_init(active_ax.elev, active_ax.azim)
            ax.figure.canvas.draw_idle()

        self.motion_cid = active_ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_motion(self, event):
        for ax in self.axes_list:
            if ax.figure.canvas == event.canvas:
                active_ax = ax
                break

        for ax in self.axes_list:
            if ax is not active_ax:
                ax.view_init(active_ax.elev, active_ax.azim)
            ax.figure.canvas.draw_idle()

    def disconnect(self):
        for cid in self.cids:
            cid.canvas.mpl_disconnect(cid)
        if self.motion_cid:
            self.axes_list[0].figure.canvas.mpl_disconnect(self.motion_cid)

def visualize_binvox_side_by_side(binvox_data_list):
    fig = plt.figure(figsize=(12, 6))

    # Create subplots for four binvox arrays
    ax1 = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222, projection='3d')
    ax3 = fig.add_subplot(223, projection='3d')
    ax4 = fig.add_subplot(224, projection='3d')

    axes_list = [ax1, ax2, ax3, ax4]

    for i, ax in enumerate(axes_list):
        binvox_data = binvox_data_list[i]

        # Get the indices of the true values in the binvox array
        x, y, z = np.indices(binvox_data.shape)
        voxels = (binvox_data != 0)

        # Plot the voxels
        ax.voxels(voxels, edgecolor='k')

        # Set the limits and labels
        ax.set_xlim([0, binvox_data.shape[0]])
        ax.set_ylim([0, binvox_data.shape[1]])
        ax.set_zlim([0, binvox_data.shape[2]])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # Rotate the view
        ax.view_init(elev=30, azim=-120)

    # Create a LinkedRotation object to link the rotations of subplots
    rotation = LinkedRotation(axes_list)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    binvox_files = ['models/original.binvox', 'models/pix2vox.binvox', 'models/pix2vox++.binvox', 'models/densenet.binvox']
    binvox_data_list = []

    for binvox_file in binvox_files:
        with open(binvox_file, 'rb') as f:
            binvox_data = binvox_rw.read_as_3d_array(f)
            binvox_data_list.append(binvox_data.data)

    visualize_binvox_side_by_side(binvox_data_list)
