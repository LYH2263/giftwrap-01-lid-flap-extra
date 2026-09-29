from app.db import connect

def _has_column(c, table, column):
    return any(r["name"] == column for r in c.execute(f"PRAGMA table_info({table})").fetchall())

def init_db():
    c = connect()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS boxes(id INTEGER PRIMARY KEY,name TEXT,length REAL,width REAL,height REAL,data_quality TEXT,note TEXT,flap_m REAL NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS papers(id INTEGER PRIMARY KEY,name TEXT,roll_width REAL,data_quality TEXT,note TEXT);
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
    CREATE TABLE IF NOT EXISTS calc_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,box_id INT,overlap REAL,result_json TEXT,note TEXT,created_at TEXT);
    """)
    if not _has_column(c, "boxes", "flap_m"):
        c.execute("ALTER TABLE boxes ADD COLUMN flap_m REAL NOT NULL DEFAULT 0")
    if c.execute("SELECT COUNT(*) c FROM boxes").fetchone()["c"] == 0:
        c.executemany("INSERT INTO boxes(name,length,width,height,data_quality,note,flap_m) VALUES (?,?,?,?,?,?,?)",[
            ("书型盒",0.30,0.20,0.15,"clean","",0.0),
            ("方形礼盒",0.25,0.25,0.10,"clean","",0.0),
            ("脏数据-负高",0.2,0.2,-0.1,"dirty","高度负",0.0),
        ])
        c.executemany("INSERT INTO papers(name,roll_width,data_quality,note) VALUES (?,?,?,?)",[
            ("哑光纸1.0m",1.0,"clean",""),
            ("牛皮纸0.7m",0.7,"clean",""),
        ])
        c.execute("INSERT INTO settings(key,value) VALUES ('overlap','1.15')")
    c.commit()
    c.close()
