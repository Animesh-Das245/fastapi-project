from typing import List

import pytest
from app import schemas , models

#simple change
def test_get_all_posts(authorised_client,test_posts):
    res = authorised_client.get("/posts")

    def validate_post(post):

        return schemas.PostOut(**post)
    
    post_map = map(validate_post,res.json())

    assert res.status_code == 200



def test_unauthorised_get_all_posts(client,test_posts):

    res = client.get("/posts")

    assert res.status_code == 401



def test_unauthorised_get_one_posts(client,test_posts):

    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_one_post_not_exist(authorised_client,test_posts):
    res = authorised_client.get("/posts/9999999")

    assert res.status_code == 404


def test_get_one_post(authorised_client,test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorised_client, test_user, test_posts, title, content, published):
    res = authorised_client.post('/posts',json={"title":title,"content":content,"published":published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorised_client, test_user, test_posts):
    res = authorised_client.post('/posts',json={"title":"default title","content":"default content"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "default title"
    assert created_post.content == "default content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
    

def test_unauthorised_create_one_posts(client,test_posts):

    res = client.post(f"/posts/",json={"title":"random","content":"random"})
    
    assert res.status_code == 401

def test_unauthorised_user_delete_Post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_delete_post_success(authorised_client, test_user, test_posts):
    res = authorised_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorised_client, test_user, test_posts):
    res = authorised_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorised_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorised_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorised_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorised_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorised_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorised_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorised_client.put(
        "/posts/8000000", json=data)
    assert res.status_code == 404