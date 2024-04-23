package com.example.bancodip.view;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import com.example.bancodip.R;
import com.example.bancodip.controller.ControllerBancoDados;
import com.example.bancodip.databinding.ActivityMainBinding;
import com.example.bancodip.model.ModelBancoDados;

public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;
    private ControllerBancoDados controllerBancoDados;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        controllerBancoDados = new ControllerBancoDados(this);

        Intent intentTrans = new Intent(MainActivity.this, TransferirActivity.class);
        Intent intent = getIntent();

        String nome = intent.getStringExtra("nome");
        String email = intent.getStringExtra("email");

        try {
            controllerBancoDados.open();

            Double saldoBanco = controllerBancoDados.getSaldoByTitular(email);
            Double chequeBanco = controllerBancoDados.getChequeByTitular(email);
            String saldoString = String.valueOf(saldoBanco);
            String chequeString = String.valueOf(chequeBanco);

            binding.userName.setText("Olá, " +  nome.toLowerCase());
            binding.saldoConta.setText("R$ " + saldoString);
            binding.chequeEspecialConta.setText(chequeString);

        } catch (Exception e){
            e.printStackTrace();
        } finally {
            controllerBancoDados.close();
        }



        binding.btnDepositar.setOnClickListener(v -> {
            controllerBancoDados.open();

            String valorCliente = binding.hintUserValor.getText().toString();

            if(!valorCliente.isEmpty()){
                try {

                    Double cheque = controllerBancoDados.getChequeByTitular(email);
                    Double valorSaldo = controllerBancoDados.getSaldoByTitular(email);

                    Double novoSaldo = Double.parseDouble(valorCliente) + valorSaldo ;
                    Double novoCheque = cheque + Double.parseDouble(valorCliente);

                    controllerBancoDados.updateSaldo(email, novoSaldo);
                    binding.saldoConta.setText(String.valueOf(novoSaldo));

                    if(valorSaldo < 0){
                        controllerBancoDados.updateCheque(email, novoCheque);
                        binding.chequeEspecialConta.setText(String.valueOf(novoCheque));
                    }

                }catch (Exception e){
                    e.printStackTrace();
                } finally {
                    controllerBancoDados.close();
                    binding.hintUserValor.setText("");
                }
            }

        });

        binding.btnSacar.setOnClickListener(v -> {
            controllerBancoDados.open();

            String valorCliente = binding.hintUserValor.getText().toString();

            if(!valorCliente.isEmpty()){
                try {

                    Double saldo = controllerBancoDados.getSaldoByTitular(email);
                    Double cheque = controllerBancoDados.getChequeByTitular(email);


                    Double novoSaldo = saldo - Double.parseDouble(valorCliente) ;
                    Double novoCheque = cheque - Double.parseDouble(valorCliente);


                    if(saldo > 0 && novoSaldo < 0 ){
                        AlertDialog.Builder builder = new AlertDialog.Builder(this);
                        builder.setTitle("BANCO DIP");
                        builder.setMessage("Saldo insuficiente! Insira um valor valido");
                        builder.setPositiveButton("ok", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                // nada aqui
                            }
                        });

                        AlertDialog alerta = builder.create();
                        alerta.show();

                    } else if(cheque > 0){
                        controllerBancoDados.updateSaldo(email, novoSaldo);
                        binding.saldoConta.setText(String.valueOf(novoSaldo));

                    } else{
                        AlertDialog.Builder builder = new AlertDialog.Builder(this);
                        builder.setTitle("BANCO DIP");
                        builder.setMessage("Você esta sem limite do cheque especial");
                        builder.setPositiveButton("ok", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                // nada aqui
                            }
                        });

                        AlertDialog alerta = builder.create();
                        alerta.show();
                    }

                    if(saldo <= 0 && cheque > 0){
                        controllerBancoDados.updateCheque(email, novoCheque);
                        binding.chequeEspecialConta.setText(String.valueOf(novoCheque));

                    }


                }catch (Exception e){
                    e.printStackTrace();
                } finally {
                    controllerBancoDados.close();
                    binding.hintUserValor.setText("");
                }
            }










        });

        binding.btnTransferir.setOnClickListener(v -> {
            startActivity(intentTrans);
        });

    }
}