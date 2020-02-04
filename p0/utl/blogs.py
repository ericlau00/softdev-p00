import sqlite3
import os
from utl import entries

__dbfile__ = os.path.dirname(os.path.abspath(__file__)) + '/../data/sitedata.db'

def init():
    db = sqlite3.connect(__dbfile__)
    db.execute('''CREATE TABLE IF NOT EXISTS blogs (
                    userid INTEGER,
                    blogid PRIMARY KEY,
                    title TEXT UNIQUE);
                ''')
    db.commit()

#create a new blog given that the title of the blog is unique, linked to user of userid
def create_blog(userid, title):
    db = sqlite3.connect(__dbfile__)
    try:    
        db.execute('INSERT INTO blogs VALUES (?,?,?);', (userid, count(), title))
        db.commit()
        return True
    except sqlite3.Error as error: # uniqueness probably
        print(error)
        return False

#deletes a blog, entries that matches the blogid
# def delete_blog(blogid):
#     db = sqlite3.connect(__dbfile__)
#     db.execute('DELETE FROM blogs, entries, entries_arc WHERE blogid=?',(blogid,))
#     db.commit()

#get the blogid, title, and user info linked to a blog.
def describe(blogid):
    db = sqlite3.connect(__dbfile__)
    try:
        query = db.execute(f'''
                SELECT blogs.blogid, blogs.title, users.userid, users.username 
                FROM blogs 
                INNER JOIN users 
                ON blogs.userid = users.userid 
                WHERE blogs.blogid = {blogid};
                ''')
        return [data for data in query][0]
    except sqlite3.Error as error:
        print(error)
        return False

#get all of the entries (and info about entry) that are linked to a blog
def read_entries(blogid):
    db = sqlite3.connect(__dbfile__)
    query = db.execute('''
                    SELECT entryid, timestamp, title, content FROM entries
                    WHERE blogid=?
                    ORDER BY entryid DESC
                    ''', (blogid,))
    elist = [item for item in query]
    for i in range(len(elist)):
        elist[i] = {
            'entryid':elist[i][0],
            'timestamp':elist[i][1],
            'title':elist[i][2],
            'content':list(elist[i])[3].split("\n"),
            'count_comments':entries.count_comments(blogid,elist[i][0])
        }
    return elist

#get all of the blogs that were created by user linked to userid
def get_user_blogs(userid):
    db = sqlite3.connect(__dbfile__)
    try:
        query = db.execute(
            '''
            SELECT blogs.blogid, blogs.title
            FROM blogs
            WHERE blogs.userid = ?
            ''', (userid,)
            )
        return [data for data in query]
    except sqlite3.Error as error:
        print(error)
        return False

#get the user that created a blog
def get_userid(blogid):
    db = sqlite3.connect(__dbfile__)
    query = db.execute(
            '''
            SELECT blogs.userid
            FROM blogs
            WHERE blogs.blogid = ?
            ''', (blogid,)
            )
    try:
        #print([data for data in query][0][0])
        return [data for data in query][0][0]
    except IndexError as error:
        return False

##SUPPLEMENTARY
#count of number of blogs
def count():
    db = sqlite3.connect(__dbfile__)
    count = db.execute('SELECT count(*) FROM blogs;')
    return [num for num in count][0][0]
