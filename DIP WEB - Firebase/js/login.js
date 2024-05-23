const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const bcrypt = require('bcryptjs');
const admin = require('firebase-admin');
const Decimal = require('decimal.js');

// Inicialize o Firebase Admin SDK
const serviceAccount = require('./firebase-config.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});
const db = admin.firestore();

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));

app.use(session({
  secret: 'SECRETO',
  resave: false,
  saveUninitialized: true,
}));

// Rotas
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/cadastro.html');
});

app.post('/processar_cadastro', async (req, res) => {
  const { nome, email, senha, cSenha, depositoInicial } = req.body;

  if (senha !== cSenha) {
    res.status(400).send('As senhas não coincidem.');
    return;
  }

  const saldoInicial = new Decimal(depositoInicial || 0);
  if (saldoInicial.lte(0)) {
    res.status(400).send('Por favor, insira um saldo inicial válido.');
    return;
  }

  const userRef = db.collection('usuarios').doc(email);
  const userDoc = await userRef.get();
  if (userDoc.exists) {
    res.status(400).send('Este endereço de e-mail já está em uso. Por favor, escolha outro.');
    return;
  }

  const hashedSenha = await bcrypt.hash(senha, 10);
  const limiteChequeEspecial = saldoInicial.mul(4);

  try {
    await userRef.set({
      nome,
      email,
      senha: hashedSenha,
      saldo: saldoInicial.toString(),
      limite_cheque_especial: limiteChequeEspecial.toString(),
    });
    res.status(201).send('Cadastro realizado com sucesso!');
  } catch (e) {
    res.status(500).send(`Erro ao cadastrar usuário: ${e.message}`);
  }
});

app.get('/login', (req, res) => {
  res.sendFile(__dirname + '/public/login.html');
});

app.post('/processar_login', async (req, res) => {
  const { email, senha } = req.body;
  const userRef = db.collection('usuarios').doc(email);
  const userDoc = await userRef.get();

  if (userDoc.exists && await bcrypt.compare(senha, userDoc.data().senha)) {
    req.session.email = email;
    res.status(200).send('Login bem-sucedido!');
  } else {
    res.status(400).send('Email ou senha incorretos.');
  }
});

app.get('/index', (req, res) => {
  if (!req.session.email) {
    res.redirect('/login');
  } else {
    res.sendFile(__dirname + '/public/index.html');
  }
});

app.get('/obter_saldo_e_limite', async (req, res) => {
  if (!req.session.email) {
    res.status(401).json({ success: false, message: 'Você precisa estar logado para obter o saldo e o limite de cheque especial.' });
    return;
  }

  const userRef = db.collection('usuarios').doc(req.session.email);
  const userDoc = await userRef.get();

  if (!userDoc.exists) {
    res.status(404).json({ success: false, message: 'Usuário não encontrado.' });
  } else {
    const { saldo, limite_cheque_especial } = userDoc.data();
    res.json({ success: true, saldo, limite_cheque_especial });
  }
});

app.post('/processar_saque', async (req, res) => {
  if (!req.session.email) {
    res.status(401).json({ success: false, message: 'Você precisa estar logado para realizar saques.' });
    return;
  }

  const { valor } = req.body;
  const valorDecimal = new Decimal(valor);

  if (valorDecimal.lte(0)) {
    res.status(400).json({ success: false, message: 'O valor do saque deve ser maior que zero.' });
    return;
  }

  const userRef = db.collection('usuarios').doc(req.session.email);
  const userDoc = await userRef.get();

  if (!userDoc.exists) {
    res.status(404).json({ success: false, message: 'Usuário não encontrado.' });
    return;
  }

  const usuario = userDoc.data();
  const saldo = new Decimal(usuario.saldo);
  const limiteChequeEspecial = new Decimal(usuario.limite_cheque_especial);

  if (valorDecimal.gt(saldo.plus(limiteChequeEspecial))) {
    res.status(400).json({ success: false, message: 'Saldo e limite de cheque especial insuficientes para o saque.' });
    return;
  }

  await userRef.update({
    saldo: saldo.minus(valorDecimal).toString(),
  });

  res.json({ success: true, saldo: saldo.minus(valorDecimal).toString() });
});

app.post('/processar_deposito', async (req, res) => {
  if (!req.session.email) {
    res.status(401).json({ success: false, message: 'Você precisa estar logado para realizar depósitos.' });
    return;
  }

  const { valor } = req.body;
  const valorDecimal = new Decimal(valor);

  if (valorDecimal.lte(0)) {
    res.status(400).json({ success: false, message: 'O valor do depósito deve ser maior que zero.' });
    return;
  }

  const userRef = db.collection('usuarios').doc(req.session.email);
  const userDoc = await userRef.get();

  if (!userDoc.exists) {
    res.status(404).json({ success: false, message: 'Usuário não encontrado.' });
    return;
  }

  const saldo = new Decimal(userDoc.data().saldo);

  await userRef.update({
    saldo: saldo.plus(valorDecimal).toString(),
  });

  res.json({ success: true, saldo: saldo.plus(valorDecimal).toString() });
});

app.post('/processar_transferencia', async (req, res) => {
  if (!req.session.email) {
    res.status(401).json({ success: false, message: 'Você precisa estar logado para realizar transferências.' });
    return;
  }

  const { valor, destinatario } = req.body;
  const valorDecimal = new Decimal(valor);

  if (valorDecimal.lte(0)) {
    res.status(400).json({ success: false, message: 'O valor da transferência deve ser maior que zero.' });
    return;
  }

  const remetenteRef = db.collection('usuarios').doc(req.session.email);
  const remetenteDoc = await remetenteRef.get();

  if (!remetenteDoc.exists) {
    res.status(404).json({ success: false, message: 'Remetente não encontrado.' });
    return;
  }

  const destinatarioRef = db.collection('usuarios').doc(destinatario);
  const destinatarioDoc = await destinatarioRef.get();

  if (!destinatarioDoc.exists) {
    res.status(404).json({ success: false, message: 'Destinatário não encontrado.' });
    return;
  }

  const remetente = remetenteDoc.data();
  const saldoRemetente = new Decimal(remetente.saldo);
  const limiteChequeEspecialRemetente = new Decimal(remetente.limite_cheque_especial);

  if (valorDecimal.gt(saldoRemetente.plus(limiteChequeEspecialRemetente))) {
    res.status(400).json({ success: false, message: 'Saldo e limite de cheque especial insuficientes para a transferência.' });
    return;
  }

  const saldoDestinatario = new Decimal(destinatarioDoc.data().saldo);

  await remetenteRef.update({
    saldo: saldoRemetente.minus(valorDecimal).toString(),
  });

  await destinatarioRef.update({
    saldo: saldoDestinatario.plus(valorDecimal).toString(),
  });

  res.json({ success: true, saldo: saldoRemetente.minus(valorDecimal).toString(), limite_cheque_especial: limiteChequeEspecialRemetente.toString() });
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
