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

        try {
            controllerBancoDados.open();

            Double saldoBanco = controllerBancoDados.getSaldoByTitular(nome);
            Double chequeBanco = controllerBancoDados.getChequeByTitular(nome);
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

                    Double valorSaldo = controllerBancoDados.getSaldoByTitular(nome);
                    Double novoSaldo = Double.parseDouble(valorCliente) + valorSaldo ;

                    controllerBancoDados.updateSaldo(nome, novoSaldo);

                    binding.saldoConta.setText(String.valueOf(novoSaldo));


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
            Double saldo = controllerBancoDados.getSaldoByTitular(nome);
            Double cheque = controllerBancoDados.getChequeByTitular(nome);

            if(!valorCliente.isEmpty()){
                try {

                    Double valorSaldo = controllerBancoDados.getSaldoByTitular(nome);
                    Double novoSaldo = valorSaldo - Double.parseDouble(valorCliente) ;

                    controllerBancoDados.updateSaldo(nome, novoSaldo);
                    binding.saldoConta.setText(String.valueOf(novoSaldo));

                    if(novoSaldo < 0){
                        Double novoCheque = cheque - saldo;
                        controllerBancoDados.updateCheque(nome, novoCheque);
                        binding.chequeEspecialConta.setText(String.valueOf(novoCheque));

                    }


                }catch (Exception e){
                    e.printStackTrace();
                } finally {
                    controllerBancoDados.close();
                    binding.hintUserValor.setText("");
                }
            }



//            if(saldo - Double.parseDouble(valorCliente) < 0 && saldo >= 0){
//                controllerBancoDados.open();
//
//                AlertDialog.Builder builder = new AlertDialog.Builder(this);
//                builder.setTitle("Banco Dip");
//                builder.setMessage("Ao fazer essa ação você caiu no cheque especial!");
//                builder.setPositiveButton("ok", new DialogInterface.OnClickListener() {
//                    @Override
//                    public void onClick(DialogInterface dialog, int which) {
//                        //nada aqui
//                    }
//                });
//
//                AlertDialog alerta = builder.create();
//                alerta.show();
//
//
//
//            }
//










        });

        binding.btnTransferir.setOnClickListener(v -> {
            startActivity(intentTrans);
        });

    }
}