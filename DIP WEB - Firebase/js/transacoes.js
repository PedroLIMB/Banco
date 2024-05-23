document.addEventListener('DOMContentLoaded', () => {
    atualizarSaldoELimite();
    
    const botaoDeposito = document.getElementById('botaoDeposito');
    const botaoSaque = document.getElementById('botaoSaque');
    const botaoTransferencia = document.getElementById('botaoTransferencia');

    botaoDeposito.addEventListener('click', () => processarTransacao('deposito'));
    botaoSaque.addEventListener('click', () => processarTransacao('saque'));
    botaoTransferencia.addEventListener('click', () => processarTransacao('transferencia'));
});

function atualizarSaldoELimite() {
    fetch('/obter_saldo_e_limite', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('saldo').innerText = `R$ ${formatarNumero(data.saldo)}`;
            document.getElementById('limiteChequeEspecial').innerText = `R$ ${formatarNumero(data.limite_cheque_especial)}`;
        } else {
            console.error('Erro ao obter saldo e limite:', data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function formatarNumero(numero) {
    return parseFloat(numero).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function processarTransacao(tipo) {
    const valorTransacao = document.getElementById('valorTransacao').value;
    const emailDestinatario = document.getElementById('emailDestinatario').value;

    let url = '';
    let data = { valor: valorTransacao };

    if (tipo === 'deposito') {
        url = '/processar_deposito';
    } else if (tipo === 'saque') {
        url = '/processar_saque';
    } else if (tipo === 'transferencia') {
        url = '/processar_transferencia';
        data.destinatario = emailDestinatario;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${tipo.charAt(0).toUpperCase() + tipo.slice(1)} realizado com sucesso!`);
            document.getElementById('saldo').innerText = `R$ ${formatarNumero(data.saldo)}`;
        } else {
            alert(`Erro: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}
