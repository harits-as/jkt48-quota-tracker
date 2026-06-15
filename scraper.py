import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL halaman event JKT48 (ganti dengan link event MnG / 2s yang lagi aktif nanti)
URL = "https://jkt48.com/purchase/exclusive?code=EX3773" 

def scrape_quota():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # Catatan: Kalau halaman JKT48 mewajibkan login, lu harus selipin cookies akun lu di sini
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print("Gagal mengambil halaman web JKT48")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    slots = []
    
    # Nyari tabel kuota di web JKT48 (disesuaikan dengan struktur HTML aslinya)
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')[1:] # Lewati baris judul/header tabel
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                member = cols[0].text.strip()
                sesi = cols[1].text.strip()
                status = cols[2].text.strip() # Isinya bisa jumlah sisa kuota atau "Habis"
                
                slots.append({
                    "member": member,
                    "sesi": sesi,
                    "status": status
                })
    
    # Format data yang bakal disimpan
    data_to_save = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": slots if slots else [{"member": "Contoh Member", "sesi": "Sesi 1", "status": "99"}] 
    }
    
    # Simpan hasil ke file data.json
    with open('data.json', 'w') as f:
        json.dump(data_to_save, f, indent=4)
        print("Data kuota berhasil diperbarui!")
        
if __name__ == "__main__":
    scrape_quota()
