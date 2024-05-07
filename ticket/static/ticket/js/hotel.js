$(document).ready(function () {
  $("svg.fill-current.h-4.w-4").parent("div").remove();
  $("#hotel_id").select2({
    placeholder: "Select Hotel",
    allowClear: true,
    theme: "classic",
  });

  $("#id_riyal_price").on("input", function () {
    let riyalPrice = $(this).val();
    let price = $("#id_riyal_rate").val();
    let pkrPrice = riyalPrice * price;
    $("#id_pkr_price").val(pkrPrice.toFixed(2)); // Update the PKR value field
  });

  $("[id^='id_hotels-'][id$='-city']").change(function () {
    let selectedCity = $(this).val();
    let hotelSelect = $(this)
      .closest(".form-template")
      .find("[id^='id_hotels-'][id$='-hotel']");
    $.ajax({
      url: "/ajax/load-hotels/",
      data: {
        city: selectedCity,
      },
      success: function (data) {
        hotelSelect.empty();
        hotelSelect.append(
          $("<option>", {
            value: "",
            text: "----------",
          })
        );
        hotelSelect.append(
          $("<option>", {
            value: "-1",
            text: "Self Accommodation",
          })
        );
        $.each(data, function (index, hotel) {
          hotelSelect.append(
            $("<option>", {
              value: hotel.id,
              text: hotel.hotel_name,
            })
          );
        });
      },
    });
  });

  $("[id^='id_hotels-'][id$='-hotel']").change(function () {
    let selectedHotel = $(this).val();
    let hotelSelect = $(this)
      .closest(".form-template")
      .find("[id^='id_hotels-'][id$='-room']");
    let ROOM_CATEGORY = {
      0: "Private",
      1: "Sharing",
      2: "Quadripple",
      3: "Tripple",
      4: "Double",
    };

    $.ajax({
      // initialize an AJAX request
      url: "/ajax/load-rooms/", // set the url of the request (= /ajax/load-hotels/)
      data: {
        hotel: selectedHotel, // add the city id to the GET parameters
      },
      success: function (data) {
        hotelSelect.empty();
        hotelSelect.append(
          $("<option>", {
            value: "",
            text: "----------",
          })
        );

        $.each(data, function (index, room) {
          hotelSelect.append(
            $("<option>", {
              value: room.id,
              text: ROOM_CATEGORY[room.room_type],
            })
          );
        });
      },
    });
  });

  $("[id^='id_hotels-'][id$='-start_at']").change(function () {
    let form = $(this).closest(".form-template");
    // let startAt = form.find("[id^='id_hotels-'][id$='-start_at']").val();
    var startAt = $(this).val();

    if (startAt) {
      let startDate = new Date(startAt);
      // Add one day to the start date
      startDate.setDate(startDate.getDate() + 1);
      // Format the date in 'yyyy-mm-dd' format
      let minDate = startDate.toISOString().split("T")[0];
      // Set the min date of the end_at field
      // $("#id_end_at").attr("min", minDate);
      form.find("[id^='id_hotels-'][id$='-end_at']").attr("min", minDate);
    }
  });
  $("[id^='id_hotels-'][id$='-end_at']").change(function () {
    var endDate = $(this).val();
    if (endDate) {
      var nextFormStartAt = $(this)
        .closest(".form-template")
        .next()
        .find("[id^='id_hotels-'][id$='-start_at']");
      nextFormStartAt.attr("min", endDate);
    }
  });

  $(
    "[id^='id_hotels-'][id$='-start_at'] , [id^='id_hotels-'][id$='-end_at']"
  ).change(function () {
    let form = $(this).closest(".form-template");
    let startAt = form.find("[id^='id_hotels-'][id$='-start_at']").val();
    let endAt = form.find("[id^='id_hotels-'][id$='-end_at']").val();
    if (startAt && endAt) {
      let startDate = new Date(startAt);
      let endDate = new Date(endAt);
      let timeDiff = Math.abs(endDate.getTime() - startDate.getTime());
      let nights = Math.ceil(timeDiff / (1000 * 3600 * 24));
      form.find("[id^='id_hotels-'][id$='-nights']").val(nights);
    }
  });

  $("#submit_btn").click(function (event) {
    event.preventDefault(); // Prevent the form from being submitted
    $("#submit_btn").prop("disabled", true);

    // Serialize the form data
    let formData = $("form").serialize();
    let url; // Declare the url variable here
    let id = $("#v_id").val();
    if (id == "") {
      url = "/create_voucher/";
    } else {
      url = "/update_voucher/" + id;
    }
    // Send the POST request
    $.ajax({
      url: url,
      type: "POST",
      data: formData,
      success: function (response) {
        window.location.href = "/vouchers/";
        $("#info-message")
          .html(response.message)
          .show()
          .delay(5000)
          .fadeOut("slow");
        // For example, you might want to redirect to a new page
      },
      error: function (error) {
        // Handle any errors
        console.log(error);
        $("#submit_btn").prop("disabled", false);
      },
    });
  });
  // Last Closing Tag
});
