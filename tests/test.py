import main

# get_data will get a total of 3203 school entries
def test_get_data():
    result = main.get_data()
    assert len(result) == 3203


# test the database file
def test_setup_db():
    # add test data
    conn, cursor = main.open_db("testdb.sqlite")
    main.setup_db(cursor)
    test_data = [{'school.id': 'Test University', '2018.student.size': 1000, 'school.state': 'MA', 'id': 11001,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004}]
    main.insert_schools_data(test_data,cursor)
    main.close_db(conn)
    # test data is saved to see if i t is there
    conn,cursor = main.open_db('testdb.sqlite')
    cursor.execute()
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'university_%';''')  # like does pattern matching with % as the wildcard
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute(''' SELECT university_name FROM university_data''')
    results = cursor.fetchall()
    test_record = results[0]
    assert test_record[0] == 'Test University'

