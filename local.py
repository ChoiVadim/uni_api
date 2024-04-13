import requests

res = requests.get('http://localhost:8000/courses/BIO-101')
print(res.json())

res = requests.delete('http://localhost:8000/courses/CS-50')
print(res)

data = {
    'course_id': 'CS-50',
    'title': 'Intro to Computer Science', 
    'dept_name': 'Computer Science', 
    'credits': 6
}

res = requests.post('http://localhost:8000/courses/CS-50', json=data)
print(res.json())

data = {
    'course_id': 'CS-50',
    'title': 'Intro to Computer Science', 
    'dept_name': 'Com. Sci.', 
    'credits': 3
}

res = requests.put('http://localhost:8000/courses/CS-50', json=data)
print(res.json())