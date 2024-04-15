package com.example.bancodip.model;

public class DadosUser {

    private String titular;
    private String email;
    private Double saldo;


    public DadosUser(String titular, String email, Double saldo){
        this.titular = titular;
        this.email = email;
        this.saldo = saldo;
    }

    public DadosUser(String titular, String email){
        this.titular = titular;
        this.email = email;
    }

    public String getTitular() {
        return titular;
    }

    public void setTitular(String titular) {
        this.titular = titular;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Double getSaldo() {
        return saldo;
    }

    public void setSaldo(Double saldo) {
        this.saldo = saldo;
    }
}
