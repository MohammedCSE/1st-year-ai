import mysql.connector


def save_claim(customer_name, claim_type, claim_amount, status):

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        database="insurance_claims"
    )

    cursor = connection.cursor()

    query = """
        INSERT INTO claims
        (customer_name, claim_type, claim_amount, status)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        customer_name,
        claim_type,
        claim_amount,
        status
    )


    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Claim saved to MySQL!")

