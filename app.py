from flask import Flask, jsonify, request

import mysql.connector
from flask_cors import CORS
from datetime import timedelta
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
Swagger(app)

db_config = {
    'user': 'objura_user',
    'password': 'root',
    'host': 'localhost',
    'database': 'objura-bdd'
}

# Route to get all users
@app.route('/api/v1/get_users', methods=['GET'])
def get_users():
    """
    Get a list of all users

    This endpoint returns a list of all users in the system.

    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              user_email:
                type: string 
              user_firstname:
                type: string
              user_lastname:
                type: string
              user_password:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM user')
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    data = []

    for row in results:
        person_data = {
            'user_email': row[0],
            'user_firstname': row[1],
            'user_lastname': row[2],
            'user_password': row[3]
        }
        data.append(person_data)

    return jsonify(data)

# Route to create a user
@app.route('/api/v1/create_user', methods=['POST'])
def create_user():
    """
    Create a new user

    This endpoint creates a new user in the system.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_email:
              type: string
            user_password:
              type: string

    responses:
      200:
        description: User created successfully
        schema:
          type: object
          properties:
            status:
              type: string
              description: Status message
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    email = request.json['email']
    password = request.json['password']

    cursor.execute('INSERT INTO user (user_email, user_password) VALUES (%s, %s)', (email, password))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        'status': 'User created successfully'
    })

# Route to get houses
@app.route('/api/v1/get_houses', methods=['GET'])
def get_houses():
    """
    Get a list of all houses

    This endpoint returns a list of all houses in the system.

    ---
    responses:
      200:
        description: A list of houses
        schema:
          type: array
          items:
            type: object
            properties:
              house_id:
                type: integer
              house_name:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM house')
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    data = []

    for row in results:
        house_data = {
            'house_id': row[0],
            'house_name': row[1]
        }
        data.append(house_data)

    return jsonify(data)

# Route to get rooms
@app.route('/api/v1/get_rooms', methods=['GET'])
def get_rooms():
    """
    Get a list of all rooms

    This endpoint returns a list of all rooms in the system.

    ---
    responses:
      200:
        description: A list of rooms
        schema:
          type: array
          items:
            type: object
            properties:
              room_id:
                type: integer
                description: The room's ID
              room_name:
                type: string
                description: The room's name
              house_id:
                type: integer
                description: The ID of the house to which the room belongs
    """

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM room')
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    data = []

    for row in results:
        room_data = {
            'room_id': row[0],
            'room_name': row[1],
            'house_id': row[2]
        }
        data.append(room_data)

    return jsonify(data)

# Route to get videos
@app.route('/api/v1/get_videos', methods=['GET'])
def get_videos():
    """
    Get a list of all videos

    This endpoint returns a list of all videos in the system.

    ---
    responses:
      200:
        description: A list of videos
        schema:
          type: array
          items:
            type: object
            properties:
              video_id:
                type: integer
              video_name:
                type: string
              room_id:
                type: integer
    """

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM video')
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    response_data = []

    for row in results:
        video_data = {
            'video_id': row[0],
            'video_name': row[1],
            'room_id': row[2]
        }
        response_data.append(video_data)

    return jsonify(response_data)

# Route to get can consult
@app.route('/api/v1/get_canconsult', methods=['GET'])
def get_can_consult():
    """
    Get a list of all consult permissions

    This endpoint returns a list of all consult permissions in the system. It includes details about the user and the house they can consult.

    ---
    responses:
      200:
        description: A list of consult permissions
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: integer
              user_firstname:
                type: string
              user_lastname:
                type: string
              house_id:
                type: integer
              house_name:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM can_consult')
    results = cursor.fetchall()

    response_data = []

    for row in results:
        user_id = row[0]
        house_id = row[1]

        # Get user_firstname and user_lastname with user_ida
        cursor.execute('SELECT user_firstname, user_lastname FROM user WHERE user_id = %s', (user_id,))
        user_results = cursor.fetchall()
        user_firstname = user_results[0][0]
        user_lastname = user_results[0][1]

        # Get house_name with house_id
        cursor.execute('SELECT house_name FROM house WHERE house_id = %s', (house_id,))
        house_results = cursor.fetchall()
        house_name = house_results[0][0]

        can_consult_data = {
            'user_id': user_id,
            'user_firstname': user_firstname,
            'user_lastname': user_lastname,
            'house_id': house_id,
            'house_name': house_name
        }
        response_data.append(can_consult_data)
    
    cursor.close()
    conn.close()

    return jsonify(response_data)

# Route to get houses that a user can consult
@app.route('/api/v1/get_houses/<user_id>', methods=['GET'])
def get_houses_of_a_user(user_id):
    """
    Get a list of houses that a user can consult

    This endpoint returns a list of houses that a specific user can consult.

    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: A list of houses
        schema:
          type: array
          items:
            type: object
            properties:
              house_id:
                type: integer
              house_name:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT house_id FROM can_consult WHERE user_id = %s', (user_id,))
    results = cursor.fetchall()

    data = []

    for row in results:
        house_id = row[0]

        cursor.execute('SELECT house_name FROM house WHERE house_id = %s', (house_id,))
        house_results = cursor.fetchall()
        house_name = house_results[0][0]

        house_data = {
            'house_id': house_id,
            'house_name': house_name
        }
        data.append(house_data)
    
    cursor.close()
    conn.close()

    return jsonify(data)

# Route to get rooms of a house
@app.route('/api/v1/get_rooms/<house_id>', methods=['GET'])
def get_rooms_of_a_house(house_id):
    """
    Get a list of rooms in a specific house

    This endpoint returns a list of rooms that belong to a specific house.

    ---
    parameters:
      - name: house_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A list of rooms
        schema:
          type: array
          items:
            type: object
            properties:
              room_id:
                type: integer
              room_name:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT room_id FROM room WHERE house_id = %s', (house_id,))
    results = cursor.fetchall()

    data = []

    for row in results:
        room_id = row[0]

        cursor.execute('SELECT room_name FROM room WHERE room_id = %s', (room_id,))
        room_results = cursor.fetchall()
        room_name = room_results[0][0]

        room_data = {
            'room_id': room_id,
            'room_name': room_name
        }
        data.append(room_data)
    
    cursor.close()
    conn.close()

    return jsonify(data)

# Route to get cameras of a house
@app.route('/api/v1/get_cameras/<house_id>', methods=['GET'])
def get_cameras_of_a_house(house_id):
    """
    Get a list of cameras in a specific house

    This endpoint returns a list of cameras that belong to a specific house.

    ---
    parameters:
      - name: house_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A list of cameras
        schema:
          type: array
          items:
            type: object
            properties:
              camera_id:
                type: integer
              camera_name:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT camera_id FROM camera WHERE house_id = %s', (house_id,))
    results = cursor.fetchall()

    data = []

    for row in results:
        camera_id = row[0]

        cursor.execute('SELECT camera_name FROM camera WHERE camera_id = %s', (camera_id,))
        camera_results = cursor.fetchall()
        camera_name = camera_results[0][0]

        camera_data = {
            'camera_id': camera_id,
            'camera_name': camera_name
        }
        data.append(camera_data)
    
    cursor.close()
    conn.close()

    return jsonify(data)

# Route to get disparitions history of a house_id with date, hour, room_name, object and image_overview
@app.route('/api/v1/get_disparitions_history/<house_id>', methods=['GET'])
def get_disparitions_history_of_a_house(house_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM room WHERE house_id = %s', (house_id,))
    results = cursor.fetchall()

    data = []

    for row in results:
        room_id = row[1]

        cursor.execute('SELECT room_name FROM room WHERE room_id = %s', (room_id,))
        room_results = cursor.fetchall()
        room_name = room_results[0][0]

        disparition_data = {
            'room_id': room_id,
            'room_name': room_name
        }
        data.append(disparition_data)

    cursor.close()
    conn.close()

    return jsonify(data)

# Route to get videos of a room of a house
# Return json with house_id and house_name, room_id and room_name, and videos
# videos : video_id, video_date, video_length, video_object_stolen, video_link
@app.route('/api/v1/get_videos/<house_id>/<room_id>', methods=['GET'])
def get_videos_of_a_room_of_a_house(house_id, room_id):
    """
    Get a list of videos in a specific room of a house

    This endpoint returns a list of videos that belong to a specific room in a specific house.

    ---
    parameters:
      - name: house_id
        in: path
        type: integer
        required: true
      - name: room_id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: A list of videos
        schema:
          type: object
          properties:
            house_id:
              type: integer
            house_name:
              type: string
            room_id:
              type: integer
            room_name:
              type: string
            videos:
              type: array
              items:
                type: object
                properties:
                  video_id:
                    type: integer
                  video_date:
                    type: string
                  video_length:
                    type: string
                  video_object_stolen:
                    type: boolean
                  video_link:
                    type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT house_name FROM house WHERE house_id = %s', (house_id,))
    house_results = cursor.fetchall()
    house_name = house_results[0][0]

    cursor.execute('SELECT room_name FROM room WHERE room_id = %s', (room_id,))
    room_results = cursor.fetchall()
    room_name = room_results[0][0]

    cursor.execute('SELECT * FROM video WHERE room_id = %s', (room_id,))
    video_results = cursor.fetchall()

    data = []

    for row in video_results:
        video_id = row[0]
        video_date = str(row[1])  # Convertir timedelta en chaîne
        video_length = str(row[2])  # Convertir timedelta en chaîne
        video_object_stolen = row[3]
        video_link = row[4]

        video_data = {
            'video_id': video_id,
            'video_date': video_date,
            'video_length': video_length,
            'video_object_stolen': video_object_stolen,
            'video_link': video_link
        }
        data.append(video_data)

    response_data = {
        'house_id': house_id,
        'house_name': house_name,
        'room_id': room_id,
        'room_name': room_name,
        'videos': data
    }

    cursor.close()
    conn.close()

    return jsonify(response_data)

# Route to get videos of a house
# Return json with disparition_id, disparition_date, disparition_object_stolen, disparition_image_overview, 
# room_id, camera_id, video_id, video_date, video_length, video_link, camera_name, room_name, house_id, house_name
@app.route('/api/v1/get_disparitions/<house_id>', methods=['GET'])
def get_disparitions_of_a_house(house_id):
    """
    Get a list of disparitions in a specific house

    This endpoint returns a list of disparitions that belong to a specific house.

    ---
    parameters:
      - name: house_id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: A list of disparitions
        schema:
          type: array
          items:
            type: object
            properties:
              disparition_id:
                type: integer
              disparition_date:
                type: string
              disparition_object_stolen:
                type: boolean
              disparition_image_overview:
                type: string
              disparition_object:
                type: string
              camera_id:
                type: integer
              room_id:
                type: integer
              room_name:
                type: string
              camera_name:
                type: string
              video_id:
                type: integer
              video_date:
                type: string
              video_length:
                type: string
              video_link:
                type: string
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    request = 'SELECT * FROM disparition WHERE room_id IN (SELECT room_id FROM room WHERE house_id = %s)'

    cursor.execute(request, (house_id,))
    disparition_results = cursor.fetchall()

    data = []

    for row in disparition_results:
        disparition_id = row[0]
        disparition_date = str(row[1])
        disparition_object_stolen = row[2]
        disparition_image_overview = row[3]
        disparition_object = row[4]
        camera_id = row[5]
        room_id = row[6]

        cursor.execute('SELECT room_name FROM room WHERE room_id = %s', (room_id,))
        room_results = cursor.fetchall()
        room_name = room_results[0][0]

        cursor.execute('SELECT camera_name FROM camera WHERE camera_id = %s', (camera_id,))
        camera_results = cursor.fetchall()
        camera_name = camera_results[0][0]
        
        cursor.execute('SELECT video_id, video_date, video_length, video_link FROM video WHERE disparition_id = %s', (disparition_id,))
        video_results = cursor.fetchall()
        video_id = video_results[0][0]
        video_date = str(video_results[0][1])
        video_length = str(video_results[0][2])
        video_link = video_results[0][3]

        data.append({
            'disparition_id': disparition_id,
            'disparition_date': disparition_date,
            'disparition_object_stolen': disparition_object_stolen,
            'disparition_image_overview': disparition_image_overview,
            'disparition_object': disparition_object,
            'camera_id': camera_id,
            'room_id': room_id,
            'room_name': room_name,
            'camera_name': camera_name,
            'video_id': video_id,
            'video_date': video_date,
            'video_length': video_length,
            'video_link': video_link,
        })

    cursor.close()
    conn.close()

    return jsonify(data)

# Route to create a disparition
@app.route('/api/v1/create_disparition', methods=['POST'])
def create_disparition():
    """
    Create a new disparition

    This endpoint creates a new disparition in the system.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            disparition_date:
              type: string
            disparition_object_stolen:
              type: integer
            disparition_image_overview:
              type: string
            disparition_object:
              type: string
            camera_id:
              type: integer
            room_id:
              type: integer
            video_id:
              type: integer

    responses:
      200:
        description: Disparition created successfully
        schema:
          type: object
          properties:
            status:
              type: string
              description: Status message
    """
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    disparition_date = request.json['disparition_date']
    disparition_object_stolen = request.json['disparition_object_stolen']
    disparition_image_overview = request.json['disparition_image_overview']
    disparition_object = request.json['disparition_object']
    camera_id = request.json['camera_id']
    room_id = request.json['room_id']
    video_id = request.json['video_id']

    cursor.execute('INSERT INTO disparition (disparition_date, disparition_object_stolen, disparition_image_overview, disparition_object, camera_id, room_id) VALUES (%s, %s, %s, %s, %s, %s)', (disparition_date, disparition_object_stolen, disparition_image_overview, disparition_object, camera_id, room_id))
    conn.commit()

    cursor.execute('INSERT INTO video (video_date, video_length, video_link, disparition_id) VALUES (%s, %s, %s, %s)', (disparition_date, '00:00:00', 'https://www.youtube.com', cursor.lastrowid))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        'status': 'Disparition created successfully'
    })

if __name__ == '__main__':
    app.run(debug=True)