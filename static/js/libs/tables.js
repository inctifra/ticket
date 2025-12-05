import $ from "jquery";
import DataTable from 'datatables.net-dt';
import 'datatables.net-responsive-dt';

/**
 * Initialize a DataTable with dynamic config.
 *
 * @param {string} selector - CSS selector for the table.
 * @param {object} options - Custom DataTable configuration.
 * @returns {object} DataTable instance
 */
export function initDynamicDataTable(selector, options = {}) {
    if(!$(selector).get(0))return;
 return new DataTable(selector, {
        responsive: true,
        colReorder: true,
        paging: true,
        pageLength: 5,
        ...options,
    });
}
