document.getElementById("fileInput").addEventListener("change", function() {

    const fileName = this.files[0].name;

    document.getElementById("fileName").textContent = "Selected file: " + fileName;

});