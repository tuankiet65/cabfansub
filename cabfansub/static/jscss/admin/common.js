var ajaxErrorCallback=null;

$.material.init();

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

$(document).ajaxError(function(event, jqxhr, settings, thrownError){
    console.log(event, jqxhr, settings);
    notifyFailure("Network failure: "+thrownError.toString());
    if (ajaxErrorCallback)
        ajaxErrorCallback();
});

function notifySuccess(msg){
    $.notify({
        message: msg
    },{
        placement: {
            from: "bottom"
        },
        type: "success",
        showProgressbar: true,
        timer: 100
    });
}

function notifyFailure(msg){
    $.notify({
        message: msg
    },{
        placement: {
            from: "bottom"
        },
        type: "danger",
        showProgressbar: true,
        timer: 100
    });
}