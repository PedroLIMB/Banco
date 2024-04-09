// Função de depósito
document.getElementById('botaoDeposito').addEventListener('click', function() {
    var valor = parseFloat(document.getElementById('valorTransacao').value);
    if (!isNaN(valor) && valor > 0) {
      animarBotao(this);
      atualizarSaldo(valor);
      mostrarMensagemResultado('Depósito realizado com sucesso!');
    } else {
      mostrarMensagemResultado('Por favor, digite um valor válido.');
    }
  });
  
  // Função de saque
  document.getElementById('botaoSaque').addEventListener('click', function() {
    var valor = parseFloat(document.getElementById('valorTransacao').value);
    if (!isNaN(valor) && valor > 0) {
      animarBotao(this);
      atualizarSaldo(-valor);
      mostrarMensagemResultado('Saque realizado com sucesso!');
    } else {
      mostrarMensagemResultado('Por favor, digite um valor válido.');
    }
  });
  
  // Função de transferência
  document.getElementById('botaoTransferencia').addEventListener('click', function() {
    var valor = parseFloat(document.getElementById('valorTransacao').value);
    if (!isNaN(valor) && valor > 0) {
      animarBotao(this);
      atualizarSaldo(-valor);
      mostrarMensagemResultado('Transferência realizada com sucesso!');
    } else {
      mostrarMensagemResultado('Por favor, digite um valor válido.');
    }
  });
  
  // Animação do botão
  function animarBotao(botao) {
    botao.classList.add('clicado');
    setTimeout(function() {
      botao.classList.remove('clicado');
    }, 300);
  }
  
  // Atualizar saldo
  function atualizarSaldo(valor) {
    var elementoSaldo = document.getElementById('saldo');
    var saldoAtual = parseFloat(elementoSaldo.innerText.replace('R$', ''));
    var novoSaldo = saldoAtual + valor;
    elementoSaldo.innerText = 'R$' + novoSaldo.toFixed(2);
  }
  
  // Mostrar mensagem de resultado
  function mostrarMensagemResultado(mensagem) {
    var elementoResultado = document.getElementById('resultado');
    elementoResultado.innerText = mensagem;
    elementoResultado.classList.add('exibir');
    setTimeout(function() {
      elementoResultado.classList.remove('exibir');
    }, 2000);
  }
  