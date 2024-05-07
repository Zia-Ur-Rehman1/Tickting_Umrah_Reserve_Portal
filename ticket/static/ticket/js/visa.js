$(document).ready(function () {
  function updatePKRValue(inputSelector, outputSelector) {
    $(inputSelector).on("input", function () {
      let value = $(this).val();
      let price = $("#riyal_rate").val();
      let pkrPrice = value * price;
      $(outputSelector).val(pkrPrice.toFixed(2)); // Update the PKR value field
    });
  }
  // Call the function for each input field
  updatePKRValue("#visa_sale", "#sale_pkr");
  updatePKRValue("#visa_purchase", "#purchase_pkr");

  function updateSARValue(inputSelector, outputSelector) {
    $(inputSelector).on("input", function () {
      let value = $(this).val();
      let price = $("#riyal_rate").val();
      let pkrPrice = value / price;
      $(outputSelector).val(pkrPrice.toFixed(2)); // Update the PKR value field
    });
  }
  updateSARValue("#purchase_pkr", "#visa_purchase");
  updateSARValue("#sale_pkr", "#visa_sale");

  $("#id_visa").select2({
    placeholder: "Select Passports",
    allowClear: true,
    theme: "classic",
  });

  $("#visa_type").change(function () {
    var visaType = $(this).val();
    // prettier-ignore
    var durationMapping = {
      "36": "36 Hours",
      "96": "96 Hours",
      "1m": "1 Month",
      "2m": "2 Months",
      "3m": "3 Months",
    };
    if (visaType === "UV") {
      durations = ["1m", "3m"];
    } else {
      durations = ["36", "96", "1m", "2m"];
    }

    var durationSelect = $("#duration");
    durationSelect.empty();

    $.each(durations, function (index, value) {
      durationSelect.append(
        $("<option></option>").attr("value", value).text(durationMapping[value])
      );
    });
  });
});
