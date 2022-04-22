# import psycopg2
# from fastapi import HTTPException, status, Response
# from psycopg2.extras import RealDictCursor
# from config import settings

# try:
#     # RealDictCursor displays the names of the columns in the db table
#     conn = psycopg2.connect(host=settings.database_host, database=settings.database_name,
#                             user=settings.database_user, cursor_factory=RealDictCursor, password=settings.database_password)
#     cursor = conn.cursor()
#     print("Connected to database successfully")
# except Exception as e:
#     print("Error: ", e)


# def get_posts():
#     cursor.execute(""" SELECT * FROM fastapi """)
#     posts = cursor.fetchall()
#     return posts

# def get_post(id: int):
#     cursor.execute(""" SELECT * FROM fastapi where id = %s """, (str(id)))
#     post = cursor.fetchone()
#     return post
# def create_post(post):
#     cursor.execute(
#         f""" INSERT INTO fastapi (title, content) VALUES ('{post.get('title')}', '{post.get('content')}') """)
#     conn.commit()

# def delete_post(id: int):
#     cursor.execute(""" DELETE FROM fastapi WHERE id = '{0}' RETURNING *""".format(str(id)))
#     deleted = cursor.fetchone()
#     conn.commit()

#     if deleted == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find post with id {id}")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# def update_post(id, post):
#     cursor.execute(""" UPDATE  fastapi SET title='{1}', content='{2}' WHERE id = {0} RETURNING *""".format(str(id),post.get('title'), post.get('content')))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     return updated_post