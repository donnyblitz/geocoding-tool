import requests
from bs4 import BeautifulSoup

# URL dan kredensial login
login_url = 'https://adminpanel-test.rideblitz.id/login'
# Login ke dashboard
username = driver.find_element(By.NAME, 'username')
password = driver.find_element(By.NAME, 'password')
login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

username.send_keys('blitz_admin')
password.send_keys('Delhi#123')
login_button.click()

# Tunggu hingga login selesai dan dashboard terbuka
wait = WebDriverWait(driver, 10)
# Klik navbar "Order List" terlebih dahulu
order_list_nav = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Order List')))
order_list_nav.click()

# Tunggu hingga halaman "Order List" terbuka dan elemen pencarian muncul
search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchbar')))  # Menggunakan ID 'searchbar'

# Cari order tertentu berdasarkan AWB number
awb_number = 'BEM00000001048'
search_box.send_keys(awb_number)
search_box.send_keys(Keys.RETURN)

# Tunggu hasil pencarian muncul
awb_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, awb_number)))

# Klik AWB number yang ditemukan untuk membuka halaman detail
awb_link.click()

# Buat sesi
session = requests.Session()

# Data login
login_data = {
    'username': username,
    'password': password
}

# Fungsi untuk login
def login(session, login_url, login_data):
    response = session.post(login_url, data=login_data)
    if response.status_code == 200:
        print("Login berhasil")
    else:
        print("Login gagal")
        exit()

# Fungsi untuk mencari data berdasarkan AWB
def search_awb(session, search_url, awb):
    response = session.get(search_url, params={'awb': awb})
    if response.status_code == 200:
        return response.text
    else:
        print("Pencarian gagal")
        return None

# Fungsi untuk ekstrak alamat dropoff dari halaman hasil pencarian
def extract_dropoff_address(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Sesuaikan selektor berdasarkan struktur halaman
    address = soup.find('div', class_='dropoff-address').text.strip()
    return address

# Main program
if __name__ == "__main__":
    # Login
    login(session, login_url, login_data)

    # Input AWB dari pengguna
    awb = input("Masukkan AWB: ")

    # Cari data berdasarkan AWB
    result_html = search_awb(session, search_url, awb)

    if result_html:
        # Ekstrak alamat dropoff
        dropoff_address = extract_dropoff_address(result_html)
        print(f"Alamat Dropoff: {dropoff_address}")
