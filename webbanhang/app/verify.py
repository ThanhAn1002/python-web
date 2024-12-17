import smtplib
from email.mime.text import MIMEText
import random
import time

# Hàm tạo mã xác minh gồm 6 chữ số
def generate_verification_code(length=6):
    return ''.join(random.choice('0123456789') for _ in range(length))

# Hàm gửi email
def send_verification_email():
    global verification_code, send_time
    verification_code = generate_verification_code()
    email_content = f'''Mã xác minh của bạn là:
    {verification_code}
    '''
    msg = MIMEText(email_content, _charset='utf-8')
    msg['Subject'] = 'Mã xác minh của bạn'
    msg['From'] = email_user
    msg['To'] = email_send

    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(email_user, email_password)
        session.sendmail(email_user, email_send, msg.as_string())
        session.quit()
        print("Email đã được gửi thành công!")
        send_time = time.time()  # Lưu thời gian gửi email
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gửi email: {e}")

# Thông tin email
email_user = 'thanhan2004thd@gmail.com'
email_password = 'nfyjpggtvkywckqk'
email_send = 'ngocson2811dn@gmail.com'

# Khởi tạo mã và thời gian gửi
verification_code = ""
send_time = 0

# Hàm kiểm tra mã xác minh
def check_verification_code():
    global verification_code, send_time

    while True:
        if verification_code == "":  # Nếu chưa có mã, gửi mã mới
            send_verification_email()

        while True:
            # Kiểm tra thời gian
            if time.time() - send_time > 5:
                print("Mã xác minh đã hết hạn! Bạn có muốn nhận lại mã mới?")
                resend = input("Nhấn 'y' để gửi lại mã xác minh, 'n' để thoát: ")
                if resend.lower() == 'y':
                    send_verification_email()  # Gửi lại mã
                    break  # Lặp lại vòng lặp ngoài
                else:
                    print("Chương trình kết thúc.")
                    return  # Kết thúc chương trình

            # Nhập mã xác minh từ người dùng
            user_code = input("Nhập mã xác minh bạn nhận được từ email: ")

            if user_code == verification_code:
                print("Mã xác minh chính xác! Thành công.")
                return  # Thoát khỏi chương trình khi mã đúng
            else:
                print("Mã xác minh sai. Vui lòng thử lại.")
                time.sleep(1)  # Dừng 1 giây trước khi yêu cầu nhập lại

# Kiểm tra mã xác minh
check_verification_code()
