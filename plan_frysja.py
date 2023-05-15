import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from selenium import webdriver
import time
import re
from urllib.parse import unquote
import traceback

def sanitize_filename(filename):
    # Fjern ugyldige tegn fra filnavnet
    valid_characters = r'[\\:/|]'
    sanitized_filename = re.sub(valid_characters, '', filename)
    return sanitized_filename

def remove_spaces(filename):
    return filename.replace(" ", "_")

def download_files(driver, directory):
    # Hent HTML-kilden til siden
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Finn alle lenker på siden og last ned filene
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href and not href.startswith("javascript:"):
            url = urllib.parse.urljoin(driver.current_url, href)
            response = requests.get(url, stream=True)
            if response.ok:
                filename = sanitize_filename(link.text)
                filename_without_spaces = remove_spaces(filename).strip()
                print(filename_without_spaces)
                filepath = os.path.join(directory, filename_without_spaces)

                with open(filepath, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print("Lastet ned:", filename_without_spaces)
def main():
    base_url = "https://innsyn.pbe.oslo.kommune.no"
    page_url = "https://innsyn.pbe.oslo.kommune.no/saksinnsyn/casedet.asp?caseno=202111625&wfl=T&Dateparam=05/09/2023&sti="
    directory = r'nedlastede_filer' # Legg til r-prefiks for å behandle strengen som en rå streng

    # Sjekk om directory er en eksisterende mappe
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Opprett en WebDriver for valgt nettleser (f.eks. Chrome)
    driver = webdriver.Chrome()

    try:
        # Naviger til siden som inneholder filene
        driver.get(page_url)

        # Logg inn i nettleseren manuelt med BankID

        # Vent noen sekunder for å sikre at innloggingen er fullført
        time.sleep(1)
        # Last ned filene
        download_files(driver, directory)

    except:
        traceback.print_exc()

    finally:
        # Lukk nettleseren
        driver.quit()

if __name__ == "__main__":
    main()
