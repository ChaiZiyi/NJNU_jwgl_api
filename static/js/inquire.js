$("input[name=idno]").on("input", function(evt) {
    if ($(this).val().trim().length) {
        $("#querybtn").removeAttr("disabled");
    } else {
        $("#querybtn").prop("disabled", "disabled");
    }
});


$("input[name=name]").on("input", function(evt) {
    if ($(this).val().trim().length) {
        $("#querybtn").removeAttr("disabled");
    } else {
        $("#querybtn").prop("disabled", "disabled");
    }
});

$("input[name=username]").on("input", function(evt) {
    if ($(this).val().trim().length) {
        $("#querybtn").removeAttr("disabled");
    } else {
        $("#querybtn").prop("disabled", "disabled");
    }
});

$("input[name=password]").on("input", function(evt) {
    if ($(this).val().trim().length) {
        $("#submitbtn").removeAttr("disabled");
    } else {
        $("#submitbtn").prop("disabled", "disabled");
    }
});

$("input[name=url]").on("input", function(evt) {
    if ($(this).val().trim().length) {
        $("#querybtn").removeAttr("disabled");
    } else {
        $("#querybtn").prop("disabled", "disabled");
    }
});

$(document).keydown(function(event) {
    //判断当event.keyCode 为37时（即左键），执行函数to_prev(); 
    //判断当event.keyCode 为39时（即右键），执行函数to_next(); 
    if (event.keyCode == 37) {
        to_prev();
    } else if (event.keyCode == 39) {
        to_next();
    }
});


function to_prev() {
    document.getElementById("prev").click();
}

function to_next() {
    document.getElementById("next").click();
}
