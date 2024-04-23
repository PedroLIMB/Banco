package com.example.bancodip.view;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

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

        binding.btnTransferirUser.setOnClickListener(v -> {
            String emailUser = binding.transUserEmail.getText().toString();
            String valorUser = binding.transUserValor.getText().toString();

            Double saldo = controllerBancoDados.getSaldoByTitular()

            if(controllerBancoDados.isEmailInDatabase(emailUser) && ){

            }


        });

        binding.btnVoltar.setOnClickListener(v -> {
            finish();

        });

    }
}