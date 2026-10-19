class ItemGame:
    def __init__(self, nama_item, tipe, hp, damage, gambar=""):
        self.nama_item = nama_item
        self.tipe = tipe
        self.hp = int(hp)
        self.damage = int(damage)
        self.gambar = gambar  # Path file gambar (opsional)
    
    def to_list(self):
        return [self.nama_item, self.tipe, self.hp, self.damage, self.gambar]
    
    def __str__(self):
        return f"{self.nama_item} ({self.tipe}) - HP: {self.hp}, Damage: {self.damage}"