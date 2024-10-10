
# Thêm đường dẫn gốc vào sys.path
from scripts.redis_subscribe import RedisSubscribe  # Class Listener để kết nối Redis
from scripts.redis_publish import RedisPublish  # Class Listener để kết nối Redis
from shapes import pendulum  # Hàm vẽ và upload đã được định nghĩa
from shapes import spring_pendulum
from config import settings


def main():
    # Khởi tạo listener để kết nối đến Redis
    subscribe = RedisSubscribe(
        host=settings.REDIS_HOST,
        port=settings.REDIS_POST,
        # password=settings.REDIS_PASSWORD,  # Thay bằng khóa truy cập của bạn
    )

    publish = RedisPublish(
        host=settings.REDIS_HOST,
        port=settings.REDIS_POST,
        # password=settings.REDIS_PASSWORD
    )
    # Lắng nghe và nhận tin nhắn
    while True:
        message = subscribe.subscribe(settings.REDIS_CHANEL_SUB)  # Phương thức listen() sẽ trả về chuỗi message
        print(f"Tin nhắn nhận được: {message}")

        # Tách tin nhắn thành các phần tử
        parts = message.split(";")
        switch_case = parts[1]

        # Kiểm tra từng trường hợp của switch case
        if switch_case == "Pendulum":
            try:
                 # Tách các tham số từ phần tử thứ 2 (parameter)
                parameters = parts[2].split(",")  # Tách chuỗi dựa trên dấu phẩy
                L = float(parameters[0])  # Chiều dài con lắc
                m = float(parameters[1])  # Khối lượng con lắc
                theta_0 = float(parameters[2])  # Góc lệch ban đầu
                print(f"Case 1: Vẽ con lắc với L={L}, m={m}, theta_0={theta_0}")

                # Tạo video và upload lên Google Drive
                link_video = pendulum.draw_pendulum_and_upload(L, m, theta_0)
                if(link_video == None): {
                    print("None")
                }
                messagereturn = parts[0] + ',' + parts[3] + ',' + link_video
                publish.publish(settings.REDIS_CHANEL_PUB, messagereturn)
            except Exception as e:
                print(f"Lỗi khi xử lý case 1: {str(e)}")
        if switch_case == "Spring Pendulum":
            try:
                 # Tách các tham số từ phần tử thứ 2 (parameter)
                parameters = parts[2].split(",")  # Tách chuỗi dựa trên dấu phẩy
                L = float(parameters[0])  # Chiều dài con lắc
                m = float(parameters[1])  # Khối lượng con lắc
                A = float(parameters[2])  # Góc lệch ban đầu
                print(f"Case 1: Vẽ con lắc với L={L}, m={m}, A={A}")

                # Tạo video và upload lên Google Drive
                link_video = spring_pendulum.draw_spring_pendulum_and_upload(L, m, A)
                if(link_video == None): {
                    print("None")
                }
                messagereturn = parts[0] + ',' + parts[3] + ',' + link_video
                publish.publish(settings.REDIS_CHANEL_PUB, messagereturn)
            except Exception as e:
                print(f"Lỗi khi xử lý case 1: {str(e)}")
        else:
            print(f"Không có hành động cho switch case {switch_case}")

if __name__ == "__main__":
    main()