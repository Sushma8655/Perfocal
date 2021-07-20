var URL = document.getElementById("header");
console.log(URL)
$(function() {
        var start = moment().subtract(29, 'days');
        var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('DD/MM/YYYY h:mm A') + ' - ' + end.format('DD/MM/YYYY h:mm A'));
    }

    $('#reportrange').daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        startDate: start,
        endDate: end,
        endTime: end,

        ranges: {
           'Today': [moment().startOf('day'), moment()],
           'Yesterday': [moment().subtract(1, 'days').startOf('day'), moment().subtract(1, 'days').endOf('day')],
           'Last 7 Days': [moment().subtract(6, 'days').startOf('day'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days').startOf('day'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);



   $('#reportrange').on('apply.daterangepicker', function(ev, picker) {
        console.log(picker.startDate.format('DD/MM/YYYY h:mm A'));
        console.log(picker.endDate.format('DD/MM/YYYY h:mm A'));
        document.getElementById("fromdate").value = picker.startDate.format('YYYY-MM-DDThh:mm:ssZ')
        document.getElementById("todate").value = picker.endDate.format('YYYY-MM-DDThh:mm:ssZ')
        sendtimeinfofunc();
        });


function sendtimeinfofunc() {
    let timerangeval = {
    'fromdateval' : document.getElementById("fromdate").value,
    'todateval': document.getElementById("todate").value,
    };
    var payload = JSON.stringify(timerangeval);
    console.log(payload)
    $.ajax({
      type: "POST",
      headers: {'X-CSRFToken': document.getElementById('csrf').value},
      url: readtimeseries,
      data : {'getdata': payload},
      success: "SUCCESS",
      dataType: 'json'
    });
    }
});


