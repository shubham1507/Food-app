$(function () {
    $('.city-select').select2({
        ajax: {
            url: "/list_cities/",
            dataType: 'json',
            delay: 100,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page,
                    only_restaurants: $(this).data("only-restaurants")
                };
            },
            processResults: function (data, params) {

                params.page = params.page || 1;
                return {
                    results: $.map(data.items, function (obj) {
                        return {id: obj, text: obj};
                    }),
                    pagination: {
                        more: (params.page * 10) < data.total_count
                    }
                };
            },
            cache: true
        }
    });
    setTimeout(function () {
        $('.alert').fadeOut();
    }, 3000);

    var alert = function (status, message, id) {
        return '<div class="alert alert-' + status + '" data-id="' + id + '">' +
            '<div class="container-fluid">' +
            '<div class="alert-icon">' +
            '<i class="material-icons">check</i>' +
            '</div>' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
            '<span aria-hidden="true"><i class="material-icons">clear</i></span>' +
            '</button>' +
            '<strong>' + message + '</strong>' +
            '</div>' +
            '</div>'
    }

    socket = new WebSocket("ws://" + window.location.host + "/orders_channel/");
    socket.onmessage = function (e) {
        data = JSON.parse(e.data);
        if ($("#order-table")) {
            $('table p[data-id=' + data['id'] + ']').attr("data-content", data['status']);
            $('table p[data-id=' + data['id'] + ']').find("strong").text(data['status'].capitalize());
        }
        status = (data['status'] == "rejected") ? "danger" : "success";
        message = "Your order " + data["name"] + " is now " + data["status"];
        $('#notifications').append(alert(status, message, data['id']));
        setTimeout(function () {
            $('.alert[data-id="' + data['id'] + '"]').fadeOut();
        }, 3000);

    };
    if (socket.readyState == WebSocket.OPEN) socket.onopen();
    String.prototype.capitalize = function () {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }

});

