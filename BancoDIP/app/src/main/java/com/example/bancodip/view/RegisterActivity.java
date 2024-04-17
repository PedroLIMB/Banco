package com.example.bancodip.view;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import com.example.bancodip.R;
import com.example.bancodip.controller.ControllerBancoDados;
import com.example.bancodip.databinding.ActivityRegisterBinding;

import java.util.Locale;

public class RegisterActivity extends AppCompatActivity {

    private ActivityRegisterBinding binding;
    private ControllerBancoDados controllerBancoDados;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityRegisterBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        Intent intentRegister = new Intent(RegisterActivity.this, MainActivity.class);
        ControllerBancoDados controllerBancoDados = new ControllerBancoDados(this);

        binding.btnCriarConta.setOnClickListener(v ->{
            controllerBancoDados.open();

            String nome = binding.hintTxtRegisterNome.getText().toString().trim().toUpperCase();
            String email = binding.hintTxtRegisterEmail.getText().toString().trim().toUpperCase();
            String saldo = binding.hintTxtRegisterSaldo.getText().toString().trim();

            if(!nome.isEmpty() && !email.isEmpty() &&!saldo.isEmpty() && !controllerBancoDados.isEmailInDatabase(email)){
                try {
                    Double saldoDouble = Double.parseDouble(saldo);

                    controllerBancoDados.insertData(nome, email, saldoDouble);

                    intentRegister.putExtra("nome", nome);
                    intentRegister.putExtra("email", email);
                    intentRegister.putExtra("saldo", saldoDouble);

                    startActivity(intentRegister);
                    finish();

                }catch (Exception e){
                    e.printStackTrace();
                } finally {
                    controllerBancoDados.close();
                }
            } else {
                Toast.makeText(getApplicationContext(), "Erro! email repetido ou um dos campos está vazio", Toast.LENGTH_LONG).show();
            }
        });


    }
}