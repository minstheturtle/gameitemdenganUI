import csv
import os
from models import ItemGame

def simpan_item():
    print("\n=== TAMBAH DATA ITEM GAME ===")
    nama_item = input("Nama Item : ").strip()
    tipe      = input("Tipe (Weapon/Armor/Consumable): ").strip()
    hp        = input("Stats HP  : ").strip()
    damage    = input("Damage    : ").strip()
    
    if not nama_item or not tipe or not hp or not damage:
        print("\n[PERINGATAN] Semua kolom harus diisi!\n")
        return
        
    try:
        item = ItemGame(nama_item, tipe, int(hp), int(damage))
    except ValueError:
        print("\n[PERINGATAN] HP dan Damage harus berupa angka!\n")
        return
        
    file_exists = os.path.exists("item.csv")
    with open("item.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["NamaItem", "Tipe", "HP", "Damage"])
        writer.writerow(item.to_list())
        
    print("\n[BERHASIL] Item game berhasil ditambahkan.\n")

def main():
    while True:
        print("=== MENU TAMBAH ITEM GAME ===")
        print("1. Tambah Item")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            simpan_item()
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.\n")

if __name__ == "__main__":
    main()
