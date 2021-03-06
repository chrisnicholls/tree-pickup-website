$(document).ready(function() {

    if(!document.location.search.match(/sourceKey=callcenter/i)) {
        $("#welcomeModal").modal('show');
    }

    var source = "Web";

    if(document.location.search.match(/sourceKey=callcenter/i)) {
        source = "Call Center";
    }

    if(document.location.search.match(/sourceKey=fb/i)) {
        source = "Facebook";
    }

    $("#sourceInput").val(source);

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
                $("#theDate").val($("#pickupDate").val()).change();
                $("#successModal").modal('show');
                $("#submitButton").prop('disabled', true);
            },
            error: function(data) {
                $("#errorModal").modal('show');
            }
        });

    });

});