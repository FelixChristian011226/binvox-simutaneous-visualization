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

def visualize_binvox_side_by_side(binvox_data1, binvox_data2):
    fig = plt.figure(figsize=(10, 5))

    # Create two sets of subplots, one for each binvox array
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')

    # Get the indices of the true values in each binvox array
    x, y, z = np.indices(binvox_data1.shape)
    voxels1 = (binvox_data1 != 0)
    voxels2 = (binvox_data2 != 0)

    # Plot the voxels of the first binvox array in blue
    ax1.voxels(voxels1, facecolors='b', edgecolor='k')

    # Set the limits and labels of the first subplot
    ax1.set_xlim([0, binvox_data1.shape[0]])
    ax1.set_ylim([0, binvox_data1.shape[1]])
    ax1.set_zlim([0, binvox_data1.shape[2]])
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')

    # Rotate the view of the first subplot
    ax1.view_init(elev=30, azim=-120)

    # Plot the voxels of the second binvox array in red
    ax2.voxels(voxels2, facecolors='r', edgecolor='k')

    # Set the limits and labels of the second subplot
    ax2.set_xlim([0, binvox_data2.shape[0]])
    ax2.set_ylim([0, binvox_data2.shape[1]])
    ax2.set_zlim([0, binvox_data2.shape[2]])
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')

    # Rotate the view of the second subplot
    ax2.view_init(elev=30, azim=-120)

    # Create a LinkedRotation object to link the rotations of both subplots
    rotation = LinkedRotation([ax1, ax2])

    # Show the plot
    plt.show()

if __name__ == '__main__':

    with open('models/model(1).binvox', 'rb') as f:
        m1 = binvox_rw.read_as_3d_array(f)

    with open('models/model(2).binvox', 'rb') as f:
        m2 = binvox_rw.read_as_3d_array(f)
    
    visualize_binvox_side_by_side(m1.data, m2.data)
