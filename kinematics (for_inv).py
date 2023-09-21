import numpy as np

def forward_kinematics(angles, lengths):
    # Check if the number of angles and lengths match
    if len(angles) != len(lengths):
        raise ValueError("Number of angles and lengths should be the same")

    # Initialize the transformation matrix
    transformation_matrix = np.eye(4)

    # Calculate the forward kinematics
    for i in range(len(angles)):
        angle = angles[i]
        length = lengths[i]

        # Calculate the transformation matrix for the current axis
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        transformation_matrix_i = np.array([[cos_theta, -sin_theta, 0, length*cos_theta],
                                            [sin_theta, cos_theta, 0, length*sin_theta],
                                            [0, 0, 1, 0],
                                            [0, 0, 0, 1]])

        # Update the overall transformation matrix
        transformation_matrix = np.dot(transformation_matrix, transformation_matrix_i)

    # Extract the position and orientation from the transformation matrix
    position = transformation_matrix[:3, 3]
    orientation = transformation_matrix[:3, :3]

    return position, orientation

def inverse_kinematics(target_position, target_orientation, lengths):
    # Check if the number of lengths matches the target position dimensions
    if len(lengths) != len(target_position):
        raise ValueError("Number of lengths should match the target position dimensions")

    # Initialize the angles list
    angles = []

    # Calculate the inverse kinematics
    for i in range(len(target_position)):
        length = lengths[i]

        # Calculate the angle for the current axis
        angle = np.arctan2(target_position[i], length)

        angles.append(angle)

    return angles

# Example usage
angles = [0.5, 1.2, 0.8]  # Angles for each axis
lengths = [1.0, 0.8, 0.6]  # Lengths for each axis

# Calculate forward kinematics
position, orientation = forward_kinematics(angles, lengths)
print("Forward Kinematics:")
print("Position: ", position)
print("Orientation:\n ", orientation)

# Calculate inverse kinematics
target_position = [0.5, 0.3, 0.2]  # Target position
target_orientation = np.eye(3)  # Target orientation (identity matrix)
calculated_angles = inverse_kinematics(target_position, target_orientation, lengths)
print("\nInverse Kinematics:")
print("Calculated Angles:", calculated_angles)