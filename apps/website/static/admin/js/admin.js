$(function () {
    $('#id_city,#id_owner').select2();
    assignSelect($('.djn-dynamic-form-menu-meal select').not(".djn-empty-form"))

    $('.djn-add-handler').on('click', function (e) {
        console.log("asd");
        assignSelect($('.djn-dynamic-form-menu-meal').find('select'));
    })

});
var assignSelect = function (selector) {

    $(selector).select2({
        ajax: {
            url: "/list_tags/",
            dataType: 'json',
            delay: 0,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page
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
    })
};