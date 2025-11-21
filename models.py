from database import get_connection

def find_owner_by_plate(plate):
    conn=get_connection(); c=conn.cursor()
    c.execute("SELECT owners.name, owners.phone, owners.email, vehicles.brand, vehicles.model, vehicles.year FROM vehicles JOIN owners ON vehicles.owner_id=owners.id WHERE UPPER(vehicles.plate)=UPPER(?)",(plate,))
    r=c.fetchone(); conn.close()
    if not r: return None
    return {"owner_name":r["name"],"owner_phone":r["phone"],"owner_email":r["email"],"vehicle_brand":r["brand"],"vehicle_model":r["model"],"vehicle_year":r["year"]}

def create_owner_vehicle(name,phone,email,plate,brand,model,year):
    conn=get_connection(); c=conn.cursor()
    c.execute("INSERT INTO owners (name,phone,email) VALUES (?,?,?)",(name,phone,email))
    oid=c.lastrowid
    c.execute("INSERT INTO vehicles (plate,brand,model,year,owner_id) VALUES (?,?,?,?,?)",(plate.upper(),brand,model,year,oid))
    conn.commit(); conn.close()
    return {"owner_id":oid}
