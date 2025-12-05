import sqlite3

def vider_base():
    try:
 
        with sqlite3.connect("cloudDB.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM article")
            cursor.execute("DELETE FROM tickets")
            
            conn.commit()
            print("Succès ")
            
    except Exception as e:
        print(f"Erreur : {e}")
        

if __name__ == "__main__":
    vider_base()