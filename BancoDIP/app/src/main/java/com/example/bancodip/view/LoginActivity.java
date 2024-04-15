package com.example.bancodip.view;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;

import com.example.bancodip.R;
import com.example.bancodip.controller.ControllerBancoDados;
import com.example.bancodip.databinding.ActivityLoginBinding;

public class LoginActivity extends AppCompatActivity {

    private ActivityLoginBinding binding;
    private ControllerBancoDados controllerBancoDados;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityLoginBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        Intent intentRegister = new Intent(LoginActivity.this, RegisterActivity.class);
        Intent intentMain = new Intent(LoginActivity.this, MainActivity.class);


        binding.btnCriarContaLogin.setOnClickListener(v -> {
            startActivity(intentRegister);
        });

        binding.btnEntrarConta.setOnClickListener(v -> {

        });



    }
}