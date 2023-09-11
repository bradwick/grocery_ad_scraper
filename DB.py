import sqlite3


class DB:
    def __init__(self):
        self.con = sqlite3.connect("/db/grocery.db")
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

        if not self.deal_table_exists():
            self.create_deal_table()

    def get_existing_deals(self):
        sql = '''
        SELECT * from deals
        WHERE hide != TRUE
        AND current = TRUE
        ORDER BY favorite DESC
        '''

        return self.cur.execute(sql).fetchall()

    def get_next_visible_deal_id(self, id):
        sql = '''
        SELECT id from deals
        WHERE hide != TRUE
        AND current = TRUE
        AND favorite != TRUE
        AND id > ?
        ORDER BY id
        LIMIT 1
        '''

        return self.cur.execute(sql, (id,)).fetchone()

    def get_saved_deals(self):
        sql = '''
        SELECT * from deals
        WHERE save = TRUE
        ORDER BY favorite DESC
        '''

        return self.cur.execute(sql).fetchall()

    def get_latest_timestamp(self):
        sql='''
        SELECT time
        FROM deals
        ORDER BY time DESC
        LIMIT 1
        '''

        return self.cur.execute(sql).fetchone()

    def insert(self, store, item, price):
        sql = '''
        INSERT INTO deals(store, item, price, current) 
        VALUES (?,?,?,?)

        ON CONFLICT(store, item) DO 
        UPDATE SET current=TRUE, price=?;
        '''

        self.cur.execute(sql, (store, item, price, True, price))
        self.con.commit()

    def manual_add(self, item):
        sql = '''
        INSERT INTO deals(store, item, price, current) 
        VALUES (?,?,?,?)

        ON CONFLICT(store, item) DO 
        UPDATE SET current=TRUE, price=?, save=TRUE
        '''

        self.cur.execute(sql, ("", item, "", True, ""))
        self.con.commit()


    def clean_old_deals(self):
        sql = '''
        DELETE FROM deals
        WHERE favorite = FALSE
        AND hide = FALSE
        AND save = FALSE    
        '''

        self.cur.execute(sql)
        self.con.commit()

        sql = '''
        UPDATE deals
        SET current = FALSE
        WHERE id > 0
        '''

        self.cur.execute(sql)
        self.con.commit()

    def toggle_favorite(self, id):
        sql = '''
        UPDATE deals
        SET favorite = NOT favorite
        WHERE id = ?
        '''

        self.cur.execute(sql, (id,))
        self.con.commit()

    def toggle_save(self, id):
        sql = '''
        UPDATE deals
        SET save = NOT save
        WHERE id = ?
        '''

        self.cur.execute(sql, (id,))
        self.con.commit()

    def toggle_hide(self, id):
        sql = '''
        UPDATE deals
        SET hide = NOT hide
        WHERE id = ?
        '''

        self.cur.execute(sql, (id,))
        self.con.commit()

    def create_deal_table(self):
        sql = '''
        create table deals
        (
            id    integer /*autoincrement needs PK*/,
            store TEXT not null,
            item  TEXT not null,
            price TEXT not null,
            favorite INT default FALSE,
            hide INT default FALSE,
            save INT default FALSE,
            current INT default FALSE,
            time ANY, 
            
            UNIQUE(store, item),
            
            constraint deals_pk
                primary key (id)
        );
        '''
        self.cur.execute(sql)
        sql='''
        CREATE TRIGGER [UPDATE_DT]
            AFTER UPDATE ON deals FOR EACH ROW
            WHEN OLD.time = NEW.time OR OLD.time IS NULL
        BEGIN
            UPDATE deals SET time=CURRENT_TIMESTAMP WHERE id=NEW.id;
        END;
        '''
        self.cur.execute(sql)

    def deal_table_exists(self):
        sql = '''
        SELECT name FROM sqlite_master 
        WHERE type='table'
        AND name='deals';
        '''

        tables = self.cur.execute(sql).fetchall()

        if len(tables) == 0:
            return False
        else:
            return True
