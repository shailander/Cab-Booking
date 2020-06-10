def query_validate_credentials(dict, table_name) :
    query = f"SELECT name FROM {table_name} WHERE username='{dict['username']}'" \
                f" AND password='{dict['password']}' AND active = 1 "
    return query

def query_get_id(dict, table_name):
    query = f"SELECT id FROM {table_name} WHERE username='{dict['username']}'" \
                f" AND password='{dict['password']}' "
    return query

def query_insert_cab_details(dict):
    query = f"INSERT INTO cab_details ('cab_number','seat_capacity','seat_available','route'," \
                    f"'timing') VALUES ('{dict['cab_number']}','{dict['seat_capacity']}'," \
                    f"'{dict['seat_available']}','{dict['route']}','{dict['timing']}')"
    return query

def query_update_details(id, item, table_name):
    query = f"UPDATE '{table_name}' SET '{item[0]}' = '{item[1]}' WHERE id = '{id}'"
    return query

def query_validate_record_existence(id, table_name):
    query = f"SELECT * FROM {table_name} WHERE id={id}"
    return query

def query_create_employee_record(dict):
    query = f"INSERT INTO employee_details ('name','username','password')" \
                    f"VALUES ('{dict['name']}','{dict['username']}','{dict['password']}')"
    return query

def query_validate_employee_existence(id):
    query = f"SELECT * FROM employee_details WHERE id = {id} AND active = 1"
    return query

def query_find_cab(source, destination):
    query = f"""SELECT id,cab_number,seat_available,route,timing FROM cab_details
                        WHERE route LIKE '%{source}%' AND route LIKE '%{destination}%'
                        AND seat_available > 0
                    """
    return query

def query_get_seat_availability(id):
    query = f"""SELECT seat_available FROM cab_details
                        WHERE id = '{id}'"""
    return query

def query_update_seat_availability(id, seat_count_updated):
    query = f"""UPDATE cab_details SET seat_available = '{seat_count_updated}'
                        WHERE id = '{id}'"""
    return query

def query_insert_travel_log(dict):
    query = f"""INSERT INTO travel_log ('employee_id','cab_id','trip_date','source',
                        'destination','timing','status') VALUES ('{dict['emp_id']}','{dict['cab_id']}',
                        '{dict['trip_date']}','{dict['source']}','{dict['destination']}',
                        '{dict['timing']}','{dict['status']}')"""
    return query

def query_find_travel_time(loc1, loc2):
    query = f"""SELECT time FROM trip_time WHERE
                        source LIKE '{loc1}' AND destination LIKE '{loc2}' OR
                        source LIKE '{loc2}' AND destination LIKE '{loc1}'"""
    return query

def query_get_travel_history(id):
    query = f"""SELECT cab_number,trip_date,x.timing,source,destination,status 
                        FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                        WHERE employee_id = '{id}'"""
    return query

def query_update_ride_status(id, prev_status, current_status):
    query = f"""UPDATE travel_log SET status = '{current_status}' WHERE
                        id = '{id}' AND status LIKE '{prev_status}'"""
    return query

def query_already_booked_status(id):
    query = f"""SELECT * FROM travel_log WHERE employee_id = '{id}' AND
                        status LIKE 'upcoming' OR status LIKE 'started'"""
    return query

def query_get_trip_specifc_info(id, info):
    query = f"""SELECT {info} FROM travel_log WHERE employee_id='{id}' 
                        AND status LIKE 'upcoming'"""
    return query

def query_check_cancelled_status(booking_id):
    query = f"""SELECT * FROM travel_log WHERE id='{booking_id}' AND status LIKE 'cancelled'"""
    return query

def query_get_record_datewise(date):
    query = f"""SELECT employee_id,cab_number,trip_date,x.timing,source,destination,status 
                        FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                        WHERE x.trip_date = '{date}'"""
    return query

def query_get_record_weekwise(date, week_list):
    query = f"""SELECT employee_id,trip_date,x.timing,source,destination,status 
                FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                WHERE SUBSTR(trip_date,4,7) LIKE '{date}' AND SUBSTR(trip_date,1,2) IN {week_list}"""
    return query

def query_get_record_monthwise(date):
    query = f"""SELECT employee_id,cab_number,trip_date,x.timing,source,destination,status 
                                        FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                                        WHERE SUBSTR(trip_date,4,7) LIKE '{date}'"""
    return query




