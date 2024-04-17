package com.example.bancodip.view;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

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

        controllerBancoDados = new ControllerBancoDados(this);

        binding.btnCriarContaLogin.setOnClickListener(v -> {
            startActivity(intentRegister);
        });

        binding.btnEntrarConta.setOnClickListener(v -> {
            controllerBancoDados.open();

            String nome = binding.hintTxtNomeLogin.getText().toString().trim();
            String email = binding.hintTxtEmail.getText().toString().trim();


            if (controllerBancoDados.isNomeInDatabase(nome) && controllerBancoDados.isEmailInDatabase(email)){

                try {
                    intentMain.putExtra("nome", nome);
                    intentMain.putExtra("email", email);
                }catch (Exception e){
                    e.printStackTrace();
                }

                startActivity(intentMain);
                finish();

            }else {
                Toast.makeText(getApplicationContext(), "Erro", Toast.LENGTH_LONG).show();
            }

        });



    }
}