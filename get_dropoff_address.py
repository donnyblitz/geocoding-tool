import logging
logging.basicConfig(level=logging.DEBUG)

def get_dropoff_address(awb_number):
    logging.debug('Memulai fungsi get_dropoff_address')
    # Set the path for chromedriver
    chromedriver_path = 'C:\\webdrivers\\chromedriver.exe'
    logging.debug('Path untuk chromedriver diatur')

    # Setup WebDriver with the Service object
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    logging.debug('WebDriver diinisialisasi')

    # Buka halaman login dashboard
    driver.get('https://adminpanel-test.rideblitz.id/')
    logging.debug('Halaman login dashboard dibuka')

    # Login ke dashboard
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username.send_keys('blitz_admin')
    password.send_keys('Delhi#123')
    login_button.click()
    logging.debug('Login berhasil')

    # Tunggu hingga login selesai dan dashboard terbuka
    wait = WebDriverWait(driver, 10)
    # Klik navbar "Order List" terlebih dahulu
    order_list_nav = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Order List')))
    order_list_nav.click()
    logging.debug('Klik Order List')

    # Tunggu hingga halaman "Order List" terbuka dan elemen pencarian muncul
    search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchbar')))  # Menggunakan ID 'searchbar'
    logging.debug('Elemen pencarian ditemukan')

    # Cari order tertentu berdasarkan AWB number
    search_box.send_keys(awb_number)
    search_box.send_keys(Keys.RETURN)
    logging.debug('Mencari AWB number')

    # Tunggu hasil pencarian muncul
    awb_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, awb_number)))

    # Klik AWB number yang ditemukan untuk membuka halaman detail
    awb_link.click()
    logging.debug('AWB number ditemukan dan diklik')

    # Tunggu halaman detail order terbuka dan elemen dropoff address muncul
    wait.until(EC.presence_of_element_located((By.ID, 'id_dropoff_address')))
    logging.debug('Halaman detail order terbuka')

    # Cari elemen alamat dropoff
    dropoff_address = driver.find_element(By.ID, 'id_dropoff_address').get_attribute('value')
    logging.debug(f'Alamat dropoff ditemukan: {dropoff_address}')

    # Tutup WebDriver
    driver.quit()

    return dropoff_address
