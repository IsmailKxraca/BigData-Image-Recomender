from Image_Recomender.code.database import get_path_from_id
from Image_Recomender.code.database import connect_test_database
from Image_Recomender.code.database import close_test_pictures_connection

def test_get_path_from_id():
    conn = connect_test_database()

    Id = 10
    expected_output = r"D:\images\weather_image_recognition\dew\2217.jpg"

    output = get_path_from_id(conn, Id)

    assert output == expected_output


