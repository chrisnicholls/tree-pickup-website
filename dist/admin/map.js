$(document).ready(function() {
    var map;
    var mc;
    var markers = {};

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 45.963585, lng: -66.643119},
        zoom: 12
    });


    $.get("/admin/mapData", function (mapData) {
        var date;
        for (date in mapData) {
            console.log(date);
            var locations = mapData[date];

            markers[date] = [];

            for (var i in locations) {
                if (locations[i].lat != null) {
                    var latLng = new google.maps.LatLng(locations[i].lat, locations[i].lng);
                    var marker = new google.maps.Marker({
                        position: latLng,
                        title: locations[i].address
                    });

                    markers[date].push(marker);
                }
            }

            //add to the select list
            $('#dateSelect').append($('<option>', {
                value: date,
                text: date
            })) ;
        }

        $('#dateSelect').val(date).change();

        mc = new MarkerClusterer(map, markers[date], {imagePath: '/assets/images/m'});
    });

    $('#dateSelect').change(function(e) {
        var date = $(e.target).val();
        console.log(date);

        if(mc != null) {
            console.log(markers);
            console.log(markers[date])
            mc.clearMarkers();
            mc.addMarkers(markers[date]);
        }
    });
});
