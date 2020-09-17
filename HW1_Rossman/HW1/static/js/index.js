//direct button to functions
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed")
})

$('#day_dropdown a').click(function () {
    $('#day_select').html($(this).text())
})

$('#open_dropdown a').click(function () {
    $('#open_select').html($(this).text())
})