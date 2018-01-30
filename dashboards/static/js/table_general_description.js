
window.onload = AconditionTable;


function AconditionTable(){
	$('#location_table').DataTable({
		scrollY: 400,
		select: true,
		dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
	});
	$('#general_information').DataTable({
		scrollY: 400,
		select: true,
		dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
	});
}