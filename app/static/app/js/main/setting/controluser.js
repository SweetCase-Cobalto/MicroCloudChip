$(() => {
    $('.modify-btn').click((e) => {
        const id = e.target.id;
        const targetFormId = "modify-" + id;
        document.getElementById(targetFormId).submit();
    });
    $('.delete-btn').click((e) => {
        const id = e.target.id;
        const targetFormId = "delete-" + id;
        var input = confirm("do you really delete this id?");
        if(input)
            document.getElementById(targetFormId).submit();
    });
});