var rowTemplate = Handlebars.compile(" \
    <tr> \
        <td>{{ id }}</td> \
        <td> <a href='/admin/season/{{ internalId }}'>{{ season_name }} {{ year }}</a></td> \
        <td> \
            <button data-season-id='{{ internalId }}' class='btn btn-primary btn-sm'> \
                <i class='material-icons'>edit</i> \
                Edit \
            </button> \
            <button data-season-id='{{ internalId }}' class='btn btn-danger btn-sm'> \
                <i class='material-icons'>delete</i> \
                Delete \
            </button> \
        </td> \
    </tr> \
");

var ajaxErrorCallback=function(){
    $("#add-season").html(i18n.button_caption);
    $("#add-season").prop("disabled", false);
};

$("select").dropdown({ "autoinit" : ".select" });

$("#add-season").on("click", function(){
    $("#add-season").html(i18n.button_adding);
    $("#add-season").prop("disabled", true);
    data = {
        season_name: $("select").val(),
        year: $("#season-year").val()
    };
    $.post("/admin/ajax/add_season", data, function(recv){
        if (recv.result == "success"){
            notifySuccess(i18n.add_success)
            rowID++;
            data.id=rowID;
            data.internalId=recv.internalId;
            $("tr:last").before(rowTemplate(data))
        } else {
            notifyFailure(i18n.add_fail+recv.result.toString())
        }
        $("#add-season").html(i18n.button_caption);
        $("#add-season").prop("disabled", false);
    })
})