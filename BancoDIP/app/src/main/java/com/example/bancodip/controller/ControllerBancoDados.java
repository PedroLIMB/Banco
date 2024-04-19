package com.example.bancodip.controller;

import android.annotation.SuppressLint;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import com.example.bancodip.model.ModelBancoDados;

public class ControllerBancoDados {

    private ModelBancoDados dbHelper;
    private final Context context;
    private SQLiteDatabase database;

    public ControllerBancoDados(Context context) {
        this.context = context;
    }

    public ControllerBancoDados open() throws SQLException {
        dbHelper = new ModelBancoDados(context);
        database = dbHelper.getWritableDatabase();
        return this;
    }

    public void close() {
        dbHelper.close();
    }

    public long insertData(String name, String email, double saldo, double chequeEspecial) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(ModelBancoDados.COLUNA_TITULAR, name);
        contentValues.put(ModelBancoDados.COLUNA_EMAIL, email);
        contentValues.put(ModelBancoDados.COLUNA_SALDO, saldo);
        contentValues.put(ModelBancoDados.COLUNA_CHEQUE_ESPECIAL, chequeEspecial);

        long result = -1; // Inicializa o resultado como -1, indicando falha na inserção

        try {
            result = database.insertOrThrow(ModelBancoDados.NOME_TABELA, null, contentValues);
            Log.d("INSERT_DATA", "Inserção bem-sucedida. ID do novo registro: " + result);
        } catch (SQLException e) {
            Log.e("INSERT_DATA", "Erro ao inserir dados: " + e.getMessage());
        }

        return result;
    }



    public void updateSaldo(String titular, String newSaldo) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(ModelBancoDados.COLUNA_SALDO, newSaldo);
        String whereClause = ModelBancoDados.COLUNA_TITULAR + " = ?";
        String[] whereArgs = {titular};
        database.update(ModelBancoDados.NOME_TABELA, contentValues, whereClause, whereArgs);
    }

    public int updateCheque(String titular, String newCheque) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(ModelBancoDados.COLUNA_CHEQUE_ESPECIAL, newCheque);
        String whereClause = ModelBancoDados.COLUNA_TITULAR + " = ?";
        String[] whereArgs = {titular};
        return database.update(ModelBancoDados.NOME_TABELA, contentValues, whereClause, whereArgs);
    }


    public Cursor getAllData() {
        return database.query(ModelBancoDados.NOME_TABELA,
                new String[]{ModelBancoDados.COLUNA_ID, ModelBancoDados.COLUNA_TITULAR, ModelBancoDados.COLUNA_SALDO, ModelBancoDados.COLUNA_EMAIL},
                null, null, null, null, null);
    }

    public Double getSaldoByTitular(String titular) {
        try {
            Cursor cursor = database.query(ModelBancoDados.NOME_TABELA,
                    new String[]{ModelBancoDados.COLUNA_SALDO},
                    ModelBancoDados.COLUNA_TITULAR + " = ?",
                    new String[]{titular},
                    null, null, null);

            Double saldo = 0.0;
            if (cursor != null && cursor.moveToFirst()) {
                int saldoIndex = cursor.getColumnIndex(ModelBancoDados.COLUNA_SALDO);
                saldo = cursor.getDouble(saldoIndex);
            }
            if (cursor != null) {
                cursor.close();
            }
            return saldo;
        } catch (Exception e) {
            e.printStackTrace();
            return 0.0; // ou algum outro valor de erro
        }
    }

    public Double getChequeByTitular(String titular) {
        try {
            Cursor cursor = database.query(ModelBancoDados.NOME_TABELA,
                    new String[]{ModelBancoDados.COLUNA_CHEQUE_ESPECIAL},
                    ModelBancoDados.COLUNA_TITULAR + " = ?",
                    new String[]{titular},
                    null, null, null);

            Double cheque = 0.0;
            if (cursor != null && cursor.moveToFirst()) {
                int chequeIndex = cursor.getColumnIndex(ModelBancoDados.COLUNA_CHEQUE_ESPECIAL);
                if (!cursor.isNull(chequeIndex)) {
                    cheque = cursor.getDouble(chequeIndex);
                }
            }
            if (cursor != null) {
                cursor.close();
            }
            return cheque;
        } catch (Exception e) {
            e.printStackTrace();
            return 0.0; // ou algum outro valor de erro
        }
    }



    public boolean isEmailInDatabase(String emailToCheck) {
        Cursor cursor = database.query(
                ModelBancoDados.NOME_TABELA,
                new String[]{ModelBancoDados.COLUNA_EMAIL},
                null, null, null, null, null
        );

        if (cursor != null && cursor.moveToFirst()) {
            do {
                @SuppressLint("Range") String email = cursor.getString(cursor.getColumnIndex(ModelBancoDados.COLUNA_EMAIL));
                if (emailToCheck.equals(email)) {

                    cursor.close();
                    return true;
                }
            } while (cursor.moveToNext());

            cursor.close();
        }

        return false;
    }

    public boolean isNomeInDatabase(String nameToCheck) {
        Cursor cursor = database.query(
                ModelBancoDados.NOME_TABELA,
                new String[]{ModelBancoDados.COLUNA_TITULAR},
                null, null, null, null, null
        );

        if (cursor != null && cursor.moveToFirst()) {
            do {
                @SuppressLint("Range") String nome = cursor.getString(cursor.getColumnIndex(ModelBancoDados.COLUNA_TITULAR));
                if (nameToCheck.equals(nome)) {

                    cursor.close();
                    return true;
                }
            } while (cursor.moveToNext());

            cursor.close();
        }

        return false;
    }



}
