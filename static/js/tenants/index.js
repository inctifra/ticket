import $ from "jquery";


$(async function() {
    const [] = await Promise.all([
        import("./auth"),
        import("../../sass/tenants/project.scss"),
        import("bootstrap-icons/font/bootstrap-icons.css"),
        import("./events"),
        import("./core")
    ])
});

