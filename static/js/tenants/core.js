import $ from "jquery";


$(async function() {
    const [] = await Promise.all([
        import("./swiperjs"),
    ])
});