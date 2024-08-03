const apiKey = "AIzaSyBj3dEMVfxewVQ7jbull1Hb_fKOM-BmFr8";
function getCoordinates() {
  const awbNumber = document.getElementById("awbNumber").value.trim();
  const resultRows = document.getElementById("resultRows");
  resultRows.innerHTML = ""; // Bersihkan hasil sebelumnya

  if (awbNumber) {
    document.getElementById("loading").style.display = "block";

    // Ganti URL berikut dengan endpoint Prod atau staging ya
    const apiUrl = `https://adminpanel-test.rideblitz.id/api/get_address?awb_number=${awbNumber}`;

    fetch(apiUrl)
      .then((response) => {
        console.log("Respon diterima:", response);
        return response.json();
      })
      .then((data) => {
        console.log("Data diterima:", data);
        if (data.status === "success") {
          const address = data.dropoff_address;
          const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(
            address
          )}&key=${apiKey}`;

          fetch(url)
            .then((response) => response.json())
            .then((geoData) => {
              if (geoData.status === "OK") {
                const location = geoData.results[0].geometry.location;
                resultRows.innerHTML += `
                                    <div class="row">
                                        <div class="column">${address}</div>
                                        <div class="column">Latitude: ${location.lat}, Longitude: ${location.lng}</div>
                                    </div>`;
              } else {
                resultRows.innerHTML += `
                                    <div class="row">
                                        <div class="column">${address}</div>
                                        <div class="column">Geocoding gagal: ${geoData.status}</div>
                                    </div>`;
              }
            })
            .catch((error) => {
              console.error("Error:", error);
              resultRows.innerHTML += `
                                <div class="row">
                                    <div class="column">${address}</div>
                                    <div class="column">Terjadi kesalahan saat mengambil koordinat.</div>
                                </div>`;
            })
            .finally(() => {
              document.getElementById("loading").style.display = "none";
            });
        } else {
          resultRows.innerHTML += `
                        <div class="row">
                            <div class="column">AWB Number: ${awbNumber}</div>
                            <div class="column">Gagal mendapatkan alamat: ${data.message}</div>
                        </div>`;
          document.getElementById("loading").style.display = "none";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        resultRows.innerHTML += `
                    <div class="row">
                        <div class="column">AWB Number: ${awbNumber}</div>
                        <div class="column">Terjadi kesalahan saat mengambil alamat.</div>
                    </div>`;
        document.getElementById("loading").style.display = "none";
      });
  }
}
