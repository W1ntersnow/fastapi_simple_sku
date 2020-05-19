import pytest
import db.models as models


@pytest.mark.parametrize('input_data', [
    {
        "title": "test_type1",
        "description": "test_type1_desc",
    },
])
def test_create_item_type(input_data, client, db):
    response = client.post(
        "/v1/item_type/",
        json=input_data,
    )
    assert response.status_code == 200

    res_json = response.json()

    for key, value in input_data.items():
        assert res_json[key] == value

    assert 'id' in res_json

    row_id = res_json['id']

    db_row = db.query(models.ItemType).filter(models.ItemType.id == row_id).first()
    assert db_row is not None

    db.query(models.ItemType).delete()
    db.commit()
