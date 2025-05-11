package com.anomaly;

public class Transaction {
    private String transaction_id;
    private String account_id;
    private double amount;

    public String getTransactionId() { return transaction_id; }
    public void setTransactionId(String transaction_id) { this.transaction_id = transaction_id; }

    public String getAccountId() { return account_id; }
    public void setAccountId(String account_id) { this.account_id = account_id; }

    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
} 