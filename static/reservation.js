$(function init() {
    $("button.rep").click(function() {
        $.ajax({
            type: "PUT",
            url: $SCRIPT_ROOT + "/reservations/" + $(this).attr("id"),
            dataType: "text",
            success: function(msg) {
                alert(msg);
            }
        });
    });
    $("button.del").click(function() {
        $.ajax({
            type: "DELETE",
            url: $SCRIPT_ROOT + "/reservations/" + $(this).attr("id"),
            dataType: "json",
            success: function(msg) {
                //var id = JSON.parse(msg);
                $("table.car_table tr#" + msg.result.reservation_id).empty();
            }
        });
    });
});
