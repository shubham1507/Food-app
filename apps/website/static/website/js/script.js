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

});