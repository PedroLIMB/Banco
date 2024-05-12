package com.example.bancodip.view;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.app.PendingIntent;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentSender;
import android.os.Bundle;
import android.preference.PreferenceManager;

import com.example.bancodip.R;
import com.example.bancodip.controller.ControllerBancoDados;
import com.example.bancodip.databinding.ActivityTransferirBinding;

public class TransferirActivity extends AppCompatActivity {

    private ActivityTransferirBinding binding;
    private ControllerBancoDados controllerBancoDados;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityTransferirBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        controllerBancoDados = new ControllerBancoDados(this);

        controllerBancoDados.open();

        Intent intent = getIntent();
        String emailUser = intent.getStringExtra("email_trans");
        Double saldoUser = controllerBancoDados.getSaldoByTitular(emailUser);
        Double chequeUser = controllerBancoDados.getChequeByTitular(emailUser);

        binding.btnTransferirUser.setOnClickListener(v -> {
            String destinatarioEmail = binding.transUserEmail.getText().toString().toUpperCase();
            Double destinatarioSaldo = controllerBancoDados.getSaldoByTitular(destinatarioEmail);
            String valorUser = binding.transUserValor.getText().toString();

            if (controllerBancoDados.isEmailInDatabase(destinatarioEmail) && !destinatarioEmail.equals(emailUser)) {
                try {
                    Double valorTransferencia = Double.parseDouble(valorUser);

                    // Verifica se o saldo é suficiente para a transferência
                    if (saldoUser < valorTransferencia && chequeUser + saldoUser < valorTransferencia) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(this);
                        builder.setMessage("SALDO E CHEQUE ESPECIAL INSUFICIENTES PARA REALIZAR A TRANSFERÊNCIA");
                        builder.setPositiveButton("Ok", (dialog, which) -> {});
                        AlertDialog alerta = builder.create();
                        alerta.show();
                        return;
                    }

                    // Atualiza os saldos
                    Double saldoUserNew = saldoUser - valorTransferencia;
                    Double saldoDestinatarioNew = destinatarioSaldo + valorTransferencia;
                    Double chequeUserNew = chequeUser;

                    if (saldoUser < valorTransferencia) {
                        // Usa o cheque especial para cobrir a diferença
                        chequeUserNew -= valorTransferencia - saldoUser;
                    }

                    controllerBancoDados.updateSaldo(destinatarioEmail, saldoDestinatarioNew);
                    controllerBancoDados.updateSaldo(emailUser, saldoUserNew);
                    controllerBancoDados.updateCheque(emailUser, chequeUserNew);

                    // Exibe mensagem de sucesso
                    AlertDialog.Builder builder = new AlertDialog.Builder(this);
                    builder.setMessage("TRANSFERÊNCIA EFETUADA COM SUCESSO");
                    builder.setPositiveButton("Ok", (dialog, which) -> {});
                    AlertDialog alerta = builder.create();
                    alerta.show();
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    controllerBancoDados.close();
                    binding.transUserValor.setText("");
                    binding.transUserEmail.setText("");
                }
            } else {
                // Email do destinatário não cadastrado
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setMessage("EMAIL DO DESTINATÁRIO NÃO CADASTRADO");
                builder.setPositiveButton("Ok", (dialog, which) -> {});
                AlertDialog alerta = builder.create();
                alerta.show();
            }

        });




    }



}