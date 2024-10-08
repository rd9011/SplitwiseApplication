> **_NOTE:_**
In alignment with our use of the RDS Postgres managed service, we have developed all necessary models and successfully migrated the tables to our sample RDS database.
This documents showcases the database schema of this application that has been migrated

## 1. Users Table

```psql
                                 Table "public.splitwisemtv_user"
    Column     |          Type          | Collation | Nullable |             Default              
---------------+------------------------+-----------+----------+----------------------------------
 userid        | integer                |           | not null | generated by default as identity
 name          | character varying(255) |           | not null | 
 email         | character varying(254) |           | not null | 
 mobile_number | character varying(15)  |           | not null | 
Indexes:
    "splitwisemtv_user_pkey" PRIMARY KEY, btree (userid)
    "splitwisemtv_user_email_090c5e87_like" btree (email varchar_pattern_ops)
    "splitwisemtv_user_email_key" UNIQUE CONSTRAINT, btree (email)
    "splitwisemtv_user_mobile_number_e0938527_like" btree (mobile_number varchar_pattern_ops)
    "splitwisemtv_user_mobile_number_key" UNIQUE CONSTRAINT, btree (mobile_number)
Referenced by:
    TABLE "splitwisemtv_balance" CONSTRAINT "splitwisemtv_balance_from_user_id_60ab6f06_fk_splitwise" FOREIGN KEY (from_user_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
    TABLE "splitwisemtv_balance" CONSTRAINT "splitwisemtv_balance_to_user_id_69202428_fk_splitwise" FOREIGN KEY (to_user_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
    TABLE "splitwisemtv_expense" CONSTRAINT "splitwisemtv_expense_paid_by_id_7ae3471f_fk_splitwise" FOREIGN KEY (paid_by_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
    TABLE "splitwisemtv_expenseshare" CONSTRAINT "splitwisemtv_expense_user_id_3122f345_fk_splitwise" FOREIGN KEY (user_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
```

## 2. Expense Table

```psql
                                Table "public.splitwisemtv_expense"
    Column    |           Type           | Collation | Nullable |             Default              
--------------+--------------------------+-----------+----------+----------------------------------
 expenseid    | integer                  |           | not null | generated by default as identity
 amount       | numeric(10,2)            |           | not null | 
 split_type   | character varying(10)    |           | not null | 
 description  | text                     |           | not null | 
 created_at   | timestamp with time zone |           | not null | 
 paid_by_id   | integer                  |           | not null | 
 split_values | jsonb                    |           |          | 
Indexes:
    "splitwisemtv_expense_pkey" PRIMARY KEY, btree (expenseid)
    "splitwisemtv_expense_paid_by_id_7ae3471f" btree (paid_by_id)
Foreign-key constraints:
    "splitwisemtv_expense_paid_by_id_7ae3471f_fk_splitwise" FOREIGN KEY (paid_by_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
Referenced by:
    TABLE "splitwisemtv_expenseshare" CONSTRAINT "splitwisemtv_expense_expense_id_dfabf616_fk_splitwise" FOREIGN KEY (expense_id) REFERENCES splitwisemtv_expense(expenseid) DEFERRABLE INITIALLY DEFERRED
```

## 3. Balance Table

```psql
                          Table "public.splitwisemtv_balance"
    Column    |     Type      | Collation | Nullable |             Default              
--------------+---------------+-----------+----------+----------------------------------
 balanceid    | integer       |           | not null | generated by default as identity
 amount       | numeric(10,2) |           | not null | 
 from_user_id | integer       |           | not null | 
 to_user_id   | integer       |           | not null | 
Indexes:
    "splitwisemtv_balance_pkey" PRIMARY KEY, btree (balanceid)
    "splitwisemtv_balance_from_user_id_60ab6f06" btree (from_user_id)
    "splitwisemtv_balance_to_user_id_69202428" btree (to_user_id)
Foreign-key constraints:
    "splitwisemtv_balance_from_user_id_60ab6f06_fk_splitwise" FOREIGN KEY (from_user_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
    "splitwisemtv_balance_to_user_id_69202428_fk_splitwise" FOREIGN KEY (to_user_id) REFERENCES splitwisemtv_user(userid) DEFERRABLE INITIALLY DEFERRED
```