//ao submeter/clicar em pesquisar form do diario-nota:
$('#form_busca').on('submit', function (event) {//evento do form(filters)
    // $("#btncriartabela").attr("disabled", true);
    event.preventDefault();
    // window.scrollBy(0, 400); // ScrollDown na página 
    // busca_dados_tabela()

    $.ajax({
        url: "historico/tabela/notas", // url da view
        type: "GET", // metodo HTTP
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            dropAluno: $("#id_aluno").val(),
        },
        success: function (json) {
            console.log(json)
        },

    });
});