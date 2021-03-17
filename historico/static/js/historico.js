// $("#btn_salvar_notas").attr("disabled", true);

$(document).ready(function () {
    $('.select2bs4').select2();

    var table = $("#table-notas").DataTable({
        //seleciona as colunas para navegar com as setas
        keys: {
            columns: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        stateSave: true,
        "dom": '<"toolbar">frtip',
        "scrollY": "300px",
        "scrollCollapse": true,
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": false,
        "responsive": true,
        "destroy": true,
        "language": {
            "search": "Buscar: ",
            "zeroRecords": "Nenhum registro encontrado",
            "emptyTable": "Nennhum registro carregado",
        },
        //deixar celular navegaveis estilo excel
    }).on('key-focus', function (e, datatable, cell, originalEvent) {
        $('input', cell.node()).focus();
    }).on("focus", "td input", function () {
        $(this).select();
    });;

    var table2 = $("#table-estudos").DataTable({
        //seleciona as colunas para navegar com as setas
        keys: {
            columns: [1, 2, 3, 4, 5],
        },
        stateSave: true,
        "dom": '<"toolbar">frtip',
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
        "autoWidth": false,
        "responsive": true,
        "destroy": true,
        "language": {
            "search": "Buscar: ",
            "zeroRecords": "Nenhum registro encontrado",
            "emptyTable": "Nennhum registro carregado",
        },
        //deixar celular navegaveis estilo excel
    }).on('key-focus', function (e, datatable, cell, originalEvent) {
        $('input', cell.node()).focus();
    }).on("focus", "td input", function () {
        $(this).select();
    });;

    $('.datatable tbody').on('mouseenter', 'td', function () {
        var colIdx = table.cell(this).index().column;
        $(table.cells().nodes()).removeClass('highlight');
        $(table.column(colIdx).nodes()).addClass('highlight');
    });


});

var json_geral;

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
})

function onchange_checkbox() {

    var checked_eja3 = $("#check_eja3").is(":checked");//eja3
    var checked_eja4 = $("#check_eja4").is(":checked");//eja4

    if (checked_eja3 == true) {
        document.getElementById("input-oferta-anual-3").setAttribute('value', '');
    }
    else {
        document.getElementById("input-oferta-anual-4").setAttribute('value', '');
    }

    if (checked_eja4 == true) {
        $(".turma8 .form-control").prop('disabled', true)
    }
    else {
        $(".turma8 .form-control").prop('disabled', false)
    }

}
function onchange_check_eja1() {
    //função reponsavel por limpar os inputs da oferta anual

    var checked_eja1 = $("#check_eja1").is(":checked");//eja1

    if (checked_eja1 == true) {
        document.getElementById("input-oferta-anual-1").setAttribute('value', '');
        document.getElementById("input-oferta-anual-1").setAttribute('class', 'form-control is-warning form-control-sm text-center')

        document.getElementById("input-oferta-anual-2").setAttribute('value', '');
        document.getElementById("input-oferta-anual-2").setAttribute('class', 'form-control is-warning form-control-sm text-center');

        document.getElementById("input-oferta-anual-3").setAttribute('value', '');
        document.getElementById("input-oferta-anual-3").setAttribute('class', 'form-control is-warning form-control-sm text-center');
    }
    else {
        document.getElementById("input-oferta-anual-1").setAttribute('value', '880');
        document.getElementById("input-oferta-anual-1").setAttribute('class', 'form-control is-valid form-control-sm text-center')

        document.getElementById("input-oferta-anual-2").setAttribute('value', '880');
        document.getElementById("input-oferta-anual-2").setAttribute('class', 'form-control is-valid form-control-sm text-center')

        document.getElementById("input-oferta-anual-3").setAttribute('value', '880');
        document.getElementById("input-oferta-anual-3").setAttribute('class', 'form-control is-valid form-control-sm text-center')
    }
}

function onchange_check_eja2() {
    //função reponsavel por limpar os inputs da oferta anual do eja2 (turmas 4 e 5)

    var checked_eja2 = $("#check_eja2").is(":checked");//eja2

    if (checked_eja2 == true) {
        document.getElementById("input-oferta-anual-4").setAttribute('value', '');
        document.getElementById("input-oferta-anual-4").setAttribute('class', 'form-control is-warning form-control-sm text-center');

        document.getElementById("input-oferta-anual-5").setAttribute('value', '');
        document.getElementById("input-oferta-anual-5").setAttribute('class', 'form-control is-warning form-control-sm text-center');

    }
    else {
        document.getElementById("input-oferta-anual-4").setAttribute('value', '880');
        document.getElementById("input-oferta-anual-4").setAttribute('class', 'form-control is-valid form-control-sm text-center');

        document.getElementById("input-oferta-anual-5").setAttribute('value', '814');
        document.getElementById("input-oferta-anual-5").setAttribute('class', 'form-control is-valid form-control-sm text-center');
    }
}

function add_row_table() {
    //criando linha
    var tbody_table = document.getElementById("row_notas");
    var create_row = document.createElement('tr');
    var count = (document.getElementsByTagName("tr").length) - 1
    //terminou de criar linha

    //seta um id no tr novo
    create_row.setAttribute('id', count);
    //pega a linha nova criada
    var tmplMarkup = $("#disciplina-notas").html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
    create_row.innerHTML = compiledTmpl
    tbody_table.appendChild(create_row);

    $(".select2bs4").select2();

};

function get_notas_tabela() {
    var arrayNovasNotas = [];

    var checked_eja1 = $("#check_eja1").is(":checked");//eja1
    var checked_eja2 = $("#check_eja2").is(":checked");//eja2
    var checked_eja3 = $("#check_eja3").is(":checked");//eja3
    var checked_eja4 = $("#check_eja4").is(":checked");//eja4
    var cont_id_td = 1;

    $("#table-notas tbody tr").each(function (item) {
        var linhaAtual = $(this);
        var obj_notas = {};
        var lista_notas = [];
        var lista_nome_turma = []
        var i = 1;

        linhaAtual.find("td").each(function (params) {
            notas = linhaAtual.find("td:eq(" + i + ") input[type='number']").val()
            if (notas != '' || notas != "" || notas != undefined) {
                lista_notas.push(notas)
                lista_nome_turma.push(i)
            }
            i++;
            if (i == 10) {
                return false;
            }
        })
        if (item == 0) {
            obj_notas.cod_disciplina = linhaAtual.find("td:eq(0) #id_form-0-disciplinas").val() || linhaAtual.find("td:eq(0) #id_disciplinas").val();
        }
        else {
            obj_notas.cod_disciplina = linhaAtual.find("td:eq(0) #id_form-" + item + "-disciplinas").val() || linhaAtual.find("td:eq(0) #id_disciplinas").val();
            cont_id_td++;
        }
        obj_notas.cod_aluno = $("#id_alunos").val()
        obj_notas.notas = lista_notas
        obj_notas.nomes_turma = lista_nome_turma
        obj_notas.eja1 = checked_eja1
        obj_notas.eja2 = checked_eja2
        obj_notas.eja3 = checked_eja3
        obj_notas.eja4 = checked_eja4

        if (obj_notas.cod_disciplina != undefined) {
            arrayNovasNotas.push(obj_notas);
        }
    });
    return arrayNovasNotas
}

function get_ch_anual() {
    var array_ch_anos_turma = []
    var obj_ch_anos = {};

    obj_ch_anos.cod_aluno = $("#id_alunos").val()

    $("#table_oferta_anual tbody tr td").each(function (item) {
        var td_atual = $(this);
        array_ch_anos_turma.push(td_atual.find("input[type='number']").val())
    });

    obj_ch_anos.ofertas_ano = array_ch_anos_turma

    return obj_ch_anos

}

function get_dados_tabela_estudos() {
    var arrayObjEstudos = []
    var cod_aluno = $("#id_alunos").val()

    $("#table-estudos tbody tr").each(function (item) {
        var linhaAtual = $(this);
        var obj_estudos = {};

        var turma = linhaAtual.find("td:eq(0) #turma").text();
        var ano_letivo = linhaAtual.find("td:eq(1) input[type='number']").val();
        var nome_escola = linhaAtual.find("td:eq(2) input[type='text']").val();
        var nome_cidade = linhaAtual.find("td:eq(3) input[type='text']").val();
        var nome_estado = linhaAtual.find("td:eq(4) input[type='text']").val();
        var resultado = linhaAtual.find("td:eq(5) #sel1").val();

        obj_estudos.cod_aluno = cod_aluno
        obj_estudos.turma = turma
        obj_estudos.ano_letivo = ano_letivo
        obj_estudos.escola = nome_escola
        obj_estudos.cidade = nome_cidade
        obj_estudos.estado = nome_estado
        if (resultado != "Selecione...") {
            obj_estudos.resultado = resultado
        }

        else {
            obj_estudos.resultado = ""
        }

        arrayObjEstudos.push(obj_estudos)

    });
    return arrayObjEstudos

}
$('#form_table_notas').on('submit', function (event) {
    $("#btn_salvar_notas").attr("disabled", true);
    event.preventDefault();
    novasNotas = get_notas_tabela()
    dadosTabelaEstudos = get_dados_tabela_estudos()

    if ($('#id_alunos').val() == '') {
        Swal.fire({
            title: "Selecione um aluno por favor!",
            text: 'Clique em ok para continuar',
            icon: 'info',
            confirmButtonText: 'Ok'
        })
        $("#btn_salvar_notas").attr("disabled", false);

    }

    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: "POST",
        contentType: "application/json",
        url: "/historicos/tabela/notas",
        data: JSON.stringify(novasNotas), // convert array to JSON
        dataType: 'json',
        success: function (data) {
            toastr.success('Notas Salvas com Sucesso!')

            $.ajax({
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                type: "POST",
                contentType: "application/json",
                url: "/historicos/tabela/estudos",
                data: JSON.stringify(dadosTabelaEstudos), // convert array to JSON
                dataType: 'json',

                success: function (data) {
                    toastr.success('Dados de estudos salvos com sucesso!')

                    //ajax oferta anual
                    $.ajax({
                        headers: { "X-CSRFToken": $.cookie("csrftoken") },
                        type: "POST",
                        contentType: "application/json",
                        url: "/historicos/tabela/ofertaanual",
                        data: JSON.stringify(get_ch_anual()), // convert array to JSON
                        dataType: 'json',

                        success: function (data) {
                            toastr.success('Oferta anual salvo com sucesso!')
                            $("#btn_salvar_notas").attr("disabled", false);

                            function reload() {
                                document.location.reload();
                            }
                            setTimeout(reload, 1000);
                        },

                        error: function (data) {
                            Swal.fire({
                                title: "" + data.responseJSON.messages + "",
                                text: 'Clique em ok para continuar',
                                icon: 'error',
                                confirmButtonText: 'Ok'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    document.location.reload();
                                }
                            })
                        },
                    })
                },

                error: function (data) {
                    Swal.fire({
                        title: "" + data.responseJSON.error + "",
                        text: 'Clique em ok para continuar',
                        icon: 'error',
                        confirmButtonText: 'Ok'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            document.location.reload();
                        }
                    })
                },
            })
        },
        error: function (data) {
            Swal.fire({
                title: '' + data.responseJSON.error + '',
                text: 'Clique em ok para continuar',
                icon: 'error',
                confirmButtonText: 'Ok'
            }).then((result) => {
                if (result.isConfirmed) {
                    document.location.reload();
                }
            })
        },
    });
});

function click_pesquisar() {
    var cod_aluno = $('#id_alunos').val();
    $('#form_busca').attr('action', '/historicos/update/' + cod_aluno);
    $('#form_busca').submit()
}


function gerar_pdf() {
    var cod_aluno = $("#id_alunos").val();
    url = "/historicos/relatorio/pdf/" + cod_aluno;

    cod_button = document.getElementById('btn_gerar_pdf')
    cod_button.setAttribute("href", url);

};
