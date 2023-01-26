import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from students.models import Student, Course
from model_bakery import baker



@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_first_course(client, course_factory):
    first_course = course_factory()
    url = reverse(viewname='courses-detail', args=(first_course.id,))
    response = client.get(url)
    response_json = response.json()

    assert response.status_code == 200
    assert first_course.name == response_json['name']


@pytest.mark.django_db
def test_courses(client, course_factory):
    course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 10

@pytest.mark.django_db
def test_courses_id_filter(client, course_factory):
    course_factory(_quantity=10)
    url = reverse('courses-list')
    last_course = Course.objects.last()
    id = last_course.id
    response = client.get(url, data={'id': id})
    response_json = response.json()

    assert response.status_code == 200
    assert response_json[0]['id'] == id

@pytest.mark.django_db
def test_courses_name_filter(client, course_factory):
    course_factory(_quantity=10)
    url = reverse('courses-list')
    last_course = Course.objects.last()
    last_course.name = 'Python'
    last_course.save()
    response = client.get(url, data={'name': last_course.name})
    response_json = response.json()

    assert response.status_code == 200
    assert response_json[0]['name'] == last_course.name


@pytest.mark.django_db
def test_courses_create(client):
    url = reverse('courses-list')
    name = 'Python'
    response = client.post(url, data={'name': name})
    response_json = response.json()

    assert response.status_code == 201
    assert response_json['name'] == name

@pytest.mark.django_db
def test_courses_update(client, course_factory):
    course = course_factory(name='Python')
    course_id = course.id
    new_name = 'Changed'
    data = {'name': new_name}
    url = reverse('courses-detail', args=(course_id,))
    response = client.put(url, data=data)
    new_course = Course.objects.get(id=course_id)

    assert response.status_code == 200
    assert new_course.name == new_name

@pytest.mark.django_db
def test_courses_delete(client, course_factory):
    course = course_factory(name='Python')
    url = reverse('courses-detail', args=(course.id,))
    response = client.delete(url)

    assert response.status_code == 204
