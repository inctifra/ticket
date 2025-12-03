import $ from "jquery";


$(async function () {
    const [{default:Choices}] = await Promise.all([
        import("choices.js"),
        import("./auth"),
        import("../../sass/tenants/project.scss"),
        import("bootstrap/dist/css/bootstrap.min.css"),
        import("bootstrap"),
        import("bootstrap-icons/font/bootstrap-icons.css"),
        import("@fortawesome/fontawesome-free/css/all.min.css"),
        import("./events"),
        import("./core"),
        import("choices.js/src/styles/choices"),
        import("./payments/scripts"),
    ]);

    new Choices('.selectpicker', {
        searchEnabled: true,
        itemSelectText: '',
    });
});
