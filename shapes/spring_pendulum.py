import os
import tempfile
import time
from utils.upload import upload_video
import numpy as np  # Dùng để tính toán
from manim import *

# Constants
k = 10  # Hằng số lò xo (N/m)
g = 9.8  # Gia tốc trọng trường

def draw_spring_pendulum_and_upload(L, m, A):
    # Tạo thư mục tạm thời để lưu video
    with tempfile.TemporaryDirectory() as temp_dir:
        # Đặt tên file video với timestamp
        timestamp = int(time.time())  # Lấy timestamp hiện tại
        output_file = os.path.join(temp_dir, f"spring_pendulum_L_{L}_m_{m}_A_{A}_{timestamp}.mp4")
        
        # Cấu hình đầu ra cho Manim để lưu video vào thư mục tạm thời
        config.media_dir = temp_dir
        config.output_file = output_file

        class SpringPendulumScene(Scene):
            def construct(self):
                # Vị trí ban đầu (điểm treo)
                pivot = np.array([0, 2, 0])  # Vị trí treo con lắc
                bob_radius = 0.1  # Bán kính quả cầu (vật nặng)
                rest_length = L  # Chiều dài tự nhiên của lò xo
                amplitude = A  # Biên độ dao động ban đầu
                omega = np.sqrt(k / m)  # Tần số góc của dao động điều hòa
                
                # Tạo vật nặng (bob)
                bob = Dot(radius=bob_radius, color=RED)  # Vật nặng
                
                # Hàm tạo lò xo bằng các đoạn thẳng nối liền nhau
                def create_spring(start, end, num_coils=20, coil_radius=0.1, coil_height=0.05):
                    spring = VGroup()  # Nhóm để chứa các đoạn thẳng tạo nên lò xo
                    coil_length = np.linalg.norm(end - start) / num_coils  # Chiều dài mỗi đoạn lò xo

                    # Tạo các đoạn của lò xo
                    for i in range(num_coils):
                        t = i / num_coils
                        angle = i * TAU / 2  # Góc quay để tạo hình xoắn ốc
                        x_offset = coil_radius * np.cos(angle)  # Tạo chuyển động theo phương ngang
                        z_offset = coil_radius * np.sin(angle)  # Tạo chuyển động theo phương z
                        start_point = start + np.array([x_offset, -coil_length * i, z_offset])
                        end_point = start + np.array([coil_radius * np.cos(angle + TAU / 2), -coil_length * (i + 1), coil_radius * np.sin(angle + TAU / 2)])
                        spring.add(Line(start_point, end_point))  # Thêm đoạn thẳng vào lò xo
                    return spring

                # Tạo lò xo ban đầu với chiều dài `rest_length`
                spring = create_spring(pivot, pivot + np.array([0, -rest_length, 0]))

                # Di chuyển vật nặng đến điểm cuối của lò xo
                bob.move_to(spring[-1].get_end())  # Vị trí cuối của lò xo

                # Nhóm các đối tượng con lắc lò xo
                pendulum = VGroup(spring, bob)
                self.add(pendulum)

                # Thời gian mô phỏng (trong giây)
                t_max = 10  # Mô phỏng trong 10 giây

                # Biến để theo dõi thời gian
                current_time = 0  # Thời gian hiện tại

                def update_spring_pendulum(pendulum, dt):
                    nonlocal current_time  # Để sử dụng biến current_time trong hàm lồng
                    current_time += dt  # Cập nhật thời gian đã trôi qua
                    
                    # Phương trình dao động của lò xo theo thời gian
                    extension = amplitude * np.cos(omega * current_time)  # Độ giãn của lò xo
                    new_spring_length = rest_length + extension  # Chiều dài mới của lò xo

                    # Cập nhật lò xo mới với chiều dài thay đổi
                    new_spring = create_spring(pivot, pivot + np.array([0, -new_spring_length, 0]))
                    bob.move_to(new_spring[-1].get_end())  # Di chuyển vật nặng theo vị trí mới của lò xo
                    pendulum.submobjects[0].become(new_spring)  # Cập nhật hình ảnh của lò xo

                # Cập nhật chuyển động của con lắc lò xo theo thời gian
                pendulum.add_updater(update_spring_pendulum)
                self.add(pendulum)
                
                # Chạy hoạt cảnh
                self.wait(t_max)
        
        try:
            # Tạo video của con lắc lò xo
            scene = SpringPendulumScene()
            scene.render()

            print(f"Đã tạo video cho con lắc lò xo có chiều dài L={L}, khối lượng m={m}, và biên độ A={A} tại {output_file}")
            # Upload video lên Google Drive
            link_video = upload_video(output_file)
            print("Đã upload video lên Google Drive.")
            return link_video
        except Exception as e:
            print(f"Lỗi khi vẽ và upload video: {str(e)}")
