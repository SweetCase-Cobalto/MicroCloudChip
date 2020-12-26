$(() => {
    $('.modify-btn').click((e) => {
        const id = e.target.id;
        const targetFormId = "modify-" + id;
        document.getElementById(targetFormId).submit();
    });
    $('.delete-btn').click((e) => {
        console.log(e.target.id);
    });
});