import DataTable from 'datatables.net-dt';
import 'datatables.net-responsive-dt';
import "datatables.net-dt/css/dataTables.datatables.min.css";
import "datatables.net-responsive-dt/css/responsive.dataTables.min.css";
import $ from "jquery";

$(function(){
    const table = new DataTable('#event-requests', {
    responsive: true
});
console.log("table")
})