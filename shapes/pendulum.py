import os
import tempfile
import time
from utils.upload import upload_video
import numpy as np  # Dùng để tính toán
from manim import *

# Constants
g = 9.8  # Gia tốc trọng trường

def draw_pendulum_and_upload(L, m, theta_0):
    # Tạo thư mục tạm thời để lưu video
    with tempfile.TemporaryDirectory() as temp_dir:
        # Đặt tên file video với timestamp
        timestamp = int(time.time())  # Lấy timestamp hiện tại
        output_file = os.path.join(temp_dir, f"pendulum_L_{L}_m_{m}_theta_{theta_0}_{timestamp}.mp4")
        
        # Cấu hình đầu ra cho Manim để lưu video vào thư mục tạm thời
        config.media_dir = temp_dir
        config.output_file = output_file

        class PendulumScene(Scene):
            def construct(self):
                # Vị trí ban đầu
                pivot = np.array([0, 2, 0])  # Vị trí treo con lắc
                bob_radius = 0.1  # Bán kính quả cầu
                length = L  # Chiều dài dây
                theta_initial = np.radians(theta_0)  # Chuyển đổi góc sang radians

                # Tạo dây và vật nặng
                bob = Dot(radius=bob_radius, color=RED)  # Vật nặng
                rod = Line(pivot, pivot + length * np.array([np.sin(theta_initial), -np.cos(theta_initial), 0]))  # Dây
                
                bob.move_to(rod.get_end())
                
                # Nhóm các đối tượng con lắc
                pendulum = VGroup(rod, bob)
                self.add(pendulum)

                # Thời gian mô phỏng (trong giây)
                t_max = 10  # Mô phỏng trong 10 giây

                # Biến để theo dõi thời gian
                current_time = 0  # Thời gian hiện tại

                def update_pendulum(pendulum, dt):
                    nonlocal current_time  # Để sử dụng biến current_time trong hàm lồng
                    current_time += dt  # Cập nhật thời gian đã trôi qua
                    
                    # Phương trình dao động góc theo thời gian
                    theta_t = theta_initial * np.cos(np.sqrt(g / length) * current_time)
                    new_rod = Line(pivot, pivot + length * np.array([np.sin(theta_t), -np.cos(theta_t), 0]))
                    bob.move_to(new_rod.get_end())
                    pendulum.submobjects[0].become(new_rod)  # Cập nhật dây

                # Cập nhật chuyển động của con lắc theo thời gian
                pendulum.add_updater(update_pendulum)
                self.add(pendulum)
                
                # Chạy hoạt cảnh
                self.wait(t_max)
        
        try:
            # Tạo video của con lắc đơn
            scene = PendulumScene()
            scene.render()

            print(f"Đã tạo video cho con lắc đơn có chiều dài L={L}, khối lượng m={m}, và góc lệch ban đầu {theta_0} tại {output_file}")
            # Upload video lên Google Drive
            link_video = upload_video(output_file)
            print("Đã upload video lên Google Drive.")
            return link_video
        except Exception as e:
            print(f"Lỗi khi vẽ và upload video: {str(e)}")
