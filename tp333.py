import sqlite3

def delete_table(table_name):
    conn = sqlite3.connect("otp_database.db")
    cursor = conn.cursor()

    # Drop the specified table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    print(f"Table {table_name} deleted.")

    # Commit and close
    conn.commit()
    conn.close()

# Call the function to delete the otp_data table
delete_table('users')