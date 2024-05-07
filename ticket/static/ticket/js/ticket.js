$(document).ready(function () {
  $("#ticket-upload").on("change", function () {
    let file = this.files[0];
    let formData = new FormData();
    $("#file-name").text("File name: " + file.name);
    formData.append("file", file);

    // Replace 'YOUR_URL' with the URL you want to hit after uploading the file
    $.ajax({
      url: "/parse_pdf/",
      type: "POST",
      data: formData,
      processData: false, // tell jQuery not to process the data
      contentType: false, // tell jQuery not to set contentType
      success: function (data) {
        $("#pnr").val(data.pnr);
        $("#sector").val(data.sector);
        $("#passenger").val(data.passenger);
        $("#airline").val(data.airline);
        $("#travel_date").val(data.travel_date);
        $("#return_date").val(data.return_date);
        $("#supplier_id").val(3).trigger("change");
        $("#customer_id").select2("open");
      },
    });
  });
});
