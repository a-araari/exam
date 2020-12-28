function printExam(printBtn, examDownloadURL) {
    $("#print-spinners").show();
    $("#print-text").hide();
    $.ajax({
        url: examDownloadURL,
        data: {
            'as_base64': true,
        },
        dataType: 'json',
        success: function (data) {
            if (data.base64_data) {
                printJS({printable: data.base64_data, type: 'pdf', base64: true})
                $("#print-spinners").hide();
                $("#print-text").show();
            }
        }
    });
}
