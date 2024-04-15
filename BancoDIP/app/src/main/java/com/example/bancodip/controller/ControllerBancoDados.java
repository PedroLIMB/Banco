package com.example.bancodip.controller;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;

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

    public long insertData(String name, String email, String saldo) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(ModelBancoDados.COLUNA_TITULAR, name);
        contentValues.put(ModelBancoDados.COLUNA_SALDO, saldo);
        contentValues.put(ModelBancoDados.COLUNA_EMAIL, email);
        return database.insert(ModelBancoDados.NOME_TABELA, null, contentValues);
    }

    public int updateSaldo(String titular, String newSaldo) {
        ContentValues contentValues = new ContentValues();
        contentValues.put(ModelBancoDados.COLUNA_SALDO, newSaldo);
        String whereClause = ModelBancoDados.COLUNA_TITULAR + " = ?";
        String[] whereArgs = {titular};
        return database.update(ModelBancoDados.NOME_TABELA, contentValues, whereClause, whereArgs);
    }


    public Cursor getAllData() {
        return database.query(ModelBancoDados.NOME_TABELA,
                new String[]{ModelBancoDados.COLUNA_ID, ModelBancoDados.COLUNA_TITULAR, ModelBancoDados.COLUNA_SALDO, ModelBancoDados.COLUNA_EMAIL},
                null, null, null, null, null);
    }




}
