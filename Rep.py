class Rep():
    def __init__(self, rep_index, top_pose, bottom_pose, rep_poses):
        self.rep_index = rep_index
        self.start_pose = top_pose
        self.bottom_pose = bottom_pose
        self.rep_poses = rep_poses
    
    def draw(self):
        self.start_pose.draw_pose(f"pose_frames/rep_{self.rep_index}_start.jpg")
        self.bottom_pose.draw_pose(f"pose_frames/rep_{self.rep_index}_bottom.jpg")    