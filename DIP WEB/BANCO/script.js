document.addEventListener("DOMContentLoaded", function() {
  const saldoElement = document.getElementById("saldo");
  const valorTransacaoInput = document.getElementById("valorTransacao");
  const resultadoElement = document.getElementById("resultado");
  const limiteChequeEspecial = 500; // Defina o limite do cheque especial aqui

  // Função para atualizar o saldo
  function atualizarSaldo(valor) {
    saldoElement.textContent = `R$${valor.toFixed(2)}`;
  }

  // Função para exibir mensagem de resultado
  function exibirResultado(mensagem) {
    resultadoElement.textContent = mensagem;
  }

  // Função para executar uma transação
  function executarTransacao(valor, tipo) {
    const valorTransacao = parseFloat(valor);
    if (isNaN(valorTransacao) || valorTransacao <= 0) {
      exibirResultado("Por favor, digite um valor válido.");
      return;
    }

    let saldoAtual = parseFloat(saldoElement.textContent.replace("R$", ""));
    let novoSaldo;

    switch (tipo) {
      case "Depósito":
        novoSaldo = saldoAtual + valorTransacao;
        exibirResultado(`Depósito de R$${valorTransacao.toFixed(2)} realizado com sucesso.`);
        break;
      case "Saque":
        if (valorTransacao > saldoAtual + limiteChequeEspecial) {
          exibirResultado("Saldo e limite de cheque especial insuficientes para realizar o saque.");
          return;
        }
        novoSaldo = saldoAtual - valorTransacao;
        exibirResultado(`Saque de R$${valorTransacao.toFixed(2)} realizado com sucesso.`);
        break;
      case "Transferência":
        if (valorTransacao > saldoAtual + limiteChequeEspecial) {
          exibirResultado("Saldo e limite de cheque especial insuficientes para realizar a transferência.");
          return;
        }
        novoSaldo = saldoAtual - valorTransacao;
        exibirResultado(`Transferência de R$${valorTransacao.toFixed(2)} realizada com sucesso.`);
        break;
      default:
        exibirResultado("Tipo de transação inválido.");
        return;
    }

    atualizarSaldo(novoSaldo);
  }

  // Adicionando evento de clique aos botões de transação
  document.getElementById("botaoDeposito").addEventListener("click", function() {
    const valor = valorTransacaoInput.value;
    executarTransacao(valor, "Depósito");
  });

  document.getElementById("botaoSaque").addEventListener("click", function() {
    const valor = valorTransacaoInput.value;
    executarTransacao(valor, "Saque");
  });

  document.getElementById("botaoTransferencia").addEventListener("click", function() {
    const valor = valorTransacaoInput.value;
    executarTransacao(valor, "Transferência");
  });
});
