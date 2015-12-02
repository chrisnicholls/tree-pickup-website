$(document).ready(function() {

    $.get("/api/pickupDates", function(data) {
        var select = $("#dateInput")
        $.each(data.dates, function(i, item) {
           select.append('<option>' + item + '</option>')
        });
    });

    $("#neighborhoodSelect").on("change", function(event) {
        if($(this).val() == "Other") {
            $("#neighborhoodOther").show();
        } else {
            $("#neighborhoodOther").hide();
        }
    });

    $("#pickupForm").on("submit", function(event) {
        event.preventDefault();

        $.ajax({
            url: "/api/pickup",
            data: $(this).serialize(),
            type: "POST",
            success: function(data) {
                console.log("success!");
            },
            error: function(data) {
                console.log("error!");
            }
        });

    });

});