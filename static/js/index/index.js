$(document).ready(function () {
    $('#historicos_aluno').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,

        "lengthMenu": [
            [10, 25, 50, -1],
            ['10 registros', '25 registros', '50 registros', 'Exibir todos']
        ],
        "buttons": [
            'pageLength'
        ],
        "ajax": {
            "processing": true,
            "serverSide": true,
            "url": '/historicos/lista/alunos/json', // url da view
            "type": "GET", // metodo HTTP

        },
        "columns": [
            { "data": "aluno__cod_aluno", className: "text-center" },
            { "data": "aluno__nome_aluno" },
            { "data": "aluno__filiacao_aluno", className: "text-center" },
            { "data": "aluno__dt_nascimento_aluno", className: "text-center" },


            {
                "data": "Action", "render": function (data, type, row, meta) {
                    return '<button class="btn btn-info" id="btnPdf"><i class="far fa-file-pdf"></i></button> ';
                }
            }

        ],

        "columnDefs": [
            { "width": "10%", "targets": 0 },
            { "width": "50%", "targets": 1 },
            { "width": "30%", "targets": 2 },
            { "width": "15%", "targets": 3 },

        ],


        "language": {
            "paginate": {
                "previous": "Página anterior",
                "next": "Próxima página"
            },
            "search": "Buscar: ",
            "info": "Exibindo _START_ to _END_ of _TOTAL_ páginas",
            "lengthMenu": "Mostrar _MENU_ registros",
            "zeroRecords": "Nenhum registro encontrado",
            "emptyTable": "Nennhum registro carregado",
            "infoEmpty": "Página 0 de 0 de 0 registros",
        },
    });
});


$("#historicos_aluno tbody").on("click", "tr #btnPdf", function () {

    var table = $('#historicos_aluno').DataTable();
    var objTableHistoricos = table.row($(this).parents('tr')).data();
    var cod_aluno = objTableHistoricos['aluno__cod_aluno'];
    url = "/historicos/relatorio/pdf/" + cod_aluno;
    window.location.href = url


});