$("#btn_salvar_notas").attr("disabled", true);

var json_geral;

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
})

//ao submeter/clicar em pesquisar form do diario-nota:
$('#form_busca').on('submit', function (event) {//evento do form(filters)
    // $("#btncriartabela").attr("disabled", true);
    event.preventDefault();
    buscar_dados_tabela()
});

function buscar_dados_tabela() {
    //desabilitar os checks
    $("#check_eja1").prop('checked', false);
    $("#check_eja2").prop('checked', false);
    $("#check_eja3").prop('checked', false);
    $("#check_eja4").prop('checked', false);

    $.ajax({
        url: "tabela/notas", // url da view
        type: "GET", // metodo HTTP
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            dropAluno: $("#id_aluno").val(),
        },
        success: function (json) {
            json_geral = json
            $("#card_check").css("display", "block");
            $("#btn_salvar_notas").attr("disabled", false);
            $("#btn_gerar_pdf").removeClass('disabled');


            if (json.historico == false) {
                Swal.fire({
                    title: 'Esse aluno não tem nenhum histórico! <br>Insira as notas na tabela e salve para criar um histórico!',
                    text: 'Clique em ok para continuar',
                    icon: 'info',
                    confirmButtonText: 'ok'
                })
            }

            montar_tabela(json);
            montar_tabela_estudos(json);

            $.each(json.ejas, function (i, val) {
                if (val == "eja1") {
                    $("#check_eja1").prop('checked', true);
                }

                if (val == 'eja2') {
                    $("#check_eja2").prop('checked', true);
                }
                if (val == 'eja3') {
                    $("#check_eja3").prop('checked', true);
                }
                if (val == 'eja4') {
                    $("#check_eja4").prop('checked', true);
                }
                onchange_checkbox();
            });

        },

    });

}

function montar_tabela(json) {
    window.scrollBy(0, 400); // ScrollDown na página

    var tableHeaders = '';
    var tbodyColunas = '';
    //limpa a tabela
    $('#notas').empty();
    tableHeaders += "<th scope=col class=text-center>Área de Conhecimentos</th>"

    $.each(json.turmas, function (i, val) {
        tableHeaders += "<th scope=col class=text-center style=vertical-align:middle>" + val['ano_turma'] + "º Ano</th>";
    });

    $.each(json.disciplinas, function (i, disciplinas) {
        tbodyColunas += '<tr class="text-center">';
        tbodyColunas += '<td style="width:20px"><h5><span class="badge badge-secondary">' + disciplinas['nome_disciplina'] + '</h5></span></td>'
        $.each(json.turmas, function (k, turmas) {
            tbodyColunas += '<td style="width:130px"><div class="turma' + turmas['ano_turma'] + '"> <input class="form-control form-control-sm text-center" type="number" onwheel="this.blur()" step="0.01" min="0.00" max="10.00" placeholder="Digite" pattern="[0-9]+$" value="' + disciplinas['notas'][k] + '"></div></td>';
        });

        tbodyColunas += '</tr>';
    })

    //aqui add os header e as linhas a tabela(criando a tabela)
    $("#notas").append('<table id="table-notas" class="table table-head-fixed table-hover"><thead class=table-active><tr>' + tableHeaders + '</tr></thead><tbody>' + tbodyColunas + '</tbody></table>');

    //transformando a tabela em um datatatble
    var table = $("#table-notas").DataTable({
        //seleciona as colunas para navegar com as setas
        keys: {
            columns: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        stateSave: true,
        "dom": '<"toolbar">frtip',
        "tablescrollY": "390px",
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

    $('.datatable tbody')
        .on('mouseenter', 'td', function () {
            var colIdx = table.cell(this).index().column;
            $(table.cells().nodes()).removeClass('highlight');
            $(table.column(colIdx).nodes()).addClass('highlight');
        });

    $("div.toolbar").html(
        '<h6 class="card-title"><b>Esse aluno é:</b></h6>' +
        '<div class="row">' +
        '<div class="form-group col-sm-1 ">' +
        '<div class="form-check">' +
        '<input class="form-check-input" type="checkbox" id="check_eja1"' +
        'onchange="onchange_checkbox()">' +
        '<label class="form-check-label">EJA1</label>' +
        '</div>' +
        '</div>' +
        '<div class="form-group col-sm-1">' +
        '<div class="form-check">' +
        '<input class="form-check-input" type="checkbox" id="check_eja2"' +
        'onchange="onchange_checkbox()">' +
        '<label class="form-check-label">EJA2</label>' +
        '</div>' +
        '</div>' +
        '<div class="form-group col-sm-1">' +
        '<div class="form-check">' +
        '<input class="form-check-input" type="checkbox" id="check_eja3"' +
        'onchange="onchange_checkbox()">' +
        '<label class="form-check-label">EJA3</label>' +
        '</div>' +
        '</div>' +
        '<div class="form-group col-sm-1">' +
        '<div class="form-check">' +
        '<input class="form-check-input" type="checkbox" id="check_eja4"' +
        'onchange="onchange_checkbox()">' +
        '<label class="form-check-label">EJA4</label>' +
        '</div>' +
        '</div>' +
        '</div>');

}

function montar_tabela_estudos(json) {
    var tableHeaders = '';
    var tbodyColunas = '';
    //limpa a tabela
    $('#table2').empty();
    tableHeaders += "<th scope=col class=text-center>ANO</th>"
    tableHeaders += "<th scope=col class=text-center>ANO LETIVO</th>"
    tableHeaders += "<th scope=col class=text-center>ESTABELECIMENTO DE ENSINO</th>"
    tableHeaders += "<th scope=col class=text-center>MUNÍCIPIO</th>"
    tableHeaders += "<th scope=col class=text-center>UF</th>"
    tableHeaders += "<th scope=col class=text-center>RESULTADO</th>"

    $.each(json.estudos_feitos, function (k, estudos) {
        tbodyColunas += '<tr class="text-center">';
        tbodyColunas += '<td style="width:5px">' + estudos['ano_turma'] + 'º</td>'
        tbodyColunas += '<td style="width:8px"><input class="form-control form-control-sm text-center" type="number" placeholder="Digite" pattern="[0-9]+$" value="' + estudos['ano_letivo'] + '"></td>';
        tbodyColunas += '<td style="width:20px"><input class="form-control form-control-sm text-center" type="text" placeholder="Digite" value="' + estudos['escola'] + '"></td>';
        tbodyColunas += '<td style="width:10px"><input class="form-control form-control-sm text-center" type="text" placeholder="Digite" value="' + estudos['municipio'] + '"></td>';
        tbodyColunas += '<td style="width:10px"><input class="form-control form-control-sm text-center" type="text" placeholder="Digite" maxlength="2"  value="' + estudos['uf'] + '"></td>';

        if (estudos.resultado == "APROVADO(A)") {
            tbodyColunas += '<td style="width:15px">' +
                '<select class="form-control" id="sel1">' +
                '<option>Selecione...</option>' +
                '<option selected>APROVADO</option>' +
                '<option>REPROVADO</option>' +
                '</select></td>';
        }
        else if (estudos.resultado == "REPROVADO(A)") {
            tbodyColunas += '<td style="width:10px">' +
                '<select class="form-control" id="sel1">' +
                '<option>Selecione...</option>' +
                '<option selected>REPROVADO(A)</option>' +
                '<option >APROVADO(A)</option>' +
                '</select></td>';
        }
        else {
            tbodyColunas += '<td style="width:10px">' +
                '<select class="form-control" id="sel1">' +
                '<option selected>Selecione...</option>' +
                '<option >APROVADO(A)</option>' +
                '<option >REPROVADO(A)</option>' +
                '</select></td>';
        }
        tbodyColunas += '</tr>';


    })

    $("#table2").append('<table id="table-estudos" class="table table-head-fixed table-hover"><thead class=table-active><tr>' + tableHeaders + '</tr></thead><tbody>' + tbodyColunas + '</tbody></table>');


    var table = $("#table-estudos").DataTable({
        //seleciona as colunas para navegar com as setas
        keys: {
            columns: [1, 2, 3, 4, 5],
        },
        stateSave: true,
        "dom": '<"toolbar">frtip',
        "tablescrollY": "390px",
        "scrollCollapse": true,
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

    $('.datatable tbody')
        .on('mouseenter', 'td', function () {
            var colIdx = table.cell(this).index().column;
            $(table.cells().nodes()).removeClass('highlight');
            $(table.column(colIdx).nodes()).addClass('highlight');
        });
}

function onchange_checkbox() {
    //função reponsavel por desabilitar inputs nao usadados
    var checked_eja1 = $("#check_eja1").is(":checked");//eja1
    var checked_eja2 = $("#check_eja2").is(":checked");//eja2
    var checked_eja3 = $("#check_eja3").is(":checked");//eja3
    var checked_eja4 = $("#check_eja4").is(":checked");//eja4

    if (checked_eja1 == true) {
        $(".turma1 .form-control").prop('disabled', true)
        $(".turma2 .form-control").prop('disabled', true)
    }
    else {
        $(".turma1 .form-control").prop('disabled', false)
        $(".turma2 .form-control").prop('disabled', false)
    }

    if (checked_eja2 == true) {
        $(".turma4 .form-control").prop('disabled', true)

    }
    else {
        $(".turma4 .form-control").prop('disabled', false)
    }

    if (checked_eja3 == true) {
        $(".turma6 .form-control").prop('disabled', true)
    }
    else {
        $(".turma6 .form-control").prop('disabled', false)
    }

    if (checked_eja4 == true) {
        $(".turma8 .form-control").prop('disabled', true)
    }
    else {
        $(".turma8 .form-control").prop('disabled', false)
    }

}

function get_notas_tabela() {
    var arrayNovasNotas = [];

    var checked_eja1 = $("#check_eja1").is(":checked");//eja1
    var checked_eja2 = $("#check_eja2").is(":checked");//eja2
    var checked_eja3 = $("#check_eja3").is(":checked");//eja3
    var checked_eja4 = $("#check_eja4").is(":checked");//eja4

    $("#table-notas tbody tr").each(function (item) {
        var linhaAtual = $(this);
        var obj_notas = {};
        var lista_notas = [];
        var lista_nome_turma = []
        var i = 1;

        nome_disciplina = linhaAtual.find("td:eq(0)").text();

        linhaAtual.find("td div").each(function (params) {
            notas = linhaAtual.find("td:eq(" + i + ") input[type='number']").val()
            if (notas != undefined) {
                lista_notas.push(notas)
                lista_nome_turma.push(i)
            }
            i++;
        })
        obj_notas.cod_aluno = $("#id_aluno").val()
        obj_notas.notas = lista_notas
        obj_notas.nomes_turma = lista_nome_turma
        obj_notas.eja1 = checked_eja1
        obj_notas.eja2 = checked_eja2
        obj_notas.eja3 = checked_eja3
        obj_notas.eja4 = checked_eja4

        json_geral.disciplinas.forEach(element => {
            if (nome_disciplina == element['nome_disciplina']) {
                obj_notas.nome_disciplina = nome_disciplina
                obj_notas.cod_disciplina = element['cod_disciplina']
            }
        });
        arrayNovasNotas.push(obj_notas);
    });

    return arrayNovasNotas
}

function get_dados_tabela_estudos() {
    var arrayObjEstudos = []
    var cod_aluno = $("#id_aluno").val()

    $("#table-estudos tbody tr").each(function (item) {
        var linhaAtual = $(this);
        var obj_estudos = {};

        var turma = linhaAtual.find("td:eq(0)").text();
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
    // $("#btn_salvar_notas").attr("disabled", true);
    event.preventDefault();
    novasNotas = get_notas_tabela(json_geral)
    dadosTabelaEstudos = get_dados_tabela_estudos()

    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: "POST",
        contentType: "application/json",
        url: "tabela/notas",
        data: JSON.stringify(novasNotas), // convert array to JSON
        dataType: 'json',
        success: function (data) {
            toastr.success('Notas Salvas com Sucesso!')
            buscar_dados_tabela()

            $.ajax({
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                type: "POST",
                contentType: "application/json",
                url: "tabela/estudos",
                data: JSON.stringify(dadosTabelaEstudos), // convert array to JSON
                dataType: 'json',

                success: function (data) {

                    toastr.success('Dados de estudos salvos com sucesso!')

                    $("#btn_salvar_notas").attr("disabled", false);
                    buscar_dados_tabela()
                },

                error: function (data) {
                    Swal.fire({
                        title: "" + data.responseJSON.error + "",
                        text: 'Clique em ok para continuar',
                        icon: 'error',
                        confirmButtonText: 'Ok'
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
            })
        },
    });
});

function gerar_pdf() {
    var cod_aluno = $("#id_aluno").val();
    url = "/historicos/relatorio/pdf/" + cod_aluno;

    cod_button = document.getElementById('btn_gerar_pdf')
    cod_button.setAttribute("href", url);

};
