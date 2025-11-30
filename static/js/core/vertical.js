"use strict";
import $ from "jquery"

$(function () {
    try {
        const $verticalNav = $(".vertical_nav");
        const $wrapper = $(".wrapper");
        const $menu = $("#js-menu");
        const $submenuItems = $menu.find(".menu--item__has_sub_menu");

        $(".toggle_menu").on("click", function () {
            $verticalNav.toggleClass("vertical_nav__opened");
            $wrapper.toggleClass("toggle-content");
        });
        $(".collapse_menu").on("click", function () {
            $verticalNav.toggleClass("vertical_nav__minify");
            $wrapper.toggleClass("wrapper__minify");
            $submenuItems.removeClass("menu--subitens__opened");
        });

        $submenuItems.each(function () {
            const $item = $(this);

            $item.find(".menu--link").on("click", function (e) {
                e.preventDefault();
                $submenuItems.not($item).removeClass("menu--subitens__opened");
                $item.toggleClass("menu--subitens__opened");
            });
        });

    } catch (error) {
        console.error(error);
    }
});
