import csv
import os
from models import ItemGame

def muat_data():
    daftar_item = []
    if not os.path.exists("item.csv"):
        print("File item.csv tidak ditemukan.")
        return daftar_item
    with open("item.csv", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Lewati header
        for row in reader:
            if row:
                item = ItemGame(
                    nama_item=row[0],
                    tipe=row[1],
                    hp=row[2],
                    damage=row[3]
                )
                daftar_item.append(item)
    return daftar_item

def tampilkan_item():
    daftar_item = muat_data()
    if not daftar_item:
        print("Tidak ada data item.")
        return
    print("\n=== DAFTAR ITEM GAME ===\n")
    print(f"{'Nama Item':20}{'Tipe':15}{'HP':10}{'Damage'}")
    print("-" * 55)
    for item in daftar_item:
        print(
            f"{item.nama_item:20}"
            f"{item.tipe:15}"
            f"{str(item.hp):10}"
            f"{str(item.damage)}"
        )
    print("-" * 55)
    print(f"Total Item: {len(daftar_item)}")

def main():
    while True:
        print("\n=== MENU ===")
        print("1. Tampilkan Item")
        print("2. Refresh Data")
        print("0. Keluar")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            tampilkan_item()
        elif pilihan == "2":
            print("Data dimuat ulang...")
            tampilkan_item()
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
