import $ from "jquery";


$(async function() {
    const [] = await Promise.all([
        import("./auth"),
        import("../../sass/tenants/project.scss")
    ])
})