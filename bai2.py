from abc import ABC, abstractmethod
import re

class BaseLesson(ABC):
    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10

    def __init__(self, lesson_code, title):
        self.lesson_code = lesson_code
        self.title = title
        self.__duration_minutes = 0

    @property
    def duration_minutes(self):
        return self.__duration_minutes

    def _add_duration(self, minutes):
        self.__duration_minutes += minutes

    def _set_duration(self, minutes):
        self.__duration_minutes = minutes

    @abstractmethod
    def calculate_completion_score(self):
        pass

    @abstractmethod
    def update_content(self, new_data):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    @staticmethod
    def validate_lesson_code(lesson_code):
        return bool(re.fullmatch(r'LMS\d{7}', lesson_code))

    @classmethod
    def update_base_points(cls, new_points):
        cls.base_completion_points = new_points


class VideoLesson(BaseLesson):
    def __init__(self, lesson_code, title):
        super().__init__(lesson_code, title)
        self.video_quality = "1080p"
        self.view_count = 0

    def calculate_completion_score(self):
        return self.base_completion_points + (self.duration_minutes * 0.5)

    def update_content(self, new_data):
        if new_data <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
        self._set_duration(new_data)

    def play_video(self):
        self.view_count += 1


class CodingChallenge(BaseLesson):
    def __init__(self, lesson_code, title):
        super().__init__(lesson_code, title)
        self.number_of_testcases = 0
        self.difficulty_multiplier = 1.5

    def calculate_completion_score(self):
        return self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier

    def update_content(self, new_data):
        if new_data <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
        self.number_of_testcases = new_data


class HybridAssessment(VideoLesson, CodingChallenge):
    def __init__(self, lesson_code, title):
        super().__init__(lesson_code, title)

    def calculate_completion_score(self):
        video_score = self.base_completion_points + (self.duration_minutes * 0.5)
        coding_score = self.number_of_testcases * self.difficulty_multiplier
        return video_score + coding_score

    def update_content(self, new_data):
        if new_data <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
        self.number_of_testcases = new_data


class AWSS3StorageService:
    def upload_lesson(self, lesson):
        print(f"[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        print(f"Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Hệ thống lưu trữ đám mây đã upload toàn bộ tài nguyên của bài học {lesson.lesson_code} lên cụm máy chủ an toàn.")


class GoogleCloudStorageService:
    def upload_lesson(self, lesson):
        print(f"[Hệ thống Google Cloud]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        print(f"Xác thực dịch vụ bằng Duck Typing thành công!")
        print(f"Hệ thống lưu trữ đám mây đã upload toàn bộ tài nguyên của bài học {lesson.lesson_code} lên cụm máy chủ an toàn.")


def sync_to_cloud(cloud_service, lesson):
    try:
        cloud_service.upload_lesson(lesson)
    except AttributeError:
        print("Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa ký kết chứng chỉ API liên thông.")


def create_lesson():
    print("--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---")
    print("1. Video Lesson (Bài học Video Lý Thuyết)")
    print("2. Coding Challenge (Bài tập Thực Hành Code)")
    print("3. Hybrid Assessment (Bài Kiểm Tra Tổng Hợp)")
    choice = input("Chọn loại bài học (1-3): ").strip()
    match choice:
        case "1" | "2" | "3":
            pass
        case _:
            print("Lựa chọn không hợp lệ!")
            return None
    lesson_code = input("Nhập mã bài học 10 ký tự: ").strip()
    if not BaseLesson.validate_lesson_code(lesson_code):
        print("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.")
        return None
    title = " ".join(input("Nhập tiêu đề bài học: ").split()).upper()
    match choice:
        case "1":
            lesson = VideoLesson(lesson_code, title)
            print("Khởi tạo bài học Video thành công!")
        case "2":
            lesson = CodingChallenge(lesson_code, title)
            print("Khởi tạo bài tập Coding Challenge thành công!")
        case "3":
            lesson = HybridAssessment(lesson_code, title)
            print("Khởi tạo bài kiểm tra Hybrid thành công!")
    print(f"Tiêu đề bài học: {title}")
    return lesson


def view_info(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được tạo!")
        return
    print("--- THÔNG TIN BÀI HỌC HIỆN TẠI ---")
    print(f"Loại bài học: {type(current_lesson).__name__}")
    print(f"Nền tảng: {current_lesson.platform_name}")
    print(f"Mã bài học: {current_lesson.lesson_code}")
    print(f"Tiêu đề bài học: {current_lesson.title}")
    print(f"Thời lượng bài học: {current_lesson.duration_minutes} phút")
    if isinstance(current_lesson, VideoLesson):
        print(f"Chất lượng video: {current_lesson.video_quality}")
    if isinstance(current_lesson, CodingChallenge):
        print(f"Số lượng testcase lập trình: {current_lesson.number_of_testcases} bài")
    print("--- THỨ TỰ KẾ THỪA MRO ---")
    for cls in type(current_lesson).__mro__:
        print(f"  {cls}")


def update_lesson(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được tạo!")
        return
    print("--- CẬP NHẬT NỘI DUNG & THỜI LƯỢNG ---")
    print("1. Giả lập học viên tăng lượt xem video (Chỉ dành cho Video/Hybrid)")
    print("2. Cập nhật thông số bài học (Thời lượng, testcase...)")
    task = input("Chọn tác vụ (1-2): ").strip()
    match task:
        case "1":
            if not isinstance(current_lesson, VideoLesson):
                print("Chức năng này chỉ dành cho Video Lesson hoặc Hybrid Assessment!")
                return
            current_lesson.play_video()
            print("Ghi nhận thành công! Học viên đã xem video bài học.")
            print(f"Tổng số lượt xem hiện tại: {current_lesson.view_count} lượt.")
        case "2":
            try:
                if isinstance(current_lesson, CodingChallenge):
                    value = int(input("Nhập số lượng testcase kiểm thử mới bổ sung: ").strip())
                    current_lesson.update_content(value)
                    print("Cập nhật thông số thành công!")
                    print(f"Số lượng testcase hiện tại trên hệ thống: {current_lesson.number_of_testcases} testcases.")
                else:
                    value = float(input("Nhập thời lượng bài học (phút): ").strip())
                    current_lesson.update_content(value)
                    print("Cập nhật thời lượng thành công!")
                    print(f"Thời lượng hiện tại: {current_lesson.duration_minutes} phút.")
            except ValueError as e:
                print(e)
        case _:
            print("Lựa chọn không hợp lệ!")


def view_score(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được tạo!")
        return
    score = current_lesson.calculate_completion_score()
    print("--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH ---")
    print(f"Bài học: {current_lesson.title} (Loại: {type(current_lesson).__name__})")
    print(f"Điểm cơ sở hệ thống: {current_lesson.base_completion_points} XP")
    print(f"Thời lượng tích lũy: {current_lesson.duration_minutes} phút")
    if isinstance(current_lesson, CodingChallenge):
        print(f"Số lượng testcase cấu hình: {current_lesson.number_of_testcases} bài")
    print(f"Tổng điểm kinh nghiệm (XP) nhận được khi hoàn thành: {score:.0f} XP")


def compare_duration(current_lesson, lessons):
    if current_lesson is None:
        print("Chưa có bài học nào được tạo!")
        return
    others = [l for l in lessons if l.lesson_code != current_lesson.lesson_code]
    if not others:
        print("Không có bài học nào khác trong hệ thống để so sánh!")
        return
    print("--- ĐỒNG BỘ & SO SÁNH THỜI LƯỢNG (OPERATOR OVERLOADING) ---")
    print(f"Bài học hiện tại (A): {current_lesson.title} (Thời lượng: {current_lesson.duration_minutes} phút)")
    for i, l in enumerate(others):
        print(f"{i+1}. {l.lesson_code} ({l.title} - Thời lượng: {l.duration_minutes} phút)")
    try:
        idx = int(input("Chọn số thứ tự bài học đối ứng (B): ").strip()) - 1
        if idx < 0 or idx >= len(others):
            print("Lựa chọn không hợp lệ!")
            return
        other = others[idx]
        result_lt = current_lesson < other
        result_add = current_lesson + other
        if result_lt is NotImplemented or result_add is NotImplemented:
            print("Không thể so sánh với đối tượng không hợp lệ.")
            return
        msg = "NGẮN HƠN" if result_lt else "KHÔNG NGẮN HƠN"
        print(f"[Kết quả So sánh (__lt__)]: Thời lượng bài học A {msg} thời lượng bài học B.")
        print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời lượng học tập của cả 2 bài học là: {result_add} phút.")
    except (ValueError, TypeError):
        print("Lựa chọn không hợp lệ!")


def cloud_sync(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được tạo!")
        return
    print("--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---")
    print("1. Đồng bộ lên máy chủ AWS S3 Storage")
    print("2. Đồng bộ lên máy chủ Google Cloud Storage")
    choice = input("Chọn dịch vụ lưu trữ (1-2): ").strip()
    match choice:
        case "1":
            service = AWSS3StorageService()
        case "2":
            service = GoogleCloudStorageService()
        case _:
            print("Lựa chọn không hợp lệ!")
            return
    sync_to_cloud(service, current_lesson)


def main():
    lessons = []
    current_lesson = None
    while True:
        print("\n===== RIKKEI ACADEMY LMS SIMULATOR PRO =====")
        print("1. Khởi tạo bài học mới (Chọn loại bài học nội dung)")
        print("2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)")
        print("3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)")
        print("4. Xem chi tiết điểm thưởng hoàn thành bài học")
        print("5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)")
        print("6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)")
        print("7. Thoát chương trình")
        print("============================================")
        choice = input("Chọn chức năng (1-7): ").strip()
        match choice:
            case "1":
                lesson = create_lesson()
                if lesson:
                    lessons.append(lesson)
                    current_lesson = lesson
            case "2":
                view_info(current_lesson)
            case "3":
                update_lesson(current_lesson)
            case "4":
                view_score(current_lesson)
            case "5":
                compare_duration(current_lesson, lessons)
            case "6":
                cloud_sync(current_lesson)
            case "7":
                print("Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!")
                break
            case _:
                print("Chức năng không hợp lệ, vui lòng chọn từ 1-7.")

main()