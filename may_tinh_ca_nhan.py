import tkinter as tk

class UngDungMayTinh:
    def __init__(self, master):
        self.master = master
        self.master.title("Máy Tính Cá Nhân")
        self.master.geometry("360x520")
        self.master.resizable(False, False)
        # Nền đổi sang tone màu xanh nhạt thay vì xám
        self.master.configure(bg="#e8f4f8") 
        
        self.bieu_thuc = tk.StringVar(value="")
        
        # Khởi tạo giao diện
        self.tao_man_hinh()
        self.tao_ban_phim()

    def tao_man_hinh(self):
        """Tạo vùng hiển thị kết quả"""
        man_hinh = tk.Label(
            self.master, 
            textvariable=self.bieu_thuc, 
            font=("Consolas", 32, "bold"),
            bg="#e8f4f8", 
            fg="#2c3e50", 
            anchor="e", 
            padx=20, 
            pady=30
        )
        man_hinh.pack(fill="both")

    def xu_ly_bam(self, ky_tu):
        """Xử lý sự kiện khi bấm nút"""
        hien_tai = self.bieu_thuc.get()
        
        if ky_tu == "=":
            try:
                ket_qua = eval(hien_tai)
                # Tinh chỉnh định dạng hiển thị: loại bỏ đuôi .0 nếu là số nguyên
                if isinstance(ket_qua, float) and ket_qua.is_integer():
                    ket_qua = int(ket_qua)
                chuoi_moi = str(ket_qua)
            except Exception:
                chuoi_moi = "Lỗi"
        elif ky_tu == "AC":
            chuoi_moi = ""
        elif ky_tu == "Xóa":
            chuoi_moi = hien_tai[:-1]
        else:
            # Giới hạn độ dài biểu thức
            if len(hien_tai) < 15:
                chuoi_moi = hien_tai + ky_tu
            else:
                chuoi_moi = hien_tai
                
        self.bieu_thuc.set(chuoi_moi)

    def tao_ban_phim(self):
        """Tạo các phím bấm và phân bổ màu sắc tương ứng"""
        khung_phim = tk.Frame(self.master, bg="#e8f4f8")
        khung_phim.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Cấu trúc bố cục các phím (Thay C bằng AC, ⌫ bằng Xóa)
        cau_hinh_phim = [
            ["AC", "Xóa", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]
        
        for index_dong, dong in enumerate(cau_hinh_phim):
            khung_dong = tk.Frame(khung_phim, bg="#e8f4f8")
            khung_dong.pack(expand=True, fill="both")
            
            for index_cot, phim in enumerate(dong):
                # Thiết lập màu sắc theo chức năng của phím
                if phim == "=":
                    mau_nen = "#2980b9" # Màu xanh biển
                    mau_chu = "white"
                    mau_nhan = "#3498db"
                elif phim in ["AC", "Xóa", "%", "/", "*", "-", "+"]:
                    mau_nen = "#bdc3c7" # Màu xám nhạt
                    mau_chu = "#2c3e50"
                    mau_nhan = "#95a5a6"
                else:
                    mau_nen = "white"
                    mau_chu = "#2c3e50"
                    mau_nhan = "#ecf0f1"

                nut_bam = tk.Button(
                    khung_dong, 
                    text=phim, 
                    font=("Consolas", 16, "bold"),
                    bg=mau_nen, 
                    fg=mau_chu, 
                    activebackground=mau_nhan,
                    activeforeground=mau_chu,
                    bd=0, 
                    relief="flat", 
                    cursor="hand2",
                    command=lambda k=phim: self.xu_ly_bam(k)
                )
                
                # Chia tỉ lệ dàn đều các nút
                nut_bam.pack(side="left", expand=True, fill="both", padx=5, pady=5)

if __name__ == "__main__":
    cua_so = tk.Tk()
    ung_dung = UngDungMayTinh(cua_so)
    cua_so.mainloop()
