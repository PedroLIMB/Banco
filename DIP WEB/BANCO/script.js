document.addEventListener("DOMContentLoaded", function() {
  // Verificar se o usuário está logado
  const emailLogado = localStorage.getItem('emailLogado');
  if (!emailLogado) {
    // Se o usuário não estiver logado, redirecionar para a página de login
    window.location.href = '../PÁGINA DE LOGIN/CADASTRO/cadastro.html';
    return; // Parar a execução do restante do código
  }

  // Selecionando os elementos HTML relevantes
  const saldoElement = document.getElementById("saldo");
  const limiteChequeEspecialElement = document.getElementById("limiteChequeEspecial");
  const valorTransacaoInput = document.getElementById("valorTransacao");
  const resultadoElement = document.getElementById("resultado");

  // Função para atualizar o saldo exibido na página
  function atualizarSaldo(valor) {
    saldoElement.textContent = `R$${valor.toFixed(2)}`;
  }

  // Função para exibir mensagens de resultado na página
  function exibirResultado(mensagem) {
    resultadoElement.textContent = mensagem;
  }

  // Função para definir o limite do cheque especial
  function definirLimiteChequeEspecial(valor) {
    limiteChequeEspecialElement.textContent = `R$${valor.toFixed(2)}`;
  }

  // Função para exibir o formulário de transferência
  function exibirFormularioTransferencia() {
    // Criação dos elementos HTML para o formulário de transferência
    const container = document.createElement("div");
    container.className = "prompt-container";

    const formulario = document.createElement("div");
    formulario.className = "formulario-transferencia";

    const mensagem = document.createElement("p");
    mensagem.textContent = "Por favor, insira o valor que deseja transferir (em R$) e o número da conta de destino:";
    formulario.appendChild(mensagem);

    const valorLabel = document.createElement("label");
    valorLabel.textContent = "Valor:";
    formulario.appendChild(valorLabel);

    const valorInput = document.createElement("input");
    valorInput.type = "number";
    valorInput.placeholder = "Digite o valor";
    formulario.appendChild(valorInput);

    const contaLabel = document.createElement("label");
    contaLabel.textContent = "Número da Conta:";
    formulario.appendChild(contaLabel);

    const contaInput = document.createElement("input");
    contaInput.type = "text";
    contaInput.placeholder = "Digite o número da conta de destino";
    formulario.appendChild(contaInput);

    const botaoConfirmar = document.createElement("button");
    botaoConfirmar.textContent = "Confirmar Transferência";
    botaoConfirmar.addEventListener("click", function() {
      const valor = parseFloat(valorInput.value);
      const contaDestino = contaInput.value;
      // Executar a transação de transferência
      executarTransacao("Transferência", valor, contaDestino);
      container.remove();
    });
    formulario.appendChild(botaoConfirmar);

    const botaoCancelar = document.createElement("button");
    botaoCancelar.textContent = "Cancelar";
    botaoCancelar.addEventListener("click", function() {
      container.remove();
    });
    formulario.appendChild(botaoCancelar);

    // Adicionando o formulário ao contêiner e ao documento HTML
    container.appendChild(formulario);
    document.body.appendChild(container);
  }

  // Função para exibir a pergunta sobre o uso do cheque especial
  function exibirPerguntaChequeEspecial() {
    const usarChequeEspecial = confirm("Você deseja usar o cheque especial?");
    return usarChequeEspecial;
  }

  // Função para executar uma transação
  function executarTransacao(tipo, valor, contaDestino) {
    const valorTransacao = parseFloat(valor);
    if (isNaN(valorTransacao) || valorTransacao <= 0) {
      // Verificar se o valor da transação é válido
      exibirResultado("Por favor, digite um valor válido.");
      return;
    }

    // Obter o saldo atual
    const saldoAtual = parseFloat(saldoElement.textContent.replace("R$", ""));

    if (tipo === "Saque" && valorTransacao > saldoAtual) {
      // Verificar se é uma transação de saque e se o saldo é suficiente
      const usarChequeEspecial = exibirPerguntaChequeEspecial();
      if (!usarChequeEspecial) {
        // Se o usuário não quiser usar o cheque especial, cancelar a transação
        exibirResultado("Saque cancelado.");
        return;
      }
    }

    // Realizar a transação com base no tipo
    switch (tipo) {
      case "Depósito":
        depositar(valorTransacao, saldoAtual);
        break;
      case "Saque":
        sacar(valorTransacao, saldoAtual);
        break;
      case "Transferência":
        transferir(valorTransacao, saldoAtual, contaDestino);
        break;
      default:
        exibirResultado("Tipo de transação inválido.");
        break;
    }
  }

  // Função para processar um depósito
  function depositar(valor, saldoAtual) {
    const novoSaldo = saldoAtual + valor;
    // Atualizar o saldo exibido na página
    atualizarSaldo(novoSaldo);
    // Exibir mensagem de sucesso
    exibirResultado(`Depósito de R$${valor.toFixed(2)} realizado com sucesso.`);
  }

  // Função para processar um saque
  function sacar(valor, saldoAtual) {
    const saldoDisponivel = saldoAtual + limiteChequeEspecial;
    if (valor > saldoDisponivel) {
      // Verificar se o saldo e o limite de cheque especial são suficientes para o saque
      exibirResultado("Saldo e limite de cheque especial insuficientes para realizar o saque.");
      return;
    }
    // Calcular o novo saldo após o saque
    const novoSaldo = saldoAtual - valor;
    // Atualizar o saldo exibido na página
    atualizarSaldo(novoSaldo);
    // Exibir mensagem de sucesso
    exibirResultado(`Saque de R$${valor.toFixed(2)} realizado com sucesso.`);
  }

  // Função para processar uma transferência
  function transferir(valor, saldoAtual, contaDestino) {
    const saldoDisponivel = saldoAtual + limiteChequeEspecial;
    if (valor > saldoDisponivel) {
      // Verificar se o saldo e o limite de cheque especial são suficientes para a transferência
      exibirResultado("Saldo e limite de cheque especial insuficientes para realizar a transferência.");
      return;
    }
    // Calcular o novo saldo após a transferência
    const novoSaldo = saldoAtual - valor;
    // Atualizar o saldo exibido na página
    atualizarSaldo(novoSaldo);
    // Exibir mensagem de sucesso
    exibirResultado(`Transferência de R$${valor.toFixed(2)} para a conta ${contaDestino} realizada com sucesso.`);
  }

  // Adicionar ouvintes de eventos aos botões de transação
  document.getElementById("botaoDeposito").addEventListener("click", function() {
    const valor = valorTransacaoInput.value;
    // Executar uma transação de depósito
    executarTransacao("Depósito", valor);
  });

  document.getElementById("botaoSaque").addEventListener("click", function() {
    const valor = valorTransacaoInput.value;
    // Executar uma transação de saque
    executarTransacao("Saque", valor);
  });

  document.getElementById("botaoTransferencia").addEventListener("click", function() {
    // Exibir o formulário de transferência
    exibirFormularioTransferencia();
  });

  // Recuperar o valor do depósito inicial do localStorage
  const email = localStorage.getItem('emailLogado');
  const userData = localStorage.getItem(email);
  if (userData) {
    const usuario = JSON.parse(userData);
    const depositoInicial = parseFloat(usuario.depositoInicial);
    if (!isNaN(depositoInicial) && depositoInicial > 0) {
      // Atualizar o saldo com o valor do depósito inicial
      atualizarSaldo(depositoInicial);

      // Definir o limite do cheque especial como 4 vezes o valor do depósito inicial
      const limiteChequeEspecial = depositoInicial * 4;
      definirLimiteChequeEspecial(limiteChequeEspecial);
    }
  }
});
