import os
import logging
import json
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__, template_folder='templates')

# Set environment variable for Flask
os.environ['FLASK_ENV'] = 'development'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_dropoff_address(awb_number):
    logging.debug(f"Processing AWB number: {awb_number}")
    # Set the path for chromedriver
    chromedriver_path = 'C:\\webdrivers\\chromedriver.exe'

    # Setup WebDriver with the Service object
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Buka halaman login dashboard
        driver.get('https://adminpanel-test.rideblitz.id/')
        logging.debug("Opened login page")

        # Login ke dashboard
        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username.send_keys('blitz_admin')
        password.send_keys('Delhi#123')
        login_button.click()
        logging.debug("Logged in to dashboard")

        # Tunggu hingga login selesai dan dashboard terbuka
        wait = WebDriverWait(driver, 10)
        # Klik navbar "Order List" terlebih dahulu
        order_list_nav = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Order List')))
        order_list_nav.click()
        logging.debug("Clicked on Order List")

        # Tunggu hingga halaman "Order List" terbuka dan elemen pencarian muncul
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchbar')))
        logging.debug("Found search box")

        # Cari order tertentu berdasarkan AWB number
        search_box.send_keys(awb_number)
        search_box.send_keys(Keys.RETURN)
        logging.debug("Searched for AWB number")

        # Tunggu hasil pencarian muncul
        awb_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, awb_number)))
        awb_link.click()
        logging.debug("Clicked on AWB number")

        # Tunggu halaman detail order terbuka dan elemen dropoff address muncul
        wait.until(EC.presence_of_element_located((By.ID, 'id_dropoff_address')))
        logging.debug("Found dropoff address element")

        # Cari elemen alamat dropoff
        dropoff_address = driver.find_element(By.ID, 'id_dropoff_address').get_attribute('value')
        logging.debug(f"Found dropoff address: {dropoff_address}")
    finally:
        driver.quit()
        logging.debug("Closed WebDriver")

    return dropoff_address

def update_dropoff_coordinates(updates):
    logging.debug("Updating coordinates for multiple AWB numbers")
    # Set the path for chromedriver
    chromedriver_path = 'C:\\webdrivers\\chromedriver.exe'

    # Setup WebDriver with the Service object
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Buka halaman login dashboard
        driver.get('https://adminpanel-test.rideblitz.id/')
        logging.debug("Opened login page")

        # Login ke dashboard
        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username.send_keys('blitz_admin')
        password.send_keys('Delhi#123')
        login_button.click()
        logging.debug("Logged in to dashboard")

        # Tunggu hingga login selesai dan dashboard terbuka
        wait = WebDriverWait(driver, 10)
        # Klik navbar "Order List" terlebih dahulu
        order_list_nav = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Order List')))
        order_list_nav.click()
        logging.debug("Clicked on Order List")

        for update in updates:
            awb_number = update['awb_number']
            lat = update['lat']
            lng = update['lng']
            logging.debug(f"Updating AWB number: {awb_number} with lat: {lat} and lng: {lng}")

            # Retry mechanism
            for attempt in range(3):
                try:
                    # Tunggu hingga halaman "Order List" terbuka dan elemen pencarian muncul
                    search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchbar')))
                    search_box.clear()
                    search_box.send_keys(awb_number)
                    search_box.send_keys(Keys.RETURN)
                    logging.debug(f"Searched for AWB number {awb_number}")

                    # Tunggu hasil pencarian muncul
                    awb_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, awb_number)))
                    awb_link.click()
                    logging.debug(f"Clicked on AWB number {awb_number}")

                    # Tunggu halaman detail order terbuka dan elemen dropoff lat dan long muncul
                    wait.until(EC.presence_of_element_located((By.NAME, 'dropoff_lat')))
                    logging.debug("Found dropoff latitude element")

                    # Cari elemen latitude dan longitude dropoff
                    dropoff_lat = driver.find_element(By.NAME, 'dropoff_lat')
                    dropoff_long = driver.find_element(By.NAME, 'dropoff_long')

                    # Membatasi desimal hingga 9 tempat
                    lat = f"{float(lat):.9f}"
                    lng = f"{float(lng):.9f}"

                    dropoff_lat.clear()
                    dropoff_lat.send_keys(lat)
                    dropoff_long.clear()
                    dropoff_long.send_keys(lng)
                    logging.debug(f"Updated dropoff latitude: {lat} and longitude: {lng}")

                    # Simpan perubahan
                    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="save_btn"]')))
                    save_button.click()
                    logging.debug(f"Clicked Save button for AWB number {awb_number}")

                    # Tunggu konfirmasi penyimpanan selesai
                    success_message = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "The order has been successfully updated.")]')))
                    logging.debug(f"Order {awb_number} updated successfully")
                    break  # Berhasil, keluar dari loop retry
                except Exception as e:
                    logging.error(f"Attempt {attempt + 1} failed for AWB number {awb_number}: {str(e)}")
                    if attempt == 2:
                        logging.error(f"Failed to update AWB number {awb_number} after 3 attempts")
                    continue
    finally:
        driver.quit()
        logging.debug("Closed WebDriver")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_dropoff_addresses', methods=['POST'])
def get_dropoff_addresses():
    awb_numbers = request.json['awb_numbers']
    results = []
    for awb_number in awb_numbers:
        dropoff_address = get_dropoff_address(awb_number)
        results.append({'awb_number': awb_number, 'dropoff_address': dropoff_address})
    return jsonify({'results': results})

@app.route('/update_admin_panel', methods=['POST'])
def update_admin_panel():
    data = request.json['updates']
    update_dropoff_coordinates(data)
    return jsonify({'message': 'Coordinates updated successfully in the admin panel.'})

if __name__ == "__main__":
    app.run(debug=True)
