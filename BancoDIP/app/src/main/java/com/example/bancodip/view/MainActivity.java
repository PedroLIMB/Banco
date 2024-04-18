package com.example.bancodip.view;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
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

                    controllerBancoDados.updateSaldo(nome, String.valueOf(novoSaldo));

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

            if(!valorCliente.isEmpty()){
                try {

                    Double valorSaldo = controllerBancoDados.getSaldoByTitular(nome);
                    Double novoSaldo = valorSaldo - Double.parseDouble(valorCliente) ;

                    controllerBancoDados.updateSaldo(nome, String.valueOf(novoSaldo));

                    binding.saldoConta.setText(String.valueOf(novoSaldo));


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