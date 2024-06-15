async function getMrt() {
  fetch("/api/mrts")
    .then((res) => res.json())
    .then((data) => {
      for (let i = 0; i < data["data"].length; i++) {
        let address = data["data"][i];
        if (address) {
          showMrt(address);
        }
      }
    })
    .catch((err) => console.error(err.message));
}
getMrt();
