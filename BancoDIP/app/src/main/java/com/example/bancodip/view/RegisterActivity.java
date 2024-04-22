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

        controllerBancoDados = new ControllerBancoDados(this);
        Intent intent = new Intent(RegisterActivity.this, MainActivity.class);

        binding.btnCriarConta.setOnClickListener(v -> {
            controllerBancoDados.open();

            String  nome = binding.hintTxtRegisterNome.getText().toString().toUpperCase().trim();
            String email = binding.hintTxtRegisterEmail.getText().toString().toUpperCase().trim();
            String saldo = binding.hintTxtRegisterSaldo.getText().toString().trim();

            if(!nome.isEmpty() && !email.isEmpty() && !saldo.isEmpty() && !controllerBancoDados.isEmailInDatabase(email)){

                double saldoDouble = Double.parseDouble(saldo);
                double chequeEspecial = saldoDouble * 4;

                try {
                    controllerBancoDados.insertData(nome, email, saldoDouble, chequeEspecial, chequeEspecial);
                    intent.putExtra("nome", nome);
                    intent.putExtra("email", email);
                    intent.putExtra("saldo", saldoDouble);
                    intent.putExtra("cheque", chequeEspecial);

                }catch (Exception e){
                    e.printStackTrace();
                } finally {
                    controllerBancoDados.close();
                    startActivity(intent);
                    finish();
                }

            } else {
                Toast.makeText(getApplicationContext(), "Erro", Toast.LENGTH_LONG).show();
            }





        });




    }
}