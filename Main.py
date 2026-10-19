import tkinter as tk
from tkinter import messagebox
import csv
import os
import time
from models import ItemGame
from UI import KomponenUI

class LoadingScreen:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        
        # Jendela Loading Screen ala Game Startup
        self.load_win = tk.Toplevel(root)
        self.load_win.overrideredirect(True)  # Tanpa tombol minimize/close standar
        self.load_win.geometry("450x250")
        self.load_win.configure(bg="#0d1117")
        
        # Posisikan di tengah layar
        self.load_win.update_idletasks()
        sw = self.load_win.winfo_screenwidth()
        sh = self.load_win.winfo_screenheight()
        x = (sw - 450) // 2
        y = (sh - 250) // 2
        self.load_win.geometry(f"450x250+{x}+{y}")

        # Label Judul Game
        tk.Label(self.load_win, text="⚡ NEXUS GAMING ENGINE ⚡", font=("Segoe UI", 14, "bold"), 
                 bg="#0d1117", fg="#58a6ff").pack(pady=(35, 10))
        
        self.lbl_status = tk.Label(self.load_win, text="Memuat modul inventaris...", font=("Segoe UI", 9), 
                                   bg="#0d1117", fg="#8b949e")
        self.lbl_status.pack(pady=5)

        # Progress Bar Buatan (Canvas)
        self.canvas = tk.Canvas(self.load_win, width=350, height=18, bg="#161b22", highlightthickness=0)
        self.canvas.pack(pady=15)
        self.progress_bar = self.canvas.create_rectangle(0, 0, 0, 18, fill="#238636", width=0)

        # Jalankan animasi loading secara asynchronous
        self.progress = 0
        self.root.after(50, self.animasi_loading)

    def animasi_loading(self):
        self.progress += 4
        current_width = int(350 * (self.progress / 100))
        self.canvas.coords(self.progress_bar, 0, 0, current_width, 18)

        if self.progress == 30:
            self.lbl_status.config(text="Menghubungkan ke database item.csv...")
        elif self.progress == 70:
            self.lbl_status.config(text="Menyiapkan antarmuka interaktif...")
        elif self.progress >= 100:
            self.load_win.destroy()
            self.on_complete()  # Buka aplikasi utama setelah loading selesai
            return

        self.load_win.after(30, self.animasi_loading)


class GameInventoryPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Item Inventory - RPG Edition")
        self.root.geometry("950x580")
        self.root.minsize(850, 500)
        
        # Palet Warna Game Dark Theme (Cyberpunk / RPG)
        self.bg_main = "#0d1117"
        self.bg_panel = "#161b22"
        self.border_color = "#30363d"
        
        self.root.configure(bg=self.bg_main)
        self.root.withdraw()  # Sembunyikan jendela utama dulu saat loading screen aktif

        # Tampilkan Loading Screen terlebih dahulu
        LoadingScreen(self.root, self.inisialisasi_aplikasi)

    def inisialisasi_aplikasi(self):
        self.root.deiconify()  # Munculkan kembali jendela utama
        self.buat_antarmuka()
        self.muat_data_tabel()

    def buat_antarmuka(self):
        # Header Game Banner
        header_outer, header_inner = KomponenUI.buat_panel_game(self.root, self.bg_panel, self.border_color)
        header_outer.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        lbl_judul = tk.Label(header_inner, text="🛡️ INVENTARIS ITEM GAME [RPG MODE] 🛡️", 
                             font=("Segoe UI", 15, "bold"), bg=self.bg_panel, fg="#f0883e")
        lbl_judul.pack(side=tk.LEFT)

        lbl_status_game = tk.Label(header_inner, text="● SERVER ONLINE", font=("Segoe UI", 9, "bold"), 
                                   bg=self.bg_panel, fg="#2ea043")
        lbl_status_game.pack(side=tk.RIGHT, pady=5)

        # Konten Utama (2 Kolom: Kiri = Daftar Listbox Game, Kanan = Dashboard Stats Karakter)
        content_frame = tk.Frame(self.root, bg=self.bg_main)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # --- KOLOM KIRI (Listbox Interaktif) ---
        left_outer, left_inner = KomponenUI.buat_panel_game(content_frame, self.bg_panel, self.border_color)
        left_outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        lbl_list_title = tk.Label(left_inner, text="📦 DAFTAR KOLEKSI ITEM", font=("Segoe UI", 11, "bold"), 
                                  bg=self.bg_panel, fg="#58a6ff")
        lbl_list_title.pack(anchor=tk.W, pady=(0, 8))

        # Listbox Bergaya Game (Konsol Terminal RPG)
        self.listbox = tk.Listbox(left_inner, font=("Consolas", 10), bg="#0d1117", fg="#c9d1d9",
                                  selectbackground="#1f6feb", selectforeground="#ffffff", 
                                  relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="#30363d")
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 12))
        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)

        # Tombol Aksi Bawah
        btn_action_frame = tk.Frame(left_inner, bg=self.bg_panel)
        btn_action_frame.pack(fill=tk.X)

        self.btn_tambah = KomponenUI.buat_tombol_game(
            btn_action_frame, "＋ Tambah Item", "#238636", "#2ea043", "#ffffff", self.buka_jendela_tambah
        )
        self.btn_tambah.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_refresh = KomponenUI.buat_tombol_game(
            btn_action_frame, "↻ Refresh", "#21262d", "#30363d", "#c9d1d9", self.muat_data_tabel
        )
        self.btn_refresh.pack(side=tk.LEFT, padx=8)

        self.btn_keluar = KomponenUI.buat_tombol_game(
            btn_action_frame, "✕ Keluar Game", "#da3633", "#f85149", "#ffffff", self.root.quit
        )
        self.btn_keluar.pack(side=tk.RIGHT)

        # --- KOLOM KANAN (Dashboard Stats & Info Item) ---
        right_outer, right_inner = KomponenUI.buat_panel_game(content_frame, self.bg_panel, self.border_color)
        right_outer.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0), ipadx=20)

        lbl_panel_title = tk.Label(right_inner, text="📊 STATISTIK ITEM", font=("Segoe UI", 11, "bold"), 
                                   bg=self.bg_panel, fg="#f0883e")
        lbl_panel_title.pack(pady=(0, 10))

        self.lbl_info = tk.Label(right_inner, text="[ Klik item di sebelah kiri\nuntuk melihat detail stats ]", 
                                 font=("Segoe UI", 10), bg=self.bg_panel, fg="#8b949e", justify=tk.LEFT)
        self.lbl_info.pack(fill=tk.X, pady=15, anchor=tk.W)

        self.lbl_power = tk.Label(right_inner, text="⚡ Power Rating: 0 PTS", font=("Segoe UI", 11, "bold"), 
                                  bg=self.bg_panel, fg="#58a6ff")
        self.lbl_power.pack(anchor=tk.W, pady=10)

    def muat_data_tabel(self):
        self.listbox.delete(0, tk.END)
        self.daftar_item_obj = []
        
        if not os.path.exists("item.csv"):
            return

        with open("item.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row and len(row) >= 4:
                    item = ItemGame(row[0], row[1], row[2], row[3])
                    self.daftar_item_obj.append(item)
                    teks_item = f"► {item.nama_item:<15} | [{item.tipe}]"
                    self.listbox.insert(tk.END, teks_item)

    def on_item_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        item = self.daftar_item_obj[index]
        power_rating = (item.hp * 2) + (item.damage * 5)

        info_text = (f"🏷️ Nama Item : {item.nama_item}\n\n"
                     f"🛡️ Tipe      : {item.tipe.upper()}\n\n"
                     f"❤️ Stats HP  : +{item.hp}\n\n"
                     f"⚔️ Damage    : {item.damage} AP")
        self.lbl_info.config(text=info_text, fg="#c9d1d9")
        self.lbl_power.config(text=f"⚡ Power Rating: {power_rating:,} PTS")

    def buka_jendela_tambah(self):
        tambah_win = tk.Toplevel(self.root)
        tambah_win.title("Tambah Item Game")
        tambah_win.geometry("380x420")
        tambah_win.configure(bg=self.bg_main)
        tambah_win.grab_set()

        tk.Label(tambah_win, text="✨ TAMBAH ITEM BARU", font=("Segoe UI", 12, "bold"), 
                 bg=self.bg_main, fg="#2ea043").pack(pady=15)

        form_frame = tk.Frame(tambah_win, bg=self.bg_main)
        form_frame.pack(fill=tk.BOTH, padx=25, pady=5)

        def buat_input(label_text):
            tk.Label(form_frame, text=label_text, bg=self.bg_main, fg="#8b949e", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(4, 2))
            entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#161b22", fg="white", insertbackground="white", relief=tk.FLAT)
            entry.pack(fill=tk.X, ipady=4, pady=(0, 6))
            return entry

        entry_nama = buat_input("Nama Item:")
        entry_tipe = buat_input("Tipe (Weapon/Armor/Consumable):")
        entry_hp   = buat_input("Stats HP:")
        entry_dmg  = buat_input("Damage:")

        def simpan_aksi():
            nama = entry_nama.get().strip()
            tipe = entry_tipe.get().strip()
            hp = entry_hp.get().strip()
            dmg = entry_dmg.get().strip()

            if not nama or not tipe or not hp or not dmg:
                messagebox.showerror("Error", "Semua kolom wajib diisi!", parent=tambah_win)
                return

            try:
                item_baru = ItemGame(nama, tipe, int(hp), int(dmg))
            except ValueError:
                messagebox.showerror("Error", "HP dan Damage harus berupa angka!", parent=tambah_win)
                return

            file_exists = os.path.exists("item.csv")
            with open("item.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["NamaItem", "Tipe", "HP", "Damage"])
                writer.writerow(item_baru.to_list())

            messagebox.showinfo("Sukses", "Item berhasil ditambahkan ke inventaris!", parent=tambah_win)
            tambah_win.destroy()
            self.muat_data_tabel()

        btn_simpan = KomponenUI.buat_tombol_game(tambah_win, "💾 Simpan Item", "#238636", "#2ea043", "#ffffff", simpan_aksi)
        btn_simpan.pack(fill=tk.X, padx=25, pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameInventoryPro(root)
    root.mainloop()