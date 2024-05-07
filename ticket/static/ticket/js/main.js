$(document).ready(function () {
  $("#currency, #sale, #purchase , #riyal_price").on("input", function () {
    this.value = this.value.replace(/[^0-9.,%+-]/g, "");
  });
  $("#airline").on("blur", function () {
    // Shift focus to the 'supplier_id' field and open the dropdown
    $("#supplier_id").select2("open");
  });
  $("#supplier_id").on("select2:select", function (e) {
    $("#customer_id").select2("open");
  });

  $("#currency, #sale, #purchase").keydown(function (e) {
    if (e.which == 13) {
      // Enter key pressed
      e.preventDefault(); // Prevent form submission
      var input = $(this).val();
      var sum = eval(input);
      $(this).val(sum);
    }
  });

  $("#pnr").keypress(function (e) {
    if (e.which == 13) {
      // Detect the Enter key
      e.preventDefault();
      var pnr = $(this).val();
      $.ajax({
        url: "/get_ticket/",
        data: {
          pnr: pnr,
        },
        dataType: "json",
        success: function (data) {
          if (data.travel_date) {
            console.log(data.travel_date);
            var travel_date = new Date(data.travel_date);
            var formatted_date = travel_date.toISOString().split("T")[0];
            $("#travel_date").val(formatted_date);
          }
          $("#ticket_type").val(data.ticket_type);
          $("#sector").val(data.sector);
          $("#passenger").val(data.passenger);
          $("#airline").val(data.airline);
          $("#supplier_id").val(data.supplier).trigger("change");
          $("#customer_id").val(data.customer).trigger("change");
          $("#sale").val(data.sale);
          $("#purchase").val(data.purchase);
          $("#narration").val(data.narration);
          $("#excel_id").val(data.excel_id);
        },
      });
    }
  });

  $("#ticket-form").on("submit", function (e) {
    // theme
    $(this).prop("disabled", true);
    $("#loading-gif").css("display", "flex");

    var form = $(this);
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "/tickets/create/",
      data: form.serialize(),
      success: function (data) {
        if (data.status == 200) {
          $("#info-message")
            .html(data.message)
            .show()
            .delay(5000)
            .fadeOut("slow");
          window.location.href = "/tickets/";
        }
        $("#info-message").html(data.message);
        $("#ticket-form")[0].reset();
        $("#supplier_id").val(null).trigger("change");
        $("#customer_id").val(null).trigger("change");
      },
      error: function (e) {
        $("#info-message")
          .html("Error: " + e.status + " " + e.responseText)
          .show()
          .delay(5000)
          .fadeOut("slow");
      },
      complete: function () {
        $("#ticket-submit").prop("disabled", false);
        $("#loading-gif").css("display", "none");
      },
    });
  });

  $(
    "#ticket-del, #cus-sup-del, #ledger-del, #visa-del, #hotel-del, #roomrate-del, #voucher-del"
  ).click(function (e) {
    e.preventDefault();
    let result = confirm("Are you sure you want to delete this?");
    if (result) {
      let ticketId = $(this).data("tid");
      ticketId = ticketId.toString().replace(/,/g, "");
      let modelName = $(this).data("model");
      $.ajax({
        url: "/delete/" + modelName + "/" + ticketId + "/delete/",
        type: "POST",
        data: {
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          if (data.status == "success") {
            $("#info-message")
              .html(data.message)
              .show()
              .delay(5000)
              .fadeOut("slow");
          }
          location.reload(false);
        },
        error: function (e) {
          $("#info-message")
            .html("Error: " + e.status + " " + e.responseText)
            .show()
            .delay(5000)
            .fadeOut("slow");
        },
      });
    }
  });

  $("#close-alert").click(function () {
    $(this).closest(".info-alert").hide();
  });

  $('input[type="datetime-local"],input[type="date"]').click(function () {
    this.showPicker();
  });

  $("#file-upload").on("change", function () {
    let file = this.files[0];
    let formData = new FormData();
    $("#file-name").text("File name: " + file.name);
    formData.append("file", file);

    // Replace 'YOUR_URL' with the URL you want to hit after uploading the file
    $.ajax({
      url: "/parse_file/",
      type: "POST",
      data: formData,
      processData: false, // tell jQuery not to process the data
      contentType: false, // tell jQuery not to set contentType
      success: function (data) {
        console.log(data.original);
        $("#currency").val(data.price); // Set the value of the currency input field
        $("#payment_date").val(data.date); // Set the value of the date input field
        $("#description").val(data.text); // Set the value of the description input field
      },
      error: function (e) {
        var response = JSON.parse(e.responseText);
        console.error(
          "An error occurred while uploading the file: ",
          response.message
        );
        console.error("Data  ", response.original);
      },
    });
  });
});
