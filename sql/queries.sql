SELECT * FROM debtors;

SELECT id, name, amount FROM debts ORDER BY amount DESC;

SELECT * FROM debts WHERE is_paid = 0;

SELECT * FROM debts WHERE amount BETWEEN 1000 AND 10000;

SELECT debts.id, debtors.name, debts.amount 
FROM debts 
JOIN debtors ON debts.debtor_id = debtors.id;

SELECT debts.id, users.name AS creditor, debtors.name AS debtor, debts.amount
FROM debts
JOIN users ON debts.user_id = users.id
JOIN debtors ON debts.debtor_id = debtors.id;

SELECT COUNT(*) AS total_debts FROM debts;

SELECT SUM(amount) AS total_sum FROM debts WHERE is_paid = 0;

SELECT debtor_id, COUNT(*) AS debt_count FROM debts GROUP BY debtor_id;

SELECT debtor_id, SUM(amount) AS total 
FROM debts 
GROUP BY debtor_id 
HAVING SUM(amount) > 5000;