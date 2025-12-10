import os
import requests

# Папка с исходными .cif файлами
cif_folder = "data"
# Папка, куда сохранять .pdb файлы
output_folder = "pdb_api"

os.makedirs(output_folder, exist_ok=True)

# URL API RCSB для получения PDB файлов
BASE_URL = "https://files.rcsb.org/download/{}.pdb"

# Получаем все pdb-коды из файлов
cif_files = [f for f in os.listdir(cif_folder) if f.lower().endswith(".cif")]
pdb_codes = [os.path.splitext(f)[0].upper() for f in cif_files]

print(f"Найдено CIF-файлов: {len(pdb_codes)}")
print("Пример кодов:", pdb_codes[:5])

for code in pdb_codes:
    url = BASE_URL.format(code)
    out_path = os.path.join(output_folder, f"{code}.pdb")

    # Пропуск, если файл уже есть
    if os.path.exists(out_path):
        print(f"[SKIP] {code} уже скачан")
        continue

    print(f"[DOWNLOAD] {code} -> {out_path}")

    r = requests.get(url)

    if r.status_code == 200 and "ATOM" in r.text:
        with open(out_path, "w") as f:
            f.write(r.text)
    else:
        print(f"[ERROR] Не удалось скачать {code}, статус: {r.status_code}")
