from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Literal

app = Flask(__name__)
app.json.ensure_ascii = False


connection = psycopg2.connect(user="change_me",
                              password="change_me",
                              host="change_me",
                              port="change_me",
                              database="postgres", cursor_factory=RealDictCursor)
connection.autocommit = True


@app.get('/')
def hello_sirius():
    return 'Домашняя работа Ивановой Эрики по базам данных (заключительная!)'

"""Метод read, который выводит все таблицы со встроенными 
массивами (Есть таблица repo, у нее есть свои developer-ы и ticket-ы (заявки)"""
@app.get('/all')
def get_actors():
    with connection.cursor() as cursor:
        query = """
with 
  repo_with_developers as (
    select 
      r.id, 
      r.title, 
      r.descr, 
      r.stars, 
      coalesce(
        json_agg(json_build_object('developer_name', d.nickname, 'reg_date', d.reg_date))
          filter (where d.id is not null), '[]') developer_data
    from repo r
    left join repo_to_developer rd on r.id = rd.repo_id
    left join developer d on d.id = rd.developer_id
    group by r.id
),
  repos_with_tickets as (
    select 
      ra.id,
      coalesce(
        json_agg(json_build_object('title', t.name_t, 'ticket description', t.desc_t, 'status', t.stat)) 
          filter (where t.name_t is not null), '[]') tickets
    from repo ra
    left join ticket t on ra.id = t.repo_id
    group by ra.id
)
select af.id, af.title, af.descr, af.stars, af.developer_data, aa.tickets
from repo_with_developers af
join repos_with_tickets aa on af.id = aa.id

    """

        cursor.execute(query)
        all_for_r = cursor.fetchall()
        return all_for_r


@app.post('/repos/create')
def create_repo():
    body = request.json

    title = body.get('title')
    descr = body.get('descr')
    stars = body.get('stars')

    query = SQL("""
insert into repo(title, descr, stars)
values ({title}, {descr}, {stars})
returning id
""").format(
        title=Literal(title),
        descr=Literal(descr),
        stars=Literal(stars))

    with connection.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchone()

    return {"id": res['id']}


@app.post('/repos/update')
def update_repo():
    body = request.json

    id = body.get('id')
    title = body.get('title')
    descr = body.get('descr')
    stars = body.get('stars')

    query = SQL("""
update repo
set title = {title}, descr = {descr}, stars = {stars}
where id = {id}
returning id
""").format(
        title=Literal(title),
        descr=Literal(descr),
        stars=Literal(stars),
        id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(query)
        updated_repos = cursor.fetchall()

    if len(updated_repos) == 0:
        return '', 404
    else:
        return '', 204


@app.delete('/repos/delete')
def delete_repo():
    id = request.json.get('id')

    query = SQL("delete from repo where id = {id} returning id").format(
        id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(query)
        deleted_repos = cursor.fetchall()

    if len(deleted_repos) == 0:
        return '', 404
    else:
        return '', 204
