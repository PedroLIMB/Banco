function validation() {
    if (document.CadastroLogin.Nome.value == "") {
        document.getElementById("resultado").innerHTML = "Insira nome de usuário";
        return false;
    } else if (document.CadastroLogin.Nome.value.length < 6) {
        document.getElementById("resultado").innerHTML = "Pelo menos seis caracteres";
        return false
    } else if (document.CadastroLogin.Email.value == "") {
        document.getElementById("resultado").innerHTML = "Insira o Email";
        return false;
    } else if (document.CadastroLogin.Senha.value == "") {
        document.getElementById("resultado").innerHTML = "Insira a senha";
        return false;
    } else if (document.CadastroLogin.Senha.value.length < 6) {
        document.getElementById("resultado").innerHTML = "A senha deve ter 6 dígitos";
        return false
    } else if (document.CadastroLogin.cSenha.value == "") {
        document.getElementById("resultado").innerHTML = "Insira a senha novamente";
        return false;
    } else if (document.CadastroLogin.Senha.value !== document.CadastroLogin.cSenha.value) {
        document.getElementById("resultado").innerHTML = "Suas senhas não correspondem";
        return false;
    } else {
        // Se todas as validações passarem, exibe o loginConfirmado
        loginConfirmado.classList.add("fecharConfirmacao");
        return false;
    }

}

var loginConfirmado = document.getElementById('loginConfirmado');
var valorDepositoInicial;

// Função para verificar se o depósito inicial foi feito antes de ativar o botão OK
function verificarDepositoInicial() {
    var valorDeposito = document.getElementById("valorTransacao").value;
    if (valorDeposito === "" || isNaN(valorDeposito) || parseFloat(valorDeposito) <= 0) {
        alert("Por favor, digite um valor válido para o depósito inicial.");
    } else {
        valorDepositoInicial = parseFloat(valorDeposito);
        document.getElementById("linkOK").innerHTML = '<button onclick="CloseSlide()">OK</button>';
    }
}

// Associar a função de verificação ao botão de fechar
document.getElementById("botaoDeposito").addEventListener("click", verificarDepositoInicial);

function CloseSlide() {
    if (valorDepositoInicial !== undefined) {
        // Aqui você pode adicionar lógica adicional, como registrar o depósito ou processá-lo de alguma forma
        alert("Depósito inicial de R$" + valorDepositoInicial.toFixed(2) + " realizado com sucesso!");
        loginConfirmado.classList.remove("fecharConfirmacao");
    } else {
        alert("Por favor, faça o depósito inicial antes de fechar.");
    }
}
