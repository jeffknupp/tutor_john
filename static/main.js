$( document ).ready(function() {
    $("form input[name='origin']").autocomplete({source: '/completions',
        minLength: 2});
    $("form input[name='destination']").autocomplete({source: '/completions', minLength: 2});
});


